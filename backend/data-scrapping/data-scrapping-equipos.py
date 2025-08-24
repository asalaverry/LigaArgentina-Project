import re
import time
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import pandas as pd

BASE_URL = "https://www.ligaprofesional.ar/clubes/"
HDRS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def clean_text(s: str) -> str:
    if not s:
        return ""
    s = s.replace('“','').replace('”','').replace('"','')
    s = re.sub(r'\s+', ' ', s)          # espacios múltiples -> 1
    s = re.sub(r'^[\s:–—\-]+', '', s)   # quitar prefijos como ":" o guiones
    return s.strip()

def parse_kv_from_div(div: Tag) -> dict:
    """
    Busca todos los <b> o <strong> dentro del div,
    arma pares clave -> valor con el texto que sigue
    hasta el próximo <b>/<strong>.
    """
    kv = {}
    strongs = div.find_all(["b", "strong"])
    
    for s in strongs:
        key = s.get_text(" ", strip=True).rstrip(":").strip().lower()

        # Acumula el valor hasta el siguiente <strong>/<b>
        value_parts = []
        for elem in s.next_siblings:
            if isinstance(elem, NavigableString):
                value_parts.append(str(elem))
            elif isinstance(elem, Tag):
                if elem.name in ["b", "strong"]:
                    break  # 👈 cortamos en la próxima clave
                elif elem.name == "br":
                    value_parts.append(" ")
                else:
                    value_parts.append(elem.get_text(" ", strip=True))
        
        value = clean_text("".join(value_parts))
        if value:
            kv[key] = value
    
    return kv


def extract_club_details(detail_html: str, short_name: str):
    soup = BeautifulSoup(detail_html, "html.parser")

    # 1) Estadio: buscamos el primer elemento text-editor que sigue al H2 del nombre
    estadio = ""
    h2 = soup.find("h2", class_="elementor-heading-title")
    if h2:
        # buscar el siguiente bloque que sea un widget de texto
        widget = h2.find_next(lambda tag: tag.name in ("div","p") and "elementor-widget-text-editor" in " ".join(tag.get("class", []) if tag.has_attr("class") else []))
        if widget:
            texto = widget.get_text(" ", strip=True)
            # si viene con la etiqueta "Estadio:" la removemos
            estadio = re.sub(r'^[Ee]stadio\s*:?\s*', '', texto).strip()
        else:
            # fallback: tomar el siguiente <p> cercano
            p = h2.find_next("p")
            if p:
                estadio = p.get_text(" ", strip=True)

    # 2) Nombre completo y demás pares: recorremos todos los bloques relevantes
    kv_total = {}
    # seleccionamos los contenedores que suelen tener las claves/valores
    for div in soup.select("div.elementor-widget-container, div.elementor-widget-text-editor"):
        kv = parse_kv_from_div(div)
        if kv:
            kv_total.update(kv)  # últimos valores reemplazan anteriores

    nombre_completo = kv_total.get("nombre completo") or kv_total.get("nombre completo:") or kv_total.get("nombre")
    if nombre_completo:
        nombre_completo = clean_text(nombre_completo)
    else:
        nombre_completo = short_name  # fallback garantizado

    return {
        "estadio": estadio,
        "nombre_completo": nombre_completo
    }


# ---------- Scraping principal ----------
resp = requests.get(BASE_URL, headers=HDRS, timeout=30)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

rows = []
for a in soup.select("a.elementor-element"):
    name_tag = a.find("h2", class_="elementor-heading-title")
    img_tag = a.find("img")
    href = a.get("href")
    if not (name_tag and img_tag and href):
        continue

    nombre = name_tag.get_text(strip=True)
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
    except Exception as e:
        # si falla, guardamos lo mínimo y seguimos
        rows.append({
            "nombre": nombre,
            "logo": logo,
            "link": href,
            "estadio": "",
            "nombre_completo": nombre
        })

    time.sleep(0.6)  # ser amables con el servidor

df = pd.DataFrame(rows, columns=["nombre","logo","link","estadio","nombre_completo"])
df.to_csv("clubes.csv", index=False, encoding="utf-8")
print("Guardados:", len(df), "clubes en clubes.csv")

