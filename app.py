from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Conexión Segura
try:
    client = MongoClient(os.environ.get("MONGO_URI"), serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client['gestion_sena']
    coleccion = db['aprendices']
    print("✅ Conexión a MongoDB exitosa")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    coleccion = None

@app.route('/')
def index():
    try:
        data = list(coleccion.find())
        return render_template('index.html', aprendices=data)
    except:
        return "Error de base de datos"

@app.route('/registrar', methods=['POST'])
def registrar():
    # Usamos request.form para recibir los datos del HTML que te di
    nuevo_aprendiz = {
        "nombre": request.form.get("nombre"),
        "correo": request.form.get("correo"),
        "nivel": request.form.get("nivel"),
        "centro": request.form.get("centro") if request.form.get("centro") != "OTRO" else request.form.get("otro_centro"),
        "programa": request.form.get("programa"),
        "ficha": request.form.get("ficha"),
        "trimestre": request.form.get("trimestre")
    }
    coleccion.insert_one(nuevo_aprendiz)
    return redirect(url_for('index'))

@app.route('/eliminar/<id>')
def eliminar(id):
    coleccion.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)