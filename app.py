from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Caminho para o arquivo do banco de dados
DATABASE = 'database.db'

def get_db_connection():
    """Cria uma conexão com o banco de dados e retorna o objeto."""
    conn = sqlite3.connect(DATABASE)
    # Isso permite acessar as colunas pelo nome (ex: cliente['nome']) em vez de apenas índice
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """Cria a tabela de clientes caso ela não exista."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa o banco ao rodar o app
init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    # Busca todos os clientes no banco
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('index.html', clientes=clientes)

@app.route('/add', methods=['POST'])
def add_cliente():
    nome = request.form.get('nome')
    email = request.form.get('email')

    if nome and email:
        conn = get_db_connection()
        # Uso de "?" para prevenir SQL Injection
        conn.execute('INSERT INTO clientes (nome, email) VALUES (?, ?)', (nome, email))
        conn.commit()
        conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)