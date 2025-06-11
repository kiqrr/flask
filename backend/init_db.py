import sqlite3
from datetime import datetime

def init_db():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('backend/database.db')
    cursor = conn.cursor()

    # Read schema
    with open('backend/schema.sql', 'r') as f:
        schema = f.read()
    
    # Create tables
    cursor.executescript(schema)

    # Insert sample data
    # Enderecos
    enderecos = [
        (1, 'SP', 'São Paulo', 'Vila Madalena', 123, 'Apto 45', 5433020),
        (2, 'SP', 'São Paulo', 'Jardins', 456, None, 1401001),
        (3, 'SP', 'São Paulo', 'Moema', 789, 'Casa 2', 4077020),
        (4, 'SP', 'São Paulo', 'Pinheiros', 321, 'Cobertura', 5422011),
        (5, 'SP', 'São Paulo', 'Perdizes', 654, None, 5015010)
    ]
    cursor.executemany('INSERT INTO endereco VALUES (?,?,?,?,?,?,?)', enderecos)

    # Usuarios
    usuarios = [
        (1, 1, 'Maria', 'Silva', '11987654321', 'maria.silva@email.com'),
        (2, 2, 'João', 'Santos', '11976543210', 'joao.santos@email.com'),
        (3, 3, 'Ana', 'Costa', '11965432109', 'ana.costa@email.com'),
        (4, 4, 'Carlos', 'Oliveira', '11954321098', 'carlos.oliveira@email.com'),
        (5, 5, 'Lucia', 'Ferreira', '11943210987', 'lucia.ferreira@email.com')
    ]
    cursor.executemany('INSERT INTO usuario VALUES (?,?,?,?,?,?)', usuarios)

    # Pets
    pets = [
        (1, 1, 'Rex', '2024-01-15', '2024-06-01', None, 
         'Cão golden retriever, muito dócil, usa coleira azul', 'perdido'),
        (2, 2, 'Mimi', '2024-02-20', None, '2024-05-15', 
         'Gata siamesa encontrada no Parque Ibirapuera', 'encontrado'),
        (3, 3, 'Thor', '2024-03-10', '2024-05-20', '2024-05-25', 
         'Cão pastor alemão, foi resgatado com ferimentos leves', 'resgatado'),
        (4, 4, 'Luna', '2024-01-05', None, None, 
         'Cadela vira-lata adotada da ONG local', 'adotado'),
        (5, 5, 'Bolt', '2024-04-12', '2024-06-05', None, 
         'Cão pequeno porte, muito ativo, sem coleira', 'perdido')
    ]
    cursor.executemany('INSERT INTO pets VALUES (?,?,?,?,?,?,?,?)', pets)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
