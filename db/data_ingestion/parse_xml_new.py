import os
import io
import requests
import psycopg2
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

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
    return xml_file, NAMESPACE

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
