from flask import Flask, render_template, request, redirect, url_for, flash, session

comidas =[]

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

@app.route('/registrosecion')
def registrosecion():
    return render_template('iniciosecion.html')

@app.route('/crtlComida')
def crtlComida():
    return render_template('ctrl.html', table = comidas)

@app.route('/control', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        alimento = request.form.get('alimento', '')
        calorias = request.form.get('calorias', '')
        proteinas = request.form.get('proteinas', '')
        cahrbohidratos = request.form.get('cahrbohidratos', '')
        grasas = request.form.get('grasas', '')

        if alimento and calorias and proteinas and cahrbohidratos and grasas:
            comidas.append({
                'nombre':alimento,
                'calorias':calorias,
                'proteinas':proteinas,
                'cahrbohidratos':cahrbohidratos,
                'grasas':grasas
            })

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
        if email == session["correo"] and password == session["contraseña"]:
            valid = True
            flash("Sesion iniciada correctamente")
            return redirect(url_for("principal"))
        else:
            flash("Los datos de usuario no coinciden", "error")
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
        
        if not nombre or not correo or not contraseña or not peso or not altura or not edad:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("registrosecion"))
        else:
            flash(f"Nuevo usuario existente: nombre: {nombre} correo: {correo} contraseña: {contraseña} peso: {peso} altura: {altura} edad: {edad}")
            session["correo"] = correo 
            session["contraseña"]= contraseña
            return redirect(url_for("registrosecion"))
            
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)