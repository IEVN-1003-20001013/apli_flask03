from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config

app = Flask(__name__)
conexion = MySQL(app)
CORS(app)


@app.route('/alumnos', methods=['GET'])
def obtener_alumnos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()

        alumnos = []
        for fila in datos:
            alumnos.append({
                'matricula': fila[0],
                'nombre': fila[1],
                'apaterno': fila[2],
                'amaterno': fila[3],
                'correo': fila[4]
            })

        return jsonify({'alumnos': alumnos, 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'exito': False}), 500


@app.route('/alumnos', methods=['POST'])
def insertar_alumno():
    try:
        datos = request.json
        matricula = datos['matricula']
        nombre = datos['nombre']
        apaterno = datos['apaterno']
        amaterno = datos['amaterno']
        correo = datos['correo']

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo)
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (matricula, nombre, apaterno, amaterno, correo))
        conexion.connection.commit()

        return jsonify({'mensaje': 'Alumno agregado correctamente', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'exito': False}), 500


@app.route('/alumnos/<dato>', methods=['GET'])
def buscar_alumno(dato):
    try:
        cursor = conexion.connection.cursor()
        sql = """
            SELECT matricula, nombre, apaterno, amaterno, correo 
            FROM alumnos 
            WHERE matricula = %s 
               OR nombre LIKE %s 
               OR apaterno LIKE %s 
               OR amaterno LIKE %s 
               OR correo LIKE %s
        """
        cursor.execute(sql, (dato, f"%{dato}%", f"%{dato}%", f"%{dato}%", f"%{dato}%"))
        datos = cursor.fetchall()

        if datos:
            alumnos = []
            for fila in datos:
                alumnos.append({
                    'matricula': fila[0],
                    'nombre': fila[1],
                    'apaterno': fila[2],
                    'amaterno': fila[3],
                    'correo': fila[4]
                })
            return jsonify({'alumnos': alumnos, 'mensaje': 'Alumno(s) encontrado(s)', 'exito': True})
        else:
            return jsonify({'mensaje': 'no se encuentra ningun resultado'}), 404

    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'exito': False}), 500


@app.route('/alumnos/<matricula>', methods=['PUT'])
def actualizar_alumno(matricula):
    try:
        datos = request.json
        nombre = datos['nombre']
        apaterno = datos['apaterno']
        amaterno = datos['amaterno']
        correo = datos['correo']

        cursor = conexion.connection.cursor()
        sql = """
            UPDATE alumnos 
            SET nombre=%s, apaterno=%s, amaterno=%s, correo=%s
            WHERE matricula=%s
        """
        cursor.execute(sql, (nombre, apaterno, amaterno, correo, matricula))
        conexion.connection.commit()

        return jsonify({'mensaje': 'Alumno actualizado correctamente', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'exito': False}), 500


@app.route('/alumnos/<matricula>', methods=['DELETE'])
def eliminar_alumno(matricula):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM alumnos WHERE matricula=%s"
        cursor.execute(sql, (matricula,))
        conexion.connection.commit()

        return jsonify({'mensaje': 'Alumno eliminado correctamente', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'exito': False}), 500


def pagina_no_encontrada(error):
    return "<h1>La página que intentas buscar no existe</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)
