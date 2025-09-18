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
    logging.info("Fetching XML data...")
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
def main(cur, conn):
    xml_file, NAMESPACE, total_products = get_xml_data()
    xml_file.seek(0)

    with tqdm.tqdm(total=total_products, desc="Przetwarzenie XML", unit="produktów") as pbar:
        for event, elem in ET.iterparse(xml_file, events=('start', 'end')):
            if event == 'end' and f"{{{NAMESPACE['ns']}}}produktLeczniczy" in elem.tag:
                id_produktu = None
                nazwa_produktu = None
                moc = None
                ulotka = None
                charakterystyka = None
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
                droga_podania = droga_podania.get("drogaPodaniaNazwa") if droga_podania is not None else None

                # Trzeci segment
                wytworcy_elem = elem.find('.//ns:daneOWytworcy/ns:wytworcy', NAMESPACE)
                if wytworcy_elem is not None:
                    nazwa_wytwórcy_importera = wytworcy_elem.get("nazwaWytworcyImportera")
                    kraj_wytwórcy_importera = wytworcy_elem.get("krajWytworcyImportera")
                else:
                    nazwa_wytwórcy_importera = None
                    kraj_wytwórcy_importera = None
                logging.info(f"Parsed XML for ID: {id_produktu}")

                # Wstaw do tabeli leki
                if False:
                    cur.execute("""--sql 
                                SELECT insert_leki(
                                    %(id_produktu)s,
                                    %(nazwa_produktu)s,
                                    %(rodzaj_preparatu)s,
                                    %(nazwa_powszechna)s,
                                    %(moc)s,
                                    %(nazwa_postaci_farmaceutycznej)s,
                                    %(podmiot_odpowiedzialny)s,
                                    %(typ_procedury)s,
                                    %(waznosc_pozwolenia)s,
                                    %(podstawa_prawna)s,
                                    %(zakaz_stosowania_zwierzeta)s,
                                    %(ulotka)s,
                                    %(charakterystyka)s,
                                    %(kod_atc)s,
                                    %(droga_podania)s,
                                    %(nazwa_wytwórcy_importera)s,
                                    %(kraj_wytwórcy_importera)s
                                );
                                """, {
                                    'id_produktu': id_produktu,
                                    'nazwa_produktu': nazwa_produktu,
                                    'rodzaj_preparatu': rodzaj_preparatu,
                                    'nazwa_powszechna': nazwa_powszechna,
                                    'moc': moc,
                                    'nazwa_postaci_farmaceutycznej': nazwa_postaci_farmaceutycznej,
                                    'podmiot_odpowiedzialny': podmiot_odpowiedzialny,
                                    'typ_procedury': typ_procedury,
                                    'waznosc_pozwolenia': waznosc_pozwolenia,
                                    'podstawa_prawna': podstawa_prawna,
                                    'zakaz_stosowania_zwierzeta': zakaz_stosowania_zwierzeta,
                                    'ulotka': ulotka,
                                    'charakterystyka': charakterystyka,
                                    'kod_atc': kod_atc,
                                    'droga_podania': droga_podania,
                                    'nazwa_wytwórcy_importera': nazwa_wytwórcy_importera,
                                    'kraj_wytwórcy_importera': kraj_wytwórcy_importera
                                    })
                else:
                    print("-----------------------------")
                    print(f"id_produktu: {id_produktu}\n nazwa_produktu: {nazwa_produktu}\n rodzaj_preparatu: {rodzaj_preparatu}\n nazwa_powszechna: {nazwa_powszechna}\n moc: {moc}\n nazwa_postaci_farmaceutycznej: {nazwa_postaci_farmaceutycznej}\n podmiot_odpowiedzialny: {podmiot_odpowiedzialny}\n typ_procedury: {typ_procedury}\n waznosc_pozwolenia: {waznosc_pozwolenia}\n podstawa_prawna: {podstawa_prawna}\n zakaz_stosowania_zwierzeta: {zakaz_stosowania_zwierzeta}\n ulotka: {ulotka}\n charakterystyka: {charakterystyka}\n kod_atc: {kod_atc}\n droga_podania: {droga_podania}\n nazwa_wytwórcy_importera: {nazwa_wytwórcy_importera}\n kraj_wytwórcy_importera: {kraj_wytwórcy_importera}\n")
                    
                    ##############################################
                    # Ekstrakcja substancji czynnych
                    # CREATE TABLE IF NOT EXISTS substancje
                    # (   id_substancji SERIAL PRIMARY KEY,
                    #     id_produktu integer NOT NULL,
                    #     FOREIGN KEY (id_produktu) REFERENCES leki(id_produktu) ON DELETE CASCADE,
                    #     nazwa_substancji VARCHAR(255),
                    #     ilosc_substancji VARCHAR(100),
                    #     jednostka_miary_ilosci_substancji VARCHAR(100),
                    #     ilosc_preparatu VARCHAR(100),
                    #     jednostka_miar_ilosci_preparatu VARCHAR(50),
                    #     informacje_dodatkowe TEXT
                    # );

                    active_substances_data = []

                    for substance in elem.findall('.//ns:substancjeCzynne/ns:substancjaCzynna', NAMESPACE):
                        active_substances_data.append({
                            'id_produktu': id_produktu,  # Link the active substance to the product
                            'nazwa_substancji': substance.get('nazwaSubstancji'),
                            'ilosc_substancji': substance.get('iloscSubstancji'),
                            'jednostka_miary_ilosci_substancji': substance.get('jednostkaMiaryIlosciSubstancji'),
                            'ilosc_preparatu': substance.get('iloscPreparatu'),
                            'jednostka_miar_ilosci_preparatu': substance.get('jednostkaMiaryIlosciPreparatu'),
                            'informacje_dodatkowe': substance.get('informacje_dodatkowe')
                        })

                    for substance in active_substances_data:
                        if False:
                            cur.execute("""--sql
                                        SELECT insert_substancje(
                                            %(id_produktu)s,
                                            %(nazwa_substancji)s,
                                            %(ilosc_substancji)s,
                                            %(jednostka_miary_ilosci_substancji)s,
                                            %(ilosc_preparatu)s,
                                            %(jednostka_miar_ilosci_preparatu)s,
                                            %(informacje_dodatkowe)s
                                        );
                                        """, substance)
                        else:
                            print(substance)
                    
                    # Ekstrakcja opakowań
                #     CREATE TABLE opakowania (
                #     id_opakowania SERIAL PRIMARY KEY,
                #     id_produktu integer NOT NULL,
                #     FOREIGN KEY (id_produktu) REFERENCES leki(id_produktu) ON DELETE CASCADE,
                #     kod_gtin VARCHAR(50),
                #     kategoria_dostepnosci VARCHAR(255),
                #     skasowane VARCHAR(50),
                #     numerEU VARCHAR(50),
                #     dystrybutor_rownolegly VARCHAR(255),
                #     id_xml VARCHAR(10),
                #     liczba_opakowan VARCHAR(50),
                #     rodzaj_opakowania VARCHAR(50),
                #     pojemnosc VARCHAR(50),
                #     jednostka_pojemnosci VARCHAR(50),
                #     informacje_dodatkowe VARCHAR(255)
                # );
                    opakowania = []
                    for opakowanie in elem.findall('.//ns:opakowania/ns:opakowanie', NAMESPACE):
                        jednostka_opakowania = opakowanie.find('.//ns:jednostkiOpakowania/ns:jednostkaOpakowania', NAMESPACE)

                        opakowania.append({
                            'id_produktu': id_produktu,
                            'kod_gtin': opakowanie.get('kodGTIN'),
                            'kategoria_dostepnosci': opakowanie.get('kategoriaDostepnosci'),
                            'skasowane': opakowanie.get('skasowane'),
                            'numerEU': opakowanie.get('numerEu'),

                            'dystrybutor_rownolegly': opakowanie.get('dystrybutorRownolegly'),
                            'id_xml': opakowanie.get('id'),

                            'liczba_opakowan': jednostka_opakowania.get('liczbaOpakowan') if jednostka_opakowania is not None else None,
                            'rodzaj_opakowania': jednostka_opakowania.get('rodzajOpakowania') if jednostka_opakowania is not None else None,
                            'pojemnosc': jednostka_opakowania.get('pojemnosc') if jednostka_opakowania is not None else None,
                            'jednostka_pojemnosci': jednostka_opakowania.get('jednostkaPojemnosci') if jednostka_opakowania is not None else None,
                            'informacje_dodatkowe': jednostka_opakowania.get('informacjeDodatkowe') if jednostka_opakowania is not None else None
                        })

                    for opakowanie in opakowania:
                        if False:
                            cur.execute("""--sql
                                        SELECT insert_opakowania(
                                            %(id_produktu)s,
                                            %(kod_gtin)s,
                                            %(kategoria_dostepnosci)s,
                                            %(skasowane)s,
                                            %(numerEU)s,
                                            %(dystrybutor_rownolegly)s,
                                            %(id_xml)s,
                                            %(liczba_opakowan)s,
                                            %(rodzaj_opakowania)s,
                                            %(pojemnosc)s,
                                            %(jednostka_pojemnosci)s,
                                            %(informacje_dodatkowe)s
                                        );
                                        """, opakowanie)
                        else:
                            print(opakowanie)


    return 0

if __name__ == "__main__":
    cur, conn = get_psql_cursor()
    main(cur, conn)
    conn.close()