import os
import io
import logging
import requests
import psycopg2
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import tqdm

logging.basicConfig(level=logging.INFO)

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_xml_data():
    response = requests.get("https://rejestry.ezdrowie.gov.pl/api/rpl/medicinal-products/public-pl-report/6.0.0/overall.xml")
    NAMESPACE = {"ns": "http://rejestry.ezdrowie.gov.pl/rpl/eksport-danych-v6.0.0"}
    xml_file = io.BytesIO(response.content)
    tree = ET.ElementTree(file=xml_file)
    root = tree.getroot()
    total_products = len(list(root.iter(f'{{{NAMESPACE["ns"]}}}produktLeczniczy')))
    logging.info(f"Total products: {total_products}")

    return xml_file, NAMESPACE, total_products

def get_psql_cursor():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connected to the database successfully!")
        return conn.cursor(), conn
    except Exception as e:
        print("Error while connecting to PostgreSQL:", e)
        return None, None

# CREATE TABLE leki (
#     id_produktu SERIAL PRIMARY KEY,
#     nazwa_produktu VARCHAR(255) NOT NULL,
#     rodzaj_preparatu VARCHAR(255), -- ludzki, zwierzęcy
#     nazwa_powszechna VARCHAR(255),
#     moc VARCHAR(255),
#     nazwa_postaci_farmaceutycznej VARCHAR(255),
#     podmiot_odpowiedzialny VARCHAR(255), 
#     typ_procedury VARCHAR(255),
#     waznosc_pozwolenia VARCHAR(255),
#     podstawa_prawna VARCHAR(255),
#     zakaz_stosowania_zwierzeta VARCHAR(255),
#     ulotka VARCHAR(255),
#     charakterystyka VARCHAR(255),
#     kod_ATC VARCHAR(50),
#     droga_podania VARCHAR(255),
#     nazwa_wytwórcy_importera VARCHAR(255),
#     kraj_wytwórcy_importera VARCHAR(100)
# );
def main():
    xml_file, NAMESPACE, total_products = get_xml_data()
    xml_file.seek(0)
    with tqdm(total=total_products, desc="Przetwarzenie XML", unit="produktów") as pbar:
        for event, elem in ET.iterparse(xml_file, events=('start', 'end')):
            # if i % 10 == 0:
            #     os.system('clear')
            # Process the product when we hit the 'end' event for a product
            if event == 'end' and f"{{{NAMESPACE['ns']}}}produktLeczniczy" in elem.tag:
                characteristics = ""
                # Pierwszy segement
                id_produktu = elem.get("id")
                nazwa_produktu = elem.get("nazwaProduktu")
                rodzaj_preparatu = elem.get("rodzajPreparatu")
                nazwa_powszechna = elem.get("nazwaPowszechnieStosowana")
                moc = elem.get("moc")
                nazwa_postaci_farmaceutycznej = elem.get("nazwaPostaciFarmaceutycznej")
                podmiot_odpowiedzialny = elem.get("podmiotOdpowiedzialny")
                typ_procedury = elem.get("typProcedury")
                waznosc_pozwolenia = elem.get("waznoscPozwolenia")
                podstawa_prawna = elem.get("podstawaPrawna")
                zakaz_stosowania_zwierzeta = elem.get("zakazStosowaniaUZwierzat")
                ulotka = elem.get("ulotka")
                charakterystyka = elem.get("charakterystyka")
                
                # Drugi segment
                kod_atc = elem.find('.//ns:kodyATC/ns:kodATC', NAMESPACE)
                kod_atc = kod_atc.text if kod_atc is not None else None
                droga_podania = elem.find('.//ns:drogiPodania/ns:drogaPodania', NAMESPACE)
                droga_podania = droga_podania.find("drogaPodaniaNazwa") if droga_podania is not None else None

                # Trzeci segment
                nazwa_wytwórcy_importera = elem.find('.//ns:daneOWytworcy/ns:wytworcy', NAMESPACE)
                kraj_wytwórcy_importera = nazwa_wytwórcy_importera.find("krajWytworcyImportera") if nazwa_wytwórcy_importera is not None else None
                nazwa_wytwórcy_importera = nazwa_wytwórcy_importera.find("nazwaWytworcyImportera") if nazwa_wytwórcy_importera is not None else None

                logging.info(f"Parsed XML for ID: {id_produktu}")
                
    return 0

if __name__ == "__main__":
    main()