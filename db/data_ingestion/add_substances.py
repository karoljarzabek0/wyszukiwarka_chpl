from dotenv import load_dotenv
import psycopg2
import os
import io
import requests
import xml.etree.ElementTree as ET

load_dotenv()

DB_HOST = "192.168.0.22"
DB_PORT = "5432"
DB_NAME = "rejestr_lekow_db"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD")

def connect_psql():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connected to the database successfully!")

        return conn
    except Exception as e:
        print("Error while connecting to PostgreSQL:", e)

def insertToSubDB(insert_data: dict):
    conn = None
    conn = connect_psql()

    query = """--sql
        INSERT INTO substances2 (
        product_id,
        substance_name,
        quantity,
        unit,
        amount,
        unit_of_measure,
        additional_info
        ) VALUES (
            %(product_id)s,
            %(substance_name)s,
            %(quantity)s,
            %(unit)s,
            %(amount)s,
            %(unit_of_measure)s,
            %(additional_info)s
        )
    """

    cur = conn.cursor()
    product_id = insert_data["product_id"]
    try:
        cur.execute(query, insert_data)
        conn.commit()
        print(f"Successfully inserted product ID {product_id}")
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error inserting product ID {product_id}: {e}")
        return False
    

###

# Fetch the XML data
response = requests.get("https://rejestry.ezdrowie.gov.pl/api/rpl/medicinal-products/public-pl-report/6.0.0/overall.xml")

# Define the XML namespace
NAMESPACE = {"ns": "http://rejestry.ezdrowie.gov.pl/rpl/eksport-danych-v6.0.0"}

xml_file = io.BytesIO(response.content)

# Initialize empty lists to store data

active_substances_data = []
i=0
# Use iterparse for incremental parsing
for event, elem in ET.iterparse(xml_file, events=('start', 'end')):
    # Process the product when we hit the 'end' event for a product
    if event == 'end' and 'produktLeczniczy' in elem.tag:
        # Extract general product details
        product_id = elem.get("id")

        active_substances_data = []
        # Extract active substances and store them in the active substances list
        for substance in elem.findall('.//ns:substancjeCzynne/ns:substancjaCzynna', NAMESPACE):
            print(f"Substance: {substance.get('nazwaSubstancji')}")
            active_substances_data.append({
                'product_id': product_id,  # Link the active substance to the product
                'substance_name': substance.get('nazwaSubstancji'),
                'quantity': substance.get('iloscSubstancji'),
                'unit': substance.get('jednostkaMiaryIlosciSubstancji'),
                'amount': substance.get('iloscPreparatu'),
                'unit_of_measure': substance.get('jednostkaMiaryIlosciPreparatu'),
                'additional_info': substance.get('innyOpisIlosci')
            })

        for substance in active_substances_data:
            insertToSubDB(insert_data=substance)

        # Clear the element to free memory (important for large XML files)
        elem.clear()
        print(f"-------> Loop: {i} <-------")
        i += 1

