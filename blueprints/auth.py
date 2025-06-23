from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Esta variable la asignamos desde app.py
mysql = None

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('txtCorreo')
        password = request.form.get('txtPassword')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo=%s AND password=%s', (correo, password))
        account = cur.fetchone()
        cur.close()

        if account:
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol'] = account['id_rol']
            session['usuario'] = account  # guardar usuario para luego usarlo

            return redirect(url_for('auth.welcome'))  # ⬅️ redirige después del login
        else:
            return render_template('login.html', mensaje="Usuario o contraseña incorrectas")
    
    return render_template('login.html')

@auth_bp.route('/welcome')
def welcome():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('auth.login'))  # redirige si no está logueado
    return render_template('welcome.html', usuario=usuario)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        rol = request.form.get('rol')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (correo, password, id_rol) VALUES (%s, %s, %s)", (correo, password, rol))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('auth.login'))
    
    return render_template('registro.html')
