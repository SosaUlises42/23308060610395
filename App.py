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
            return redirect(url_for('crtlComida')) 
    
    return render_template('index.html')

@app.route('/macroscal', methods = ['POST','GET'])
def macroscal():
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        edad = float(request.form['edad'])
        grasa = float(request.form['grasa'])
        genero = request.form['genero']
        actividad = request.form['actividad']
        objetivos = request.form['objetivos']

        if genero == 'hombre':
            tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
        else:
            tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

        factores = {
            'sedentario': 1.2,
            'ligero': 1.375,
            'moderado': 1.55,
            'intenso': 1.725,
            'muy_intenso': 1.9
        }
        factor_act = factores.get(actividad, 1.2)
        gct = tmb * factor_act

        if objetivos == 'bajar':
            calorias_objetivo = gct - 400
        elif objetivos == 'subir':
            calorias_objetivo = gct + 300
        else:
            calorias_objetivo = gct

        masa_magra = peso * (1 - grasa / 100.0)

        if objetivos == 'bajar':
            prot_g = masa_magra * 2.0
        elif objetivos == 'subir':
            prot_g = masa_magra * 2.0
        else:  # mantener
            prot_g = masa_magra * 1.6

        prot_kcal = prot_g * 4
        grasa_kcal = grasa_g * 9

        carb_kcal = calorias_objetivo - (prot_kcal + grasa_kcal)
        carb_g = carb_kcal / 4 if carb_kcal > 0 else 0

        resultados = {
            'cal': round(calorias_objetivo),
            'pro': round(prot_g),
            'carbo': round(carb_g),
        }

        return render_template('calendario.html', resultados=resultados)

    return render_template('calendario.html')



@app.route('/macros')
def macros():
    return render_template('calendario.html')

@app.route('/registrosecion/<int:paso>')
def registrosecion(paso):
    return render_template('iniciosecion.html', paso = paso)

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

@app.route('/registro/<int:paso>', methods = ['GET','POST'])
def registro(paso):
    if request.method == 'POST':

        if paso == 1:
            nombre = request.form['nombre']
            correo = request.form['correo']
            contraseña = request.form['contraseña']
            peso = request.form['peso']
            altura = request.form['altura']
            edad = request.form['edad']
            imgPerfil = request.form['imgPerfil']
            genero = request.form['genero']
            actividad = request.form['actividad']
            
            if not nombre or not correo or not contraseña or not peso or not altura or not edad or not genero or not actividad:
                flash("Todos los campos son obligatorios", "error")
                return redirect(url_for("registrosecion", paso = 1) + "#formu")
            else:
                session["nombre"] = nombre
                session["correo"] = correo 
                session["contraseña"]= contraseña
                session["valida"]=False

                if not imgPerfil:
                    session["imagen"]= "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
                else:
                    session["imagen"]= imgPerfil

            return redirect(url_for("registrosecion", paso = paso + 1) + "#formu")
        elif paso == 2:
            objetivos = request.form.getlist("objetivos")


            if not objetivos:
                flash("Por favor selecciona almenos un objetivo", "error")
                return redirect(url_for("registrosecion", paso = 2) + "#formu")
            else:
                return redirect(url_for("registrosecion", paso = paso + 1) + "#formu")
        else:
            alergias = request.form['alergias']
            intolerancias = request.form['intolerancias']
            dietas = request.form['dietas']
            disgusta = request.form['disgusta']
            nivel = request.form['nivel']

            if not alergias or not intolerancias or not dietas or not disgusta or not nivel:
                flash("Todos los campos son obligatorios", "error")
                return redirect(url_for("registrosecion", paso = 3) + "#formu")
            else:
                return redirect(url_for("principal", cal = 1))
            
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)