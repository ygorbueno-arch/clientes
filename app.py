from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do Banco de Dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da Tabela de Clientes
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# Cria o banco de dados se não existir
with app.app_context():
    db.create_all()

# Rota Principal: Lista os clientes
@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

# Rota para Cadastrar: Recebe os dados do formulário
@app.route('/add', methods=['POST'])
def add_cliente():
    nome = request.form.get('nome')
    email = request.form.get('email')

    if nome and email:
        novo_cliente = Cliente(nome=nome, email=email)
        db.session.add(novo_cliente)
        db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)