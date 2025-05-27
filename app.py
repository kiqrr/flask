from flask import Flask, request, render_template, redirect, url_for
import pyodbc
import re

app = Flask(__name__)

conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=EventoGeekDB;'
    'UID=flask_user;'
    'PWD=SenhaSegura123!'
)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nome_completo = request.form['nome_completo']
    email = request.form['email']
    categoria = request.form['categoria']
    personagem_jogo = request.form['personagem_jogo']
    nivel_experiencia = request.form['nivel_experiencia']

    # Validação básica
    if not nome_completo.strip() or not personagem_jogo.strip():
        return "<h2>Nome completo e personagem/jogo são obrigatórios.</h2><a href='/'>Voltar</a>"

    # Validação de email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "<h2>Email inválido.</h2><a href='/'>Voltar</a>"

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

from flask import Flask, request, render_template, redirect, url_for
import pyodbc
import re

app = Flask(__name__)

conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=EventoGeekDB;'
    'UID=flask_user;'
    'PWD=SenhaSegura123!'
)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nome_completo = request.form['nome_completo']
    email = request.form['email']
    categoria = request.form['categoria']
    personagem_jogo = request.form['personagem_jogo']
    nivel_experiencia = request.form['nivel_experiencia']

    # Validação básica
    if not nome_completo.strip() or not personagem_jogo.strip():
        return "<h2>Nome completo e personagem/jogo são obrigatórios.</h2><a href='/'>Voltar</a>"

    # Validação de email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "<h2>Email inválido.</h2><a href='/'>Voltar</a>"

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


@app.route('/inscricoes')
def listar_inscricoes():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Inscricoes")
        inscricoes = cursor.fetchall()
        cursor.close()
        conn.close()

        html = "<h1>Inscrições Realizadas</h1><ul>"
        for insc in inscricoes:
            html += f"<li>{insc.id} - {insc.nome_completo} - {insc.email} - {insc.categoria} - {insc.personagem_jogo} - {insc.nivel_experiencia} \
                     [<a href='/editar/{insc.id}'>Editar</a>] \
                     [<a href='/deletar/{insc.id}'>Deletar</a>]</li>"
        html += "</ul><a href='/'>Voltar ao Formulário</a>"
        return html
    except Exception as e:
        return f"<h2>Erro ao listar inscrições:</h2><pre>{e}</pre>"

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    if request.method == 'POST':
        nome_completo = request.form['nome_completo']
        email = request.form['email']
        categoria = request.form['categoria']
        personagem_jogo = request.form['personagem_jogo']
        nivel_experiencia = request.form['nivel_experiencia']

        cursor.execute("""
            UPDATE Inscricoes
            SET nome_completo=?, email=?, categoria=?, personagem_jogo=?, nivel_experiencia=?
            WHERE id=?
        """, (nome_completo, email, categoria, personagem_jogo, nivel_experiencia, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('listar_inscricoes'))
    else:
        cursor.execute("SELECT * FROM Inscricoes WHERE id=?", (id,))
        insc = cursor.fetchone()
        cursor.close()
        conn.close()

        if not insc:
            return "<h2>Inscrição não encontrada.</h2>"

        return f"""
        <h1>Editar Inscrição</h1>
        <form method='post'>
            Nome completo: <input name='nome_completo' value='{insc.nome_completo}' required><br>
            Email: <input name='email' value='{insc.email}' required><br>
            Categoria: <input name='categoria' value='{insc.categoria}' required><br>
            Personagem/Jogo: <input name='personagem_jogo' value='{insc.personagem_jogo}' required><br>
            Nível: <input name='nivel_experiencia' value='{insc.nivel_experiencia}' required><br>
            <button type='submit'>Atualizar</button>
        </form>
        """

@app.route('/deletar/<int:id>')
def deletar(id):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Inscricoes WHERE id=?", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('listar_inscricoes'))
    except Exception as e:
        return f"<h2>Erro ao deletar inscrição:</h2><pre>{e}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
