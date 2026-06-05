from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os

app = Flask(__name__)
app.secret_key = "clave_secreta_sena" # Necesaria para los mensajes flash

# URI de conexión: En local usa localhost, en Render usará la variable de entorno
MONGO_URI = os.environ.get('MONGO_URI', "mongodb://localhost:27017/")

# Intentamos conectar a MongoDB Atlas
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client['gestion_academica']
    coleccion_estudiantes = db['estudiantes']
except Exception as e:
    print(f"Error inicial de conexión: {e}")

@app.route('/')
def index():
    try:
        # 3. Consultar todos los estudiantes registrados
        estudiantes = list(coleccion_estudiantes.find())
        return render_template('index.html', estudiantes=estudiantes)
    # 4. Controlar excepciones (Fallo de BD)
    except ServerSelectionTimeoutError:
        return render_template('error.html', mensaje="El servidor de base de datos no responde. Verifica la conexión a MongoDB Atlas.")
    except Exception as e:
        return render_template('error.html', mensaje=f"Error inesperado: {str(e)}")

@app.route('/registrar', methods=['POST'])
def registrar():
    try:
        # 1. Recibir datos
        documento = request.form.get('documento')
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        programa = request.form.get('programa')
        ficha = request.form.get('ficha')
        
        # 2. Validar datos registrados
        if not documento or not nombre or not correo or not programa or not ficha:
             flash("Todos los campos son obligatorios", "danger")
             return redirect(url_for('index'))

        nuevo_estudiante = {
            "documento": documento,
            "nombre": nombre,
            "correo": correo,
            "programa": programa,
            "ficha": ficha
        }
        
        coleccion_estudiantes.insert_one(nuevo_estudiante)
        flash("Estudiante registrado exitosamente", "success")
        return redirect(url_for('index'))
        
    except ServerSelectionTimeoutError:
        return render_template('error.html', mensaje="Error crítico: Pérdida de conexión con MongoDB Atlas al intentar guardar el registro.")
    except Exception as e:
        return render_template('error.html', mensaje=f"Ha ocurrido un error al registrar: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)