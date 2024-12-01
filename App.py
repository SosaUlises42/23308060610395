from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import requests
from flask_mysqldb import MySQL
import os

API_KEY = "h5mDjpnjN1Z5X2qyHRJ8gSbhyaCP4f6P2WfcEjGz"

app = Flask(__name__)
app.secret_key = "clave-secreta"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nutriapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

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

@app.route('/macros/<int:cal>/<int:pro>/<int:car>', methods = ['POST','GET'])
def macros(cal, pro, car):
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
        else:
            prot_g = masa_magra * 1.6

        prot_kcal = prot_g * 4
        
        carb_percent = 0.5
        carb_kcal = calorias_objetivo * carb_percent

        carb_g = carb_kcal / 4 if carb_kcal > 0 else 0

        flash('Tus macronutrientes recomendados son:', 'macros')
        return redirect(url_for('macros', cal = round(calorias_objetivo, 2), pro = round(prot_g, 2), car = round(carb_g, 2)))

    return render_template('macros.html', cal = cal, pro = pro, car = car)

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

        resultado = round(resultado, 2)

        flash(f'Tu gasto calorico total es de {resultado}', 'gtc')
        return redirect(url_for('crtlComida'))

    return redirect(url_for('crtlComida'))

@app.route('/inciosecion')
def sesion():
    return render_template('sesinguardada.html')

@app.route("/valida", methods=["POST"])
def valida():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for("sesion"))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE correo = %s", (email,))
    user = cur.fetchone()
    cur.close()

    print(user)

    if user and user["contraseña"] == password:
        session["valida"] = True
        session["user_id"] = user["id"]
        session["nombre"] = user["nombre"]
        session["correo"] = user["correo"]
        session["imagen"] = user["imgPerfil"]
        session["genero"] = user["genero"]
        session["actividad"] = user["actividad"]
        session["peso"] = str(user["peso"])
        session["altura"] = str(user["altura"])

        flash("Sesión iniciada correctamente", "success")
        return redirect(url_for("principal", cal=1))

    flash("Correo o contraseña incorrectos", "error")
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
                session["valida"]=False

                if not imgPerfil:
                    imgPerfil = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"

            try:
                cur = mysql.connection.cursor()
                cur.execute("""
                    INSERT INTO usuarios
                    (nombre, correo, contraseña, peso, altura, edad, imgPerfil, genero, actividad)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (nombre, correo, contraseña, peso, altura, edad, imgPerfil, genero, actividad))
                mysql.connection.commit()
                cur.close()
            except Exception as e:
                print("ERROR:", e)
                flash("Error al guardar usuario", "error")
                return redirect(url_for("registrosecion", paso=1))

            return redirect(url_for("registrosecion", paso=2))

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
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("index"))

@app.route("/imc/<float:r>", methods=["GET", "POST"])
def imc(r):
    if request.method == "POST":
        peso = float(request.form["peso"])
        altura_cm = float(request.form["altura"])

        altura = altura_cm / 100 
        imc = peso / (altura ** 2)
        imc = round(imc, 2)

        if imc < 18.5:
            flash("Tienes bajo peso. Es recomendable evaluar tu alimentación.", "bajo")
            return redirect(url_for('imc', r = imc))
        elif 18.5 <= imc < 25:
            flash("Tu peso es saludable. ¡Buen trabajo!", "saludable")
            return redirect(url_for('imc', r = imc))
        elif 25 <= imc < 30:
            flash("Tienes sobrepeso. Considera mejorar hábitos de alimentación.", "alto")
            return redirect(url_for('imc', r = imc))
        else:
            flash("Tienes obesidad. Es recomendable acudir con un profesional de la salud.", "obesidad")
            return redirect(url_for('imc', r = imc))

    return render_template("imc.html", r = r)

@app.route("/pci", methods=["GET", "POST"])
def pci():
    peso_ideal = None
    if request.method == "POST":
        sexo = request.form['sexo']
        altura = float(request.form['altura'])

        altura_in = altura / 2.54 
        if sexo == "hombre":
            peso_ideal = 50 + 2.3 * (altura_in - 60)
        else:
            peso_ideal = 45.5 + 2.3 * (altura_in - 60)

        resultado = round(peso_ideal, 2)

        return render_template("idealpeso.html", peso_ideal=resultado)
    
    return render_template("idealpeso.html", peso_ideal=peso_ideal)

@app.route('/api/<string:name>/<int:cal>/<int:pro>/<int:car>', methods=["GET", "POST"])
def api(name,cal,pro,car):
    if request.method == "POST":
        busqueda = request.form['busqueda']
        resp = requests.get(f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={API_KEY}&query={busqueda}")

        if resp.status_code == 200:
            comida_data = resp.json()

            if comida_data.get('foods'):
                alimentos = comida_data['foods']

                listaC = []
                listaS = []

                for x in alimentos:
                    food_data = {
                        'name':x['description'],
                        'calorias':next((n['value'] for n in x['foodNutrients'] if n['nutrientName'] == 'Energy'),None),
                        'proteina':next((n['value'] for n in x['foodNutrients'] if n['nutrientName'] == 'Protein'),None),
                        'carbo':next((n['value'] for n in x['foodNutrients'] if n['unitName'] == 'G'),None)
                    }

                    listaC.append(food_data)

                    if len(listaC) == 4:
                        listaS.append(listaC)
                        listaC = []

                if listaC:
                    listaS.append(listaC)

                return render_template('api.html', name=name, cal=cal, pro=pro, car=car, comidas=listaS)
                

    return render_template('api.html', name=name, cal=cal, pro=pro, car = car)

@app.route('/articulo/<int:art>')
def articulo(art):
    return render_template('articulo.html', art = art)

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/ejercicios/<string:down>')
def ejercicios(down):
    if down == 'entrar':
        return render_template('stayhard.html')
    else:
        carpeta = os.path.join(app.root_path, "static")
        nombre_archivo = "ejercicios.pdf"
        return send_from_directory(carpeta, nombre_archivo, as_attachment=True)

@app.route('/proceso/<int:d>')
def proceso(d):
    if d == 0:
        return render_template('nohechx.html')
    elif d == 1:
        carpeta = os.path.join(app.root_path, "static")
        nombre_archivo = "5 Recetario de Cocina Saludable autor Universidad Veracruzana.pdf"
        return send_from_directory(carpeta, nombre_archivo, as_attachment=True)
    elif d == 2:
        carpeta = os.path.join(app.root_path, "static")
        nombre_archivo = "Principiosde cocina.pdf"
        return send_from_directory(carpeta, nombre_archivo, as_attachment=True)
    elif d == 3:
        carpeta = os.path.join(app.root_path, "static")
        nombre_archivo = "Recetas Económicas.pdf"
        return send_from_directory(carpeta, nombre_archivo, as_attachment=True)

@app.route("/tmb", methods=["GET", "POST"])
def tmb():
    resultado_tmb = None

    if request.method == "POST":
        sexo = request.form.get("sexo")
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        edad = int(request.form.get("edad"))

        if sexo == "hombre":
            tmb_valor = 10 * peso + 6.25 * altura - 5 * edad + 5
        else:
            tmb_valor = 10 * peso + 6.25 * altura - 5 * edad - 161
        resultado_tmb = round(tmb_valor, 2)

        flash(f'Tu Tasa Metabólica Basal(TMB) es de {resultado_tmb}', 'resultado')
        return redirect(url_for('tmb'))
    return render_template('tmb.html')

if __name__ == "__main__":
    app.run(debug=True)