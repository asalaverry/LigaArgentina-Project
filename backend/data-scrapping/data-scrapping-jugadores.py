import time
import pandas as pd
from bs4 import BeautifulSoup #biblioteca para analizar documentos HTML
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ----------------------------------------
# Scraping de jugadores
# ----------------------------------------
def scrape_players(url, equipo):
    options = Options()
    options.add_argument("--headless")  # no abre ventana
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)  # esperar que cargue el JS

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    data = []
    sections = soup.select("div.Opta-Squad > h4")
    for section in sections:
        posicion = section.get_text(strip=True)  # Arqueros, Defensores, etc.
        players_div = section.find_next("div", class_="Opta-Flex")
        for player in players_div.select("div.Opta-Card"):
            nombre = player.select_one(".Opta-Player-Name").get_text(strip=True)
            nacionalidad = player.select_one(".Opta-Country").get_text(strip=True)

            # Buscar edad y número de camiseta
            detalles = player.select(".Opta-Details p")
            edad, numero = None, None
            for d in detalles:
                t = d.get_text()
                if "Edad" in t:
                    edad = t.replace("Edad:", "").strip()
                if "Nº" in t:
                    numero = t.split(":")[-1].strip()

            data.append({
                "Equipo": equipo,
                "Nombre": nombre,
                "Posición": posicion,
                "Nacionalidad": nacionalidad,
                "Número": numero,
                "Edad": edad
            })

    return data


# ----------------------------------------
# MAIN: recorrer todos los clubes
# ----------------------------------------
def main():
    # CSV de clubes que generaste con tu otro script
    clubes = pd.read_csv("clubes.csv")  

    all_players = []
    for _, row in clubes.iterrows():
        equipo = row["nombre"]
        url = row["link"]
        print(f"Scrapeando {equipo} ...")

        try:
            players = scrape_players(url, equipo)
            all_players.extend(players)
        except Exception as e:
            print(f"❌ Error con {equipo}: {e}")

        time.sleep(2)  # ser amables con el servidor

    df = pd.DataFrame(all_players, columns=["Equipo","Nombre","Posición","Nacionalidad","Número","Edad"])
    df.to_csv("planteles_completos.csv", index=False, encoding="utf-8-sig")
    print(f"\n✅ Guardado planteles_completos.csv con {len(df)} jugadores")

if __name__ == "__main__":
    main()