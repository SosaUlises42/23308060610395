from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "clave-secreta"

@app.route('/')
def index():
    return render_template('yepez.html')

@app.route('/principal/<int:cal>')
def principal(cal):
    return render_template('index.html', cal = cal)

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

@app.route('/registrosecion')
def registrosecion():
    return render_template('iniciosecion.html')

@app.route('/crtlComida')
def crtlComida():
    return render_template('ctrl.html')

@app.route('/control', methods=['GET', 'POST'])
def control():
    resultado = None
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        edad = float(request.form['edad'])
        genero = request.form['genero']
        actividad = request.form['actividad']

        if genero == 'hombre':
            resultado = 88.362 + 13.397 * peso + 4.799 * altura - 5.677 * edad
        elif genero == 'mujer':
            resultado = 447.593 + 9.247 * peso + 3.098 * altura - 4.330 * edad

        if actividad == "sedentario":
            resultado = resultado * 1.2
        elif actividad == "activo":
            resultado = resultado * 1.55
        elif actividad == "altoRendimiento":
            resultado = resultado * 1.9

        return render_template('ctrl.html', resultado = resultado)

    return redirect(url_for('crtlComida'))

@app.route('/inciosecion')
def sesion():
    return render_template('sesinguardada.html')

@app.route('/valida', methods=['GET', 'POST'])
def valida():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
    
    if not email or not password:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for("sesion"))
    else:
        if session != None:
            if email == session["correo"] and password == session["contraseña"]:
                session["valida"]=True
                flash("Sesion iniciada correctamente")
                return redirect(url_for("principal", cal = 1))
            else:
                flash("Los datos de usuario no coinciden", "error")
                return redirect(url_for("sesion"))
        else:
            flash("Aun no hay ususarios registrados", "error")
            return redirect(url_for("sesion"))

@app.route('/registro', methods = ['GET','POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        peso = request.form['peso']
        altura = request.form['altura']
        edad = request.form['edad']
        imgPerfil = request.form['imgPerfil']
        
        if not nombre or not correo or not contraseña or not peso or not altura or not edad:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("registrosecion"))
        else:
            flash(f"Nuevo usuario existente: nombre: {nombre} correo: {correo} contraseña: {contraseña} peso: {peso} altura: {altura} edad: {edad}")
            session["nombre"] = nombre
            session["correo"] = correo 
            session["contraseña"]= contraseña
            session["valida"]=False

            if not imgPerfil:
                session["imagen"]= "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
            else:
                session["imagen"]= imgPerfil

            return redirect(url_for("registrosecion"))
            
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)