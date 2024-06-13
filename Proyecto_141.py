import requests
from bs4 import BeautifulSoup
import pandas as pd


START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars"


headers = ["Nombre", "Magnitud_Visual", "Distancia (ly)", "Tipo_Espectral"]


star_data = []

headers_req = {"User-Agent": "Mozilla/5.0"}

try:
    response = requests.get(START_URL, headers=headers_req)  
    response.raise_for_status()  
except requests.exceptions.RequestException as e:
    print(f"Error al obtener la página: {e}")
    exit()


soup = BeautifulSoup(response.text, "html.parser")


table = soup.find("table", {"class": ["wikitable", "sortable"]})

if table is None:
    print("No se encontró la tabla.")
    exit()


for row in table.find_all("tr")[1:]:
    cells = row.find_all("td")
    if len(cells) >= 5: 
        star = [
            cells[2].find('a').text.strip(), 
            cells[1].text.strip(),
            cells[4].text.strip(),
            cells[5].text.strip(),
        ]
        star_data.append(star)


star_df = pd.DataFrame(star_data, columns=headers)


star_df.to_csv("brightest_stars.csv", index=False)

print("Datos extraídos y guardados en brightest_stars.csv")

