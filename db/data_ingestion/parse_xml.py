import io
import os
from tqdm import tqdm
from dotenv import load_dotenv
import requests
import xml.etree.ElementTree as ET
import psycopg2
import logging

load_dotenv()

logging.basicConfig(
    #filename='scraping_log.log',
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.WARNING
)

def connect_psql():
    DB_HOST = "192.168.0.22"
    DB_PORT = "5432"
    DB_NAME = "rejestr_lekow_db"
    DB_USER = "postgres"
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logging.debug("Connected to the database successfully!")

        return conn
    except Exception as e:
        logging.error("Error while connecting to PostgreSQL:", e)

def insertToDB(insert_data: dict):
    conn = None
    conn = connect_psql()

    # Create the SQL query
    query = """--sql
        INSERT INTO medicines2 (
            product_id,
            product_name,
            common_name,
            strength,
            form,
            company,
            characteristics,
            leaflet,
            species,
            atc_code,

            nazwa_sklad_postac,
            stosowanie_przeciwwskazania,
            interakcje_dzial_niep,
            wlasc_farmakologiczne,
            full_text
        ) VALUES (
            %(product_id)s,
            %(product_name)s,
            %(common_name)s,
            %(strength)s,
            %(form)s,
            %(company)s,
            %(characteristics)s,
            %(leaflet)s,
            %(species)s,
            %(atc_code)s,

            %(nazwa_sklad_postac)s,
            %(stosowanie_przeciwwskazania)s,
            %(interakcje_dzial_niep)s,
            %(wlasc_farmakologiczne)s,
            %(full_text)s
        )
        """

    cur = conn.cursor()
    product_id = insert_data["product_id"]
    try:
        cur.execute(query, insert_data)
        conn.commit()
        logging.debug(f"Successfully inserted product ID {product_id}")
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        logging.error(f"Error inserting product ID {product_id}: {e}")
        conn.close()
        return False


# Fetch the XML data
xml_filename = "response.xml"
def save_xml_to_file(xml_filename = xml_filename) -> None:
    try:
        response = requests.get("https://rejestry.ezdrowie.gov.pl/api/rpl/medicinal-products/public-pl-report/6.0.0/overall.xml")
        logging.debug("Fetched XML file successfully")
        with open(xml_filename, "wb") as file:
            file.write(response.content)
    except Exception as e:
        logging.error(f"ERROR FETCHING XML: {e}")
        exit()

save_xml_to_file()

with open(xml_filename, "rb") as file:
    xml_content = file.read()

# Create a BytesIO object from the content to parse it with ElementTree
xml_file = io.BytesIO(xml_content)

NAMESPACE = {"ns": "http://rejestry.ezdrowie.gov.pl/rpl/eksport-danych-v6.0.0"}
xml_file.seek(0)
tree = ET.ElementTree(file=xml_file)
root = tree.getroot()
total_products = len(list(root.iter(f'{{{NAMESPACE["ns"]}}}produktLeczniczy')))
logging.info(f"Total products: {total_products}")

i=0

# Use iterparse for incremental parsing
with tqdm(total=total_products, desc="Processing Products", unit="product") as pbar:
    for event, elem in ET.iterparse(xml_file, events=('start', 'end')):
        # if i % 10 == 0:
        #     os.system('clear')
        # Process the product when we hit the 'end' event for a product
        if event == 'end' and f"{{{NAMESPACE['ns']}}}produktLeczniczy" in elem.tag:
            characteristics = ""
            # Extract general product details
            product_id = elem.get("id")
            product_name = elem.get("nazwaProduktu")
            common_name = elem.get("nazwaPowszechnieStosowana")
            strength = elem.get("moc")
            form = elem.get("nazwaPostaciFarmaceutycznej")
            company = elem.get("podmiotOdpowiedzialny")
            characteristics = elem.get("charakterystyka")
            leaflet = elem.get("ulotka")
            species = elem.get("rodzajPreparatu")

            # Extract ATC code (assuming there is only one per product)
            atc_code = elem.find('.//ns:kodyATC/ns:kodATC', NAMESPACE)
            atc_code = atc_code.text if atc_code is not None else None
            logging.info(f"Parsed XML for ID: {product_id}")

            if characteristics is None or len(characteristics) <= 10:
                logging.warning(f"URL for ID: {product_id} not found")
                textInDict = {
                    "nazwa_sklad_postac": 'NO_URL',
                    "stosowanie_przeciwwskazania": 'NO_URL',
                    "interakcje_dzial_niep": 'NO_URL',
                    "wlasc_farmakologiczne": 'NO_URL',
                    }
            else:
                try:
                    textInDict, fullText = parseToPlainText(url=characteristics)
                    logging.debug(f"Fetched ChPL document for ID: {product_id}")
                except Exception as e:
                    logging.warning(f"Failed to fetch ChPL for ID: {product_id} | Reason: {e} | URL: {characteristics}")
                    textInDict = {
                        "nazwa_sklad_postac": 'NOT_FOUND',
                        "stosowanie_przeciwwskazania": 'NOT_FOUND',
                        "interakcje_dzial_niep": 'NOT_FOUND',
                        "wlasc_farmakologiczne": 'NOT_FOUND',
                        }

            product = {
                "product_id": product_id,
                "product_name": product_name,
                "common_name": common_name,
                "strength": strength,
                "form": form,
                "company": company,
                "characteristics": characteristics,
                "leaflet": leaflet,
                "species": species,
                "atc_code": atc_code,
                **textInDict,
                "full_text": fullText
            }
            insertToDB(insert_data=product)

            # Clear the element to free memory (important for large XML files)
            product.clear()
            elem.clear()
            # print(f"----> Loop: {i} <----")
            i += 1
            os.system('clear')
            pbar.update(1)
            with open('progress_bar.log', 'a') as f:
                f.write(f"Progress: {pbar.n}/{pbar.total} ({(pbar.n/pbar.total)*100:.2f}%)\n")


# Convert the lists to DataFrames


# Optionally, save the data to CSV files


# DB_HOST = "192.168.0.22"
# DB_PORT = "5432"
# DB_NAME = "rejestr_lekow_db"
# DB_USER = "postgres"
# DB_PASSWORD = os.getenv("DB_PASSWORD")

# engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# df_products.to_sql("basic_info", engine, if_exists="replace", index=False)
# df_active_substances.to_sql("active_substances", engine, if_exists="replace", index=False)
# Print the first few rows of each DataFrame to verify
# print("Products Data:")
# print(df_products.head())
# print("\nActive Substances Data:")
# print(df_active_substances.head())
