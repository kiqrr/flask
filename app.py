from flask import Flask, request, render_template
import pyodbc

app = Flask(__name__)

# String de conexão
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=EventoGeekDB;'
    'UID=flask_user;'
    'PWD=SenhaSegura123!'
)

# Rota principal: exibe o formulário
@app.route('/')
def index():
    return render_template('form.html')

# Rota para tratar os dados enviados pelo formulário
@app.route('/enviar', methods=['POST'])
def enviar():
    nome_completo = request.form['nome_completo']
    email = request.form['email']
    categoria = request.form['categoria']
    personagem_jogo = request.form['personagem_jogo']
    nivel_experiencia = request.form['nivel_experiencia']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Inscricoes (nome_completo, email, categoria, personagem_jogo, nivel_experiencia)
            VALUES (?, ?, ?, ?, ?)
        """, (nome_completo, email, categoria, personagem_jogo, nivel_experiencia))
        conn.commit()
        cursor.close()
        conn.close()
        return "<h2>Inscrição realizada com sucesso!</h2><a href='/'>Voltar</a>"
    except Exception as e:
        return f"<h2>Erro ao salvar inscrição:</h2><pre>{e}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
