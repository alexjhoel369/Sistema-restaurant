from flask import request, redirect, render_template, session
from app.models.usuario_model import Usuario

def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario = Usuario.query.filter_by(email=email).first()

        #por ahora sin bcrypt (luego lo mejoramos)
        if usuario and usuario.contraseña_hash == password:
            session['user_id'] = usuario.id_usuario
            session['user_name'] = usuario.nombre

            return redirect('/dashboard')

        return render_template('auth/login.html', error="Credenciales incorrectas")

    return render_template('auth/login.html')


def logout():
    session.clear()
    return redirect('/')

# ruta dashboard
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    return render_template('dashboard.html')