from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pyodbc
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_PHOTOS = 5

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return str(obj)

app.json_encoder = JSONEncoder

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def dict_factory(cursor, row):
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))

def get_db():
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=ALUNO33\MSSQLSERVER03;'
        r'DATABASE=cademeupet;'
        r'Trusted_Connection=yes;'
    )
    conn = pyodbc.connect(conn_str)
    return conn

def create_pet(data):
    conn = get_db()
    cursor = conn.cursor()
    try:
        # First, create address
        cursor.execute('''
            INSERT INTO endereco (Estado, Cidade, Bairro, Numero, Complemento, CEP)
            OUTPUT INSERTED.Cod_endereco
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['address']['state'],
            data['address']['city'],
            data['address']['neighborhood'],
            data['address']['number'],
            data['address']['complement'],
            data['address']['zip_code']
        ))
        address_id = cursor.fetchone()[0]

        # Then, create user
        cursor.execute('''
            INSERT INTO usuario (cod_endereco, Nome_usuario, sobrenome_usuario, telefone, email)
            OUTPUT INSERTED.Cod_usuario
            VALUES (?, ?, ?, ?, ?)
        ''', (
            address_id,
            data['owner']['first_name'],
            data['owner']['last_name'],
            data['owner']['phone'],
            data['owner']['email']
        ))
        user_id = cursor.fetchone()[0]

        # Finally, create pet
        cursor.execute('''
            INSERT INTO pets (cod_usuario, Nome_animal, status, data_registro, data_perda, observacoes)
            OUTPUT INSERTED.Cod_animal
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            data['pet']['name'],
            data['pet']['status'],
            datetime.now().strftime('%Y-%m-%d'),
            data['pet']['lost_date'],
            data['pet']['observations']
        ))
        pet_id = cursor.fetchone()[0]
        
        conn.commit()
        return True, pet_id
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

