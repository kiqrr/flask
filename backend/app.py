from flask import Flask, jsonify, request
from flask_cors import CORS
import pyodbc
import json
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return str(obj)

app.json_encoder = JSONEncoder

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
            WHERE p.status = 'perdido'
        ''')
        
        pets = cursor.fetchall()
        conn.close()
        
        pets_list = [dict_factory(cursor, row) for row in pets]
        return jsonify(pets_list)
    except Exception as e:
        print(f"Error in get_pets: {str(e)}")
        return jsonify({"error": str(e)}), 500

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
        conn.close()
        
        if pet:
            pet_dict = dict_factory(cursor, pet)
            return jsonify(pet_dict)
        return jsonify({'message': 'Pet not found'}), 404
    except Exception as e:
        print(f"Error in get_pet: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/pets', methods=['POST'])
def create_new_pet():
    try:
        data = request.get_json()
        success, result = create_pet(data)
        
        if success:
            return jsonify({'message': 'Pet registered successfully', 'id': result}), 201
        else:
            return jsonify({'message': 'Failed to register pet', 'error': result}), 400
            
    except Exception as e:
        print(f"Error in create_new_pet: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
