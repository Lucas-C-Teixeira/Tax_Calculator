from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from bridge import TaxEngineBridge

app = Flask(__name__, 
            template_folder='web/templates', 
            static_folder='web/static')

app.secret_key = 'desenvolvimento_seguro_123' # Para gerenciar sessões e mensagens

DATABASE = 'database/taxes.db'
bridge = TaxEngineBridge()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# --- ROTAS ---

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Aqui buscaremos na sua tabela 'accounts'
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM accounts WHERE username = ?', (username,)).fetchone()
        conn.close()

        # Validando (Substitua por hash de senha no futuro para ser 100% profissional)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        
        flash('Credenciais inválidas. Tente novamente.', 'error')
    
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)