from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "clave-secreta"

session = {
    "alimento":"",
    "grasas":"",
    "proteinas":"",
    "carbohidratos":""
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tabla')
def tabla():
    return render_template('tabla.html')

@app.route('/registro', methods = ['POST','GET'])
def registro():
    if request.method == 'POST':
        alimento = request.form['alimento']
        grasas = request.form['grasas']
        proteinas = request.form['proteinas']
        carbohidratos = request.form['carbohidratos']
        
        if alimento != "" and grasas != "" and proteinas != "" and carbohidratos != "":
            session["alimento"] = alimento
            session["grasas"] = grasas
            session["proteinas"] = proteinas
            session["carbohidratos"] = carbohidratos
        
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)