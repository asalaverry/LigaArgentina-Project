from flask import Flask
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)   # habilita CORS para todas las rutas

@app.route("/equipos")
def get_equipos():
    conn = sqlite3.connect("LPF.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, logo FROM equipos")
    equipos = [dict(row) for row in cur.fetchall()]
    conn.close()
    return {"equipos": equipos}

@app.route("/equipos/<int:equipo_id>")
def get_equipo(equipo_id):
    conn = sqlite3.connect("LPF.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Info del equipo
    cur.execute("SELECT * FROM equipos WHERE id = ?", (equipo_id,))
    equipo = dict(cur.fetchone())

    # Jugadores del equipo
    cur.execute("SELECT nombre, posicion, nacionalidad, numero, edad FROM jugadores WHERE equipo_id = ?", (equipo_id,))
    jugadores = [dict(row) for row in cur.fetchall()]

    conn.close()

    return {"equipo": equipo, "jugadores": jugadores}


if __name__ == "__main__":
    app.run(debug=True)

