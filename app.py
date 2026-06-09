from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from bridge import TaxEngineBridge
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(
    __name__,
    template_folder='web/templates',
    static_folder='web/static'
)

app.secret_key = 'desenvolvimento_seguro_123'

DATABASE = 'database/taxes.db'
bridge = TaxEngineBridge()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- ROTAS ---------------- #

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    # Se já estiver logado
    if 'user' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':

        input_email = request.form.get('username')
        input_password = request.form.get('password')

        conn = get_db_connection()

        user = conn.execute(
            'SELECT * FROM accounts WHERE email = ?',
            (input_email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user['password_hash'], input_password):

            session['user'] = user['email']
            session['account_id'] = user['account_id']

            return redirect(url_for('home'))

        flash('E-mail ou senha incorretos.', 'error')

    return render_template('login.html')


@app.route('/home')
def home():

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    # Histórico
    history = conn.execute("""
        SELECT
            tax_type,
            revenue_cents,
            tax_amount_cents,
            fiscal_date
        FROM tax_calculations
        WHERE account_id = ?
        ORDER BY fiscal_date ASC
    """, (
        session['account_id'],
    )).fetchall()

    # Últimos cálculos
    recent = conn.execute("""
        SELECT
            tax_type,
            revenue_cents,
            tax_amount_cents,
            fiscal_date
        FROM tax_calculations
        WHERE account_id = ?
        ORDER BY fiscal_date DESC
        LIMIT 5
    """, (
        session['account_id'],
    )).fetchall()

    conn.close()

    # Analytics
    total_calculations = len(history)

    total_tax = sum(
        item['tax_amount_cents']
        for item in history
    ) / 100 if history else 0

    latest_tax = (
        history[-1]['tax_amount_cents'] / 100
        if history else 0
    )

    return render_template(
        'home.html',

        history=history,
        recent=recent,

        total_calculations=total_calculations,
        total_tax=total_tax,
        latest_tax=latest_tax
    )


@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validação básica
        if password != confirm_password:

            flash('As senhas não coincidem.', 'error')

            return redirect(url_for('register'))

        conn = get_db_connection()

        # Verifica se usuário já existe
        existing_user = conn.execute(
            'SELECT * FROM accounts WHERE email = ?',
            (email,)
        ).fetchone()

        if existing_user:

            conn.close()

            flash('Este e-mail já está cadastrado.', 'error')

            return redirect(url_for('register'))

        # GUID único
        account_guid = str(uuid.uuid4())

        # Hash da senha
        hashed_password = generate_password_hash(password)

        # Cria conta já verificada
        conn.execute("""
            INSERT INTO accounts (
                account_guid,
                email,
                password_hash,
                email_verified
            )
            VALUES (?, ?, ?, ?)
        """, (
            account_guid,
            email,
            hashed_password,
            1
        ))

        conn.commit()
        conn.close()

        flash('Conta criada com sucesso.', 'success')

        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/irpf', methods=['GET', 'POST'])
def irpf():

    if 'user' not in session:
        return redirect(url_for('login'))
    
    result = None
    if request.method == 'POST':
        try:
            income = float(
                request.form.get('income', 0)
            )
            dependents = int(
                request.form.get('dependents', 0)
            )
            deduction_mode = request.form.get(
                'deduction_mode'
            )
            custom_deduction = request.form.get(
                'custom_deduction',
                0
            )
            # EVITA STRING VAZIA
            if custom_deduction == '':
                custom_deduction = 0
            custom_deduction = float(
                custom_deduction
            )
            # HTML -> C ENUM
            if deduction_mode == 'simplified':
                deduction_mode = 0
            else:
                deduction_mode = 1
            # DEBUG
            print("\n=== DEBUG IRPF ===")
            print("Income:", income)
            print("Dependents:", dependents)
            print("Custom deduction:", custom_deduction)
            print("Deduction mode:", deduction_mode)
            # C ENGINE
            tax_result = bridge.run_irpf(
                income,
                dependents,
                custom_deduction,
                deduction_mode
            )
            print("Tax Result:", tax_result)
            print("==================\n")

            result = bridge.format_brl(
                tax_result
            )

            conn = get_db_connection()
            user = conn.execute(
                '''
                SELECT account_id
                FROM accounts
                WHERE email = ?
                ''',
                (session['user'],)
            ).fetchone()
            conn.execute("""
                INSERT INTO tax_calculations (
                    account_id,
                    person_id,
                    tax_type,
                    revenue_cents,
                    tax_amount_cents
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                user['account_id'],
                None,
                'IRPF',
                int(income * 100),
                int(tax_result * 100)
            ))
            conn.commit()
            conn.close()
            flash(
                'Cálculo realizado com sucesso.',
                'success'
            )
        except Exception as e:
            print(e)
            flash(
                f'Erro no cálculo: {e}',
                'error'
            )
    return render_template(
        'irpf.html',
        result=result
    )

@app.route('/irpj', methods=['GET', 'POST'])
def irpj():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    result = None
    if request.method == 'POST':
        try:
            # 1. Captura os dados do formulário HTML
            regime_form = request.form.get('regime_type', 'presumido') # 'real' ou 'presumido'
            revenue = float(request.form.get('revenue', 0))
            
            # Mapeamento estrito para o que a sua bridge.py espera ("REAL" ou "PRESUMED")
            db_regime_code = "REAL" if regime_form == "real" else "PRESUMED"
            
            # 2. Tratamento dos parâmetros baseados no regime (Evita passar lixo para a Struct C)
            if db_regime_code == "REAL":
                expenses = request.form.get('expenses', 0)
                expenses = float(expenses) if expenses != '' else 0.0
                margin = 0.0
            else:
                expenses = 0.0
                margin_form = request.form.get('presumption_rate', 0)
                # irpj.c exige float entre 0.0 e 1.0 (ex: 32% -> 0.32)
                margin = float(margin_form) / 100.0 if margin_form != '' else 0.0

            # 3. DEBUG NO TERMINAL (Padrão idêntico ao seu IRPF)
            print("\n=== DEBUG IRPJ ===")
            print("Regime Form:", regime_form)
            print("Mapped for Bridge:", db_regime_code)
            print("Revenue:", revenue)
            print("Expenses:", expenses)
            print("Margin (Decimal):", margin)

            # 4. EXECUÇÃO NA ENGINE EM C VIA BRIDGE
            tax_result = bridge.run_irpj(
                db_regime_code=db_regime_code,
                revenue=revenue,
                expenses=expenses,
                margin=margin
            )
            print("Tax Result dos centavos:", tax_result)
            print("==================\n")

            # 5. FORMATAÇÃO PARA EXIBIÇÃO NO TOPO DO HTML
            result = bridge.format_brl(tax_result)

            # 6. PERSISTÊNCIA NO BANCO DE DADOS (Respeitando estritamente o seu Schema)
            conn = get_db_connection()
            
            # Busca o account_id do usuário logado
            user = conn.execute(
                '''
                SELECT account_id 
                FROM accounts 
                WHERE email = ?
                ''', 
                (session['user'],)
            ).fetchone()
            
            if user:
                # Inserção na tabela de fatos 'tax_calculations'
                # Como é uma simulação livre do painel, company_id e person_id vão como None (NULL)
                conn.execute("""
                    INSERT INTO tax_calculations (
                        account_id,
                        company_id,
                        person_id,
                        tax_type,
                        revenue_cents,
                        tax_amount_cents
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    user['account_id'],
                    None,                 # company_id (NULL) para simulação avulsa
                    None,                 # person_id (NULL) pois é um cálculo de PJ
                    'IRPJ',
                    int(revenue * 100),   # Armazenando em centavos como pede o seu Schema
                    int(tax_result * 100) # Armazenando em centavos como pede o seu Schema
                ))
                conn.commit()
            
            conn.close()
            flash('Cálculo do IRPJ realizado e salvo com sucesso.', 'success')
            
        except Exception as e:
            print(f"Erro na execução da rota IRPJ: {e}")
            flash(f'Erro no cálculo do IRPJ: {e}', 'error')
            
    return render_template('irpj.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)