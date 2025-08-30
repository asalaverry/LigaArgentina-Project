import sqlite3

def obtener_nacionalidades_unicas(nombre_db):
    """
    Obtiene y retorna una lista de todas las nacionalidades únicas
    de los jugadores en la base de datos.
    """
    nacionalidades = []
    conn = None
    try:
        conn = sqlite3.connect(nombre_db)
        cursor = conn.cursor()

        # Consulta SQL para seleccionar valores únicos de la columna 'nacionalidad'
        query = "SELECT DISTINCT nacionalidad FROM jugadores;"

        cursor.execute(query)

        # Obtener todos los resultados
        resultados = cursor.fetchall()

        # Iterar sobre los resultados e imprimirlos
        for fila in resultados:
            nacionalidad = fila[0]
            if nacionalidad:  # Opcional: para evitar imprimir valores nulos o vacíos
                nacionalidades.append(nacionalidad)

    except sqlite3.Error as e:
        print(f"Ocurrió un error de SQLite: {e}")
        nacionalidades = []  # Devolver una lista vacía en caso de error
    finally:
        if conn:
            conn.close()

    return nacionalidades

if __name__ == "__main__":
    nombre_de_mi_db = 'LPF.db'
    
    nacionalidades_encontradas = obtener_nacionalidades_unicas(nombre_de_mi_db)
    
    if nacionalidades_encontradas:
        print("Nacionalidades encontradas en la base de datos:")
        for nac in nacionalidades_encontradas:
            print(nac)
    else:
        print("No se encontraron nacionalidades o la base de datos está vacía/no existe.")