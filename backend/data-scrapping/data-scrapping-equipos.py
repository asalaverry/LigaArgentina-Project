import re
import time
import requests
from bs4 import BeautifulSoup #biblioteca para analizar documentos HTML
from bs4.element import Tag, NavigableString
import pandas as pd

BASE_URL = "https://www.ligaprofesional.ar/clubes/" 
HDRS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def clean_text(s: str) -> str: #Toma una cadena de texto y la limpia 
    if not s:
        return ""
    s = s.replace('“','').replace('”','').replace('"','') # sacar comillas
    s = re.sub(r'\s+', ' ', s)          # espacios múltiples -> 1
    s = re.sub(r'^[\s:–—\-]+', '', s)   # quitar prefijos como ":" o guiones; El .sub se usa para sustituir en un string
    return s.strip()

def parse_kv_from_div(div: Tag) -> dict: 
    """
    Busca todos los <b> o <strong> dentro del div,
    arma pares clave,valor con el texto que sigue
    hasta el próximo <b>/<strong>.
    """
    kv = {}
    strongs = div.find_all(["b", "strong"])

    for s in strongs: #para cada etiqueta <b> o <strong>
        key = s.get_text(" ", strip=True).rstrip(":").strip().lower()  #Limpia el texto que se encuentra en la etiqueta HTML; .get_text extrae el texto de la etiqueta y sus hijos.

        # Acumula el valor hasta el siguiente <strong>/<b>
        value_parts = []
        for elem in s.next_siblings: #iterar sobre los hermanos siguientes del elemento s
            if isinstance(elem, NavigableString): #isinstance comprueba si elem es una cadena navegable (NavigableString)
                value_parts.append(str(elem)) 
            elif isinstance(elem, Tag): #isinstance comprueba si elem es una etiqueta HTML
                if elem.name in ["b", "strong"]: #Comprueba si elem es <b> o <strong>
                    break  #Ya que encontrar otro b o strong significa que encontro la proxima clave
                elif elem.name == "br": #Si es un salto de linea <br>
                    value_parts.append(" ")
                else:
                    value_parts.append(elem.get_text(" ", strip=True)) #si es cualquier otra etiqueta, extrae el texto y lo añade a value_parts
        
        value = clean_text("".join(value_parts)) #guarda el texto limpio en value
        if value: #si value tiene algo...
            kv[key] = value #asigna el valor a la clave correspondiente

    return kv


def extract_club_details(detail_html: str, short_name: str):
    soup = BeautifulSoup(detail_html, "html.parser") #analiza el HTML de detalle del club. "html.parser" es el analizador por defecto de BeautifulSoup

    # 1) Estadio: buscamos el primer elemento text-editor que sigue al H2 del nombre
    estadio = ""
    h2 = soup.find("h2", class_="elementor-heading-title") #busca la primera etiqueta <h2> con la clase "elementor-heading-title"
    if h2:
        #buscar el siguiente bloque que sea un widget de texto
        widget = h2.find_next(lambda tag: tag.name in ("div","p") and "elementor-widget-text-editor" in " ".join(tag.get("class", []) if tag.has_attr("class") else [])) #find_next busca el siguiente elemento que cumpla la condicion dada por la funcion lambda
        if widget:
            texto = widget.get_text(" ", strip=True) 
            estadio = re.sub(r'^[Ee]stadio\s*:?\s*', '', texto).strip() #si viene con la etiqueta "Estadio:" la removemos
        else:
            p = h2.find_next("p") #tomar el siguiente <p> cercano
            if p:
                estadio = p.get_text(" ", strip=True)

    # 2) Nombre completo y demás pares: recorremos todos los bloques relevantes
    kv_total = {}
    #seleccionamos los contenedores que suelen tener las claves/valores (Segun lo que vimos inspeccionando la pagina en el navegador...)
    for div in soup.select("div.elementor-widget-container, div.elementor-widget-text-editor"):
        kv = parse_kv_from_div(div)
        if kv:
            kv_total.update(kv) #Si kv tiene datos, los agrega a kv_total

    nombre_completo = kv_total.get("nombre completo") or kv_total.get("nombre completo:") or kv_total.get("nombre")
    if nombre_completo:
        nombre_completo = clean_text(nombre_completo)
    else:
        nombre_completo = short_name  #si no encontramos nombre completo, usar el corto

    return {
        "estadio": estadio,
        "nombre_completo": nombre_completo
    }


# ---------- Scraping principal ----------
resp = requests.get(BASE_URL, headers=HDRS, timeout=30) #Realiza una solicitud GET a la URL base con los encabezados y un tiempo de espera de 30 segundos
resp.raise_for_status() #Verifica si la solicitud fue exitosa
soup = BeautifulSoup(resp.text, "html.parser") #analiza el HTML de la respuesta

rows = []
for a in soup.select("a.elementor-element"): #soup.select busca elementos en el HTML utilizando selectores CSS
    name_tag = a.find("h2", class_="elementor-heading-title")
    img_tag = a.find("img")
    href = a.get("href")
    if not (name_tag and img_tag and href): #Si no encuentra alguno de los elementos, continuar con el siguiente
        continue

    nombre = name_tag.get_text(strip=True) #Strip=true indica que se eliminarán los espacios en blanco
    logo = img_tag.get("src")

    try:
        d = requests.get(href, headers=HDRS, timeout=30)
        d.raise_for_status()
        details = extract_club_details(d.text, nombre)
        rows.append({
            "nombre": nombre,
            "logo": logo,
            "link": href,
            "estadio": details["estadio"],
            "nombre_completo": details["nombre_completo"]
        })
    except Exception as e: # si falla, guardamos lo mínimo y seguimos
        rows.append({
            "nombre": nombre,
            "logo": logo,
            "link": href,
            "estadio": "",
            "nombre_completo": nombre
        })

    time.sleep(0.6)  #darle un tiempo al servidor

df = pd.DataFrame(rows, columns=["nombre","logo","link","estadio","nombre_completo"]) #Convierte la lista de diccionarios "rows" en un DataFrame de pandas
df.to_csv("clubes.csv", index=False, encoding="utf-8") #convierte el dataframe a csv
print("Guardados:", len(df), "clubes en clubes.csv")

