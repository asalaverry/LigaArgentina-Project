from flask import Flask
from flask_cors import CORS
import sqlite3

app = Flask(__name__) #Creamos instancia de la app web
CORS(app)   # habilita CORS para todas las rutas

@app.route("/equipos") #Definimos la ruta equipos
def get_equipos():
    conn = sqlite3.connect("LPF.db") #Se conecta a la base de datos
    conn.row_factory = sqlite3.Row #Configura el cursor para que devuelva filas como diccionarios
    cur = conn.cursor()
    
    cur.execute("SELECT id, nombre, logo FROM equipos") #Ejecuta la consulta SQL
    equipos = [dict(row) for row in cur.fetchall()] #Convierte las filas en diccionarios
    conn.close()
    
    return {"equipos": equipos} #Retorna la lista de equipos en JSON

@app.route("/equipos/<int:equipo_id>") #Define ruta dinamica, que cambia segun el id del equipo
def get_equipo(equipo_id):
    conn = sqlite3.connect("LPF.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM equipos WHERE id = ?", (equipo_id,)) # Obtiene la info del equipo
    equipo = dict(cur.fetchone()) #Convierte la fila en un diccionario

    cur.execute("SELECT nombre, posicion, nacionalidad, numero, edad FROM jugadores WHERE equipo_id = ?", (equipo_id,))
    jugadores = [dict(row) for row in cur.fetchall()]
    conn.close()

    return {"equipo": equipo, "jugadores": jugadores} #Retorna el objeto JSON de equipo y jugadores


if __name__ == "__main__": 
    app.run(debug=True)

