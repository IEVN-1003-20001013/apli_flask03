from wtforms import form
from flask import Flask, render_template, request
import math
import forms

from flask import make_response, jsonify
import json

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

@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
    mat = ""
    nom = ""
    ape = ""
    em = ""
    datos = {}
    alumnos_clase = forms.UserForm(request.form)

    if request.method == 'POST' and alumnos_clase.validate:
        
        mat = alumnos_clase.matricula.data
        nom = alumnos_clase.nombre.data
        ape = alumnos_clase.apellido.data
        em = alumnos_clase.correo.data

        nuevo = {"matricula": mat, "nombre": nom, "apellido": ape, "correo": em}

        
        datos_cookie = request.cookies.get('estudiantes')
        if datos_cookie:
            lista_estudiantes = json.loads(datos_cookie)
        else:
            lista_estudiantes = []

        
        lista_estudiantes.append(nuevo)

        
        response = make_response(render_template(
            'alumnos.html',
            form=alumnos_clase,
            mat=mat,
            nom=nom,
            ape=ape,
            em=em
        ))
        response.set_cookie('estudiantes', json.dumps(lista_estudiantes))
        return response

    return render_template('alumnos.html', form=alumnos_clase)


@app.route('/cookie')
def get_cookie():
    datos_str = request.cookies.get('estudiantes')
    if not datos_str:
        return render_template('cookie.html', datos=None)

    datos = json.loads(datos_str)
    return render_template('cookie.html', datos=datos)





@app.route('/figuras', methods=['GET', 'POST'])
def figuras():
    area = None
    figura = ""
    mensaje = ""

    if request.method == 'POST':
        figura = request.form.get('figura')
        accion = request.form.get('accion') 

        if accion == "Calcular":
            v1 = request.form.get('valor1', type=float)
            v2 = request.form.get('valor2', type=float)

            if figura == 'triangulo':
                if v1 is not None and v2 is not None:
                    area = (v1 * v2) / 2
                    mensaje = f"El área del triángulo es {area}"
                else:
                    mensaje = "Ingrese base y altura."
            elif figura == 'rectangulo':
                if v1 is not None and v2 is not None:
                    area = v1 * v2
                    mensaje = f"El área del rectángulo es {area}"
                else:
                    mensaje = "Ingrese base y altura."
            elif figura == 'circulo':
                if v1 is not None:
                    area = math.pi * (v1 ** 2)
                    mensaje = f"El área del círculo es {area:.2f}"
                else:
                    mensaje = "Ingrese el radio."
            elif figura == 'pentagono':
                if v1 is not None and v2 is not None:
                    area = (v1 * v2) / 2
                    mensaje = f"El área del pentágono es {area}"
                else:
                    mensaje = "Ingrese perímetro y apotema."

    return render_template('figuras.html', area=area, figura=figura, mensaje=mensaje)

@app.route('/pizzas', methods=['GET', 'POST'])
def pizzas():
    cliente_form = forms.ClienteForm(request.form)

    pizzas_lista = []
    ventas_lista = []
    total_general = 0

    cookie_pizzas = request.cookies.get('pizzas')
    if cookie_pizzas:
        pizzas_lista = json.loads(cookie_pizzas)

    cookie_ventas = request.cookies.get('ventas')
    if cookie_ventas:
        ventas_lista = json.loads(cookie_ventas)
        total_general = sum(v['total'] for v in ventas_lista)

    
    if 'agregar' in request.form:
        tamano = request.form.get('tamano')
        ingredientes = request.form.getlist('ingredientes')
        cantidad = int(request.form.get('cantidad', 1))

        precios = {'chica': 40, 'mediana': 80, 'grande': 120}
        
        subtotal = precios[tamano.lower()] * cantidad + len(ingredientes) * 10 * cantidad

        nueva_pizza = {
            'tamano': tamano.capitalize(),
            'ingredientes': ', '.join([i.capitalize() for i in ingredientes]) if ingredientes else 'Ninguno',
            'cantidad': cantidad,
            'subtotal': subtotal
        }
        pizzas_lista.append(nueva_pizza)

        response = make_response(render_template('pizzas.html',
                                                 cliente_form=cliente_form,
                                                 pizzas=pizzas_lista,
                                                 ventas=ventas_lista,
                                                 total_general=total_general))
        response.set_cookie('pizzas', json.dumps(pizzas_lista))
        return response

    
    if 'quitar' in request.form:
        index = int(request.form['quitar'])
        if 0 <= index < len(pizzas_lista):
            del pizzas_lista[index]

        response = make_response(render_template('pizzas.html',
                                                 cliente_form=cliente_form,
                                                 pizzas=pizzas_lista,
                                                 ventas=ventas_lista,
                                                 total_general=total_general))
        response.set_cookie('pizzas', json.dumps(pizzas_lista))
        return response

    
    if 'terminar' in request.form and cliente_form.validate():
        total = sum(p['subtotal'] for p in pizzas_lista)
        nombre = cliente_form.nombre.data
        direccion = cliente_form.direccion.data
        telefono = cliente_form.telefono.data

        venta = {
            'nombre': nombre,
            'direccion': direccion,
            'telefono': telefono,
            'total': total
        }

        ventas_lista.append(venta)
        total_general = sum(v['total'] for v in ventas_lista)

        response = make_response(render_template('pizzas.html',
                                                 cliente_form=cliente_form,
                                                 pizzas=[],
                                                 ventas=ventas_lista,
                                                 total_general=total_general))
        response.set_cookie('ventas', json.dumps(ventas_lista))
        response.set_cookie('pizzas', json.dumps([]))
        return response

    return render_template('pizzas.html',
                           cliente_form=cliente_form,
                           pizzas=pizzas_lista,
                           ventas=ventas_lista,
                           total_general=total_general)

if __name__ == '__main__':
    app.run(debug=True)
