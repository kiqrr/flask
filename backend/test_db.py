import sqlite3

def test_db():
    conn = sqlite3.connect('backend/database.db')
    cursor = conn.cursor()
    
    print("Testing pets table:")
    cursor.execute('''
        SELECT 
            p.Cod_animal,
            p.Nome_animal,
            p.status,
            p.data_perda,
            p.observacoes,
            u.Nome_usuario || ' ' || u.sobrenome_usuario as owner_name,
            u.telefone,
            e.Bairro || ', ' || e.Cidade || ' - ' || e.Estado as location
        FROM pets p
        JOIN usuario u ON p.cod_usuario = u.Cod_usuario
        JOIN endereco e ON u.cod_endereco = e.Cod_endereco
        WHERE p.status = 'perdido'
    ''')
    
    rows = cursor.fetchall()
    for row in rows:
        print("\nPet record:")
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Status: {row[2]}")
        print(f"Lost date: {row[3]}")
        print(f"Observations: {row[4]}")
        print(f"Owner: {row[5]}")
        print(f"Phone: {row[6]}")
        print(f"Location: {row[7]}")
    
    conn.close()

if __name__ == '__main__':
    test_db()
