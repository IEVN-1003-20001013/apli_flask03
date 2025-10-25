from flask import Flask, render_template, request



app = Flask(__name__)


@app.route('/')
def hello_world():
    return '¡Hola, señor!'

@app.route('/about')
def about():
    return "this is about page"

@app.route('/user/<string:user>')
def user(user):
    return "hola: " + user

@app.route("/numero/<int:n>")
def numero(n):
    return "Número: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "ID: {} nombre: {}".format(id, username)

@app.route("/usam/<float:n1>/<float:n2>")
def func(n1, n2):
    return "La suma es: {}".format(n1 + n2)

@app.route("/prueba")
def prueba():
    return """
    <h1>Prueba</h1>
    <p>Carpio</p>
    <h2>una lista</h2>
    <ul>
        <li>1</li>
        <li>2</li>
        <li>3</li>
    </ul>
    """
@app.route("/index") 
def index():
    return render_template ("index.html")  

@app.route("/operaciones", methods=['GET', 'POST']) 
def operaciones():
   if request.method=='POST':
       x1=request.form.get('x1')
       x2=request.form.get('x2')
       resultado=x1+x2
       return render_template("operaciones.html", resultado=resultado)
   return render_template('operaciones.html')
   
@app.route("/distancia") 
def distancia():
    return render_template ("distancia.html")  

@app.route("/layuot") 
def layuot():
    return render_template ("layuot.html")  

@app.route('/utl')
def utl():
    titulo = "IEVN1003"
    listado = ["opera 1", "opera 2", "opera 3", "opera 4"]
    return render_template("index.html", titulo=titulo, listado=listado)

if __name__ == '__main__':
    app.run(debug=True)
