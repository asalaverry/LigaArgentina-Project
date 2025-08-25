import sqlite3
import csv

# Conexión a la base (crea LPF.db si no existe)
conn = sqlite3.connect("LPF.db")
cur = conn.cursor() #crea un objeto "cursor", que es esencial para interactuar con una base de datos

# Crear tablas
cur.execute("""
CREATE TABLE IF NOT EXISTS equipos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    logo TEXT,
    estadio TEXT,
    nombre_completo TEXT
)
""") #Ejecuta este codigo SQL

cur.execute("""
CREATE TABLE IF NOT EXISTS jugadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipo_id INTEGER,
    nombre TEXT,
    posicion TEXT,
    nacionalidad TEXT,
    numero INTEGER,
    edad INTEGER,
    FOREIGN KEY (equipo_id) REFERENCES equipos(id)
)
""")

# --- Insertar equipos ---
equipos_map = {}  # Diccionario para mapear nombre → id

with open("clubes.csv", "r", encoding="utf-8") as f: #Abrir el archivo clubes.csv en modo lectura
    reader = csv.DictReader(f) #Crea un lector de diccionarios. Lee cada fila del csv como un diccionario. 
    for row in reader:
        cur.execute("""
            INSERT INTO equipos (nombre, logo, estadio, nombre_completo)
            VALUES (?, ?, ?, ?)
        """, (row["nombre"], row["logo"], row["estadio"], row["nombre_completo"]))
        equipos_map[row["nombre"]] = cur.lastrowid  # Guardar id del equipo insertado

# --- Insertar jugadores ---
with open("planteles_completos.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        equipo_id = equipos_map.get(row["\ufeffEquipo"])  # Buscar el id del equipo *Equipo esta escrito asi, porque lo vimos con el reader... Tema de formato csv
        if equipo_id:  # Solo si el equipo existe en la tabla equipos
            cur.execute("""
                INSERT INTO jugadores (equipo_id, nombre, posicion, nacionalidad, numero, edad)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (equipo_id, row["Nombre"], row["Posición"], row["Nacionalidad"],
                  row["Número"], row["Edad"]))

conn.commit() #Hace el commit
conn.close()

print("✅ Datos cargados correctamente en LPF.db")
