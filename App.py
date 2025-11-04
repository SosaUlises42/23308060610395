from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "clave-secreta"

@app.route('/')
def index():
    return render_template('yepez.html')

@app.route('/principal')
def principal():
    return render_template('index.html')

@app.route('/buscar', methods = ['POST','GET'])
def buscar():
    if request.method == 'POST':
        busqueda = request.form['busqueda']

        if busqueda == "calendario" or busqueda == "agenda" or busqueda == "plan":
            return redirect(url_for('calendary'))
        elif busqueda == "control alimenticio" or busqueda == "contar calorias" or busqueda == "comparar alimentos":
            flash('Estamos trabajando en esta seccion')
            return redirect(url_for('principal'))
        else:
            flash('Ningun resultado coincide con la busqueda', 'error')
            return redirect(url_for('principal')) 
    
    return render_template('index.html')

@app.route('/calendary')
def calendary():
    return render_template('calendario.html')

@app.route('/inciosecion')
def sesion():
    return render_template('iniciosecion.html')

@app.route('/registro', methods = ['POST','GET'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        peso = request.form['peso']
        altura = request.form['altura']
        edad = request.form['edad']
        
        if not nombre or not correo or not contraseña or not peso or not altura or not edad:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("sesion"))
        else:
            flash(f"Nuevo usuario existente: nombre: {nombre} correo: {correo} contraseña: {contraseña} peso: {peso} altura: {altura} edad: {edad}")
            return redirect(url_for("sesion"))
            
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)