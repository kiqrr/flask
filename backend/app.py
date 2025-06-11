from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

pets = [
    {'id': 1, 'name': 'Miau da Silva', 'species': 'Cat', 'breed': 'Domestic Shorthair', 'age': 3, 'size': 'Small', 'lost_date': '2023-01-02', 'lost_location': 'Avenida Washington Luis'},
    {'id': 2, 'name': 'Caramelho', 'species': 'Dog', 'breed': 'Mixed Breed', 'age': 5, 'size': 'Medium', 'lost_date': '2023-01-02', 'lost_location': 'Avenida Washington Luis'},
    {'id': 3, 'name': 'Sabido', 'species': 'Parrot', 'breed': 'Budgerigar', 'age': 1, 'size': 'Small', 'lost_date': '2023-01-02', 'lost_location': 'Avenida Washington Luis'}
]

@app.route('/pets', methods=['GET'])
def get_pets():
    return jsonify(pets)

@app.route('/pets/<int:id>', methods=['GET'])
def get_pet(id):
    pet = next((pet for pet in pets if pet['id'] == id), None)
    if pet:
        return jsonify(pet)
    return jsonify({'message': 'Pet not found'}), 404

@app.route('/pets', methods=['POST'])
def create_pet():
    new_pet = request.get_json()
    new_pet['id'] = len(pets) + 1
    pets.append(new_pet)
    return jsonify(new_pet), 201

@app.route('/pets/<int:id>', methods=['PUT'])
def update_pet(id):
    pet = next((pet for pet in pets if pet['id'] == id), None)
    if pet:
        data = request.get_json()
        pet.update(data)
        return jsonify(pet)
    return jsonify({'message': 'Pet not found'}), 404

@app.route('/pets/<int:id>', methods=['DELETE'])
def delete_pet(id):
    pet = next((pet for pet in pets if pet['id'] == id), None)
    if pet:
        pets.remove(pet)
        return jsonify({'message': 'Pet deleted'})
    return jsonify({'message': 'Pet not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