@app.route('/api/pets', methods=['GET'])
def get_pets():
    try:
        status_filter = request.args.get('status')
        state_filter = request.args.get('state')
        city_filter = request.args.get('city')

        conn = get_db()
        cursor = conn.cursor()

        base_query = '''
            SELECT 
                p.Cod_animal as id,
                p.Nome_animal as name,
                p.status,
                p.data_perda as lost_date,
                p.observacoes as observations,
                u.Nome_usuario + ' ' + u.sobrenome_usuario as owner_name,
                u.telefone as owner_phone,
                e.Bairro + ', ' + e.Cidade + ' - ' + e.Estado as lost_location,
                (SELECT TOP 1 photo_path FROM pet_photos WHERE pet_id = p.Cod_animal AND is_primary = 1) as primary_photo
            FROM pets p
            JOIN usuario u ON p.cod_usuario = u.Cod_usuario
            JOIN endereco e ON u.cod_endereco = e.Cod_endereco
        '''

        conditions = []
        params = []

        if status_filter and status_filter.lower() != 'todos':
            conditions.append('p.status = ?')
            params.append(status_filter)

        if state_filter:
            conditions.append('e.Estado = ?')
            params.append(state_filter)

        if city_filter:
            conditions.append('e.Cidade = ?')
            params.append(city_filter)

        if conditions:
            base_query += ' WHERE ' + ' AND '.join(conditions)

        cursor.execute(base_query, params)
        pets = cursor.fetchall()
        conn.close()

        pets_list = [dict_factory(cursor, row) for row in pets]
        return jsonify(pets_list)
    except Exception as e:
        print(f"Error in get_pets: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/pets', methods=['POST'])
def create_pet_route():
    data = request.get_json()
    success, result = create_pet(data)
    if success:
        return jsonify({'id': result}), 201
    else:
        return jsonify({'message': result}), 400

@app.route('/api/pets/<int:id>', methods=['GET'])
def get_pet(id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                p.Cod_animal as id,
                p.Nome_animal as name,
                p.status,
                p.data_perda as lost_date,
                p.observacoes as observations,
                u.Nome_usuario + ' ' + u.sobrenome_usuario as owner_name,
                u.telefone as owner_phone,
                e.Bairro + ', ' + e.Cidade + ' - ' + e.Estado as lost_location
            FROM pets p
            JOIN usuario u ON p.cod_usuario = u.Cod_usuario
            JOIN endereco e ON u.cod_endereco = e.Cod_endereco
            WHERE p.Cod_animal = ?
        ''', (id,))
        
        pet = cursor.fetchone()
        if not pet:
            conn.close()
            return jsonify({'message': 'Pet not found'}), 404
        
        pet_dict = dict_factory(cursor, pet)
        
        # Get all photos for the pet
        cursor.execute('''
            SELECT photo_id, photo_path, is_primary
            FROM pet_photos
            WHERE pet_id = ?
            ORDER BY is_primary DESC, photo_id ASC
        ''', (id,))
        photos = cursor.fetchall()
        conn.close()
        
        pet_dict['photos'] = [dict_factory(cursor, row) for row in photos]
        
        return jsonify(pet_dict)
    except Exception as e:
        print(f"Error in get_pet: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/pets/<int:id>/photos', methods=['POST'])
def upload_pet_photos(id):
    if 'photos' not in request.files:
        return jsonify({'message': 'No photos part in the request'}), 400
    
    files = request.files.getlist('photos')
    if len(files) == 0:
        return jsonify({'message': 'No photos uploaded'}), 400
    if len(files) > MAX_PHOTOS:
        return jsonify({'message': f'Maximum {MAX_PHOTOS} photos allowed'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    saved_photos = []
    try:
        # Check if pet exists
        cursor.execute('SELECT Cod_animal FROM pets WHERE Cod_animal = ?', (id,))
        pet = cursor.fetchone()
        if not pet:
            return jsonify({'message': 'Pet not found'}), 404
        
        # Check how many photos already exist
        cursor.execute('SELECT COUNT(*) FROM pet_photos WHERE pet_id = ?', (id,))
        count = cursor.fetchone()[0]
        if count + len(files) > MAX_PHOTOS:
            return jsonify({'message': f'You can upload only {MAX_PHOTOS - count} more photos'}), 400
        
        for idx, file in enumerate(files):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # To avoid filename conflicts, prepend pet id and timestamp
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
                filename = f"{id}_{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                print(f"Saved photo file at: {filepath}")
                
                # If no photos exist, mark first as primary
                is_primary = 0
                if count == 0 and idx == 0:
                    is_primary = 1
                
                cursor.execute('''
                    INSERT INTO pet_photos (pet_id, photo_path, is_primary)
                    VALUES (?, ?, ?)
                ''', (id, filename, is_primary))
                saved_photos.append(filename)
        
        conn.commit()
        return jsonify({'message': 'Photos uploaded successfully', 'files': saved_photos}), 201
    except Exception as e:
        conn.rollback()
        # Delete any saved files if database operation failed
        for photo in saved_photos:
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, photo))
            except:
                pass
        return jsonify({'message': 'Failed to upload photos', 'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/uploads/<path:filename>')
def serve_photo(filename):
    print(f"Serving photo: {filename}")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Full path: {os.path.join(UPLOAD_FOLDER, filename)}")
    print(f"File exists: {os.path.exists(os.path.join(UPLOAD_FOLDER, filename))}")
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/states', methods=['GET'])
def get_states():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT Estado FROM endereco ORDER BY Estado')
        states = [row[0] for row in cursor.fetchall()]
        conn.close()
        return jsonify(states)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cities', methods=['GET'])
def get_cities():
    try:
        state = request.args.get('state')
        if not state:
            return jsonify({'error': 'State parameter is required'}), 400
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT Cidade FROM endereco WHERE Estado = ? ORDER BY Cidade', (state,))
        cities = [row[0] for row in cursor.fetchall()]
        conn.close()
        return jsonify(cities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
