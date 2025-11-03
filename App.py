from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "clave-secreta"

@app.route('/')
def index():
    return render_template('iniciosecion.html')

@app.route('/inciosecion')
def sesion():
    return render_template('base.html')

@app.route('/registro', methods = ['POST','GET'])
def registro():
    error = None
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        peso = request.form['peso']
        altura = request.form['altura']
        edad = request.form['edad']
        
        if not nombre or not correo or not contraseña or not peso or not altura or not edad:
            flash("Todos los campos son obligatorios", "error")
            redirect(url_for("index"))
        else:
            flash(f"Nuevo usuario existente: nombre: {nombre} correo: {correo} contraseña: {contraseña} peso: {peso} altura: {altura} edad: {edad}")
            redirect(url_for("index"))
            
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)