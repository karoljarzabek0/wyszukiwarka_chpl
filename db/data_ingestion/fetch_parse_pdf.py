import os
import requests
import re
import fitz
from dotenv import load_dotenv
import psycopg2


load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

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

def pdf_to_text(url):
    try:
        response = requests.get(url, timeout=5)
    except Exception as e:
        print("Request error:", e)
        return ""

    if response.status_code == 200:
        # Save the PDF to a local file
        with open('test.pdf', 'wb') as f:
            f.write(response.content)
        try:
            with fitz.open('test.pdf') as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                    text += '\n'      
        except Exception as e:
            text = ''
            print("Failed to open PDF:", e)
  
        # Usuń znaczniki stron i ich szum
        #text = re.sub(r"\n\d+\s*\n", "[[NOWA_STRONA]]\n", text)
        text = re.sub(r"\n\d+\s*\n", "\n", text)
        # Usuń puste miejsca
        #text = re.sub(r"\n\s*\n", "\n[[PUSTE_SPACJE]]\n", text)
        text = re.sub(r"\n\s*\n", r"\n", text)
        text = re.sub(r"\s*\n", r"\n", text)
        # Popraw nagłówki
        #text = re.sub(r"\d\s*\n", " ", text)
        text = re.sub(r"\.(\d)\s*\n", r".\1 ", text)
        text = re.sub(r"(\d)\.\s*\n", r"\1. ", text)
        #text = re.sub(r"\d\s*\n", "", text)
        # Usuń podwójne spacje
        #text = re.sub(r" {2}", "[[2x spacja]]", text)
        text = re.sub(r" {2}", " ", text)
        # Popraw punktory
        text = re.sub(r"^•\s*$\n?", "• ", text, flags=re.MULTILINE)
        with open("test.txt", "w", encoding="utf-8") as txt:
            txt.write(text)

        return text
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
    return ""

def get_pdf_links(cur):
    cur.execute("""--sql              
WITH leki_not_null AS (
SELECT
id_produktu,
nazwa_produktu,
charakterystyka
FROM leki
WHERE charakterystyka IS NOT NULL
)

SELECT DISTINCT ON (nazwa_produktu)
    l.id_produktu,
    l.nazwa_produktu,
    l.charakterystyka,
    COUNT(*) OVER (PARTITION BY l.nazwa_produktu) AS total_count
	--t.tresc_chpl
--FROM leki
FROM leki_not_null l
LEFT JOIN tresc_chpl t ON l.nazwa_produktu = t.nazwa_produktu
WHERE t.tresc_chpl IS NULL
ORDER BY nazwa_produktu, l.id_produktu
;
                """)
    return cur.fetchall()



def main(conn, cur):
    pdf_links = get_pdf_links(cur)
    print(pdf_links[:3])
    print(f"Found {len(pdf_links)} unique product names with PDF links.")

    for id_produktu, nazwa_produktu, url, count in pdf_links:
        print(f"Processing {nazwa_produktu} (ID: {id_produktu}) - {url}")
        text = pdf_to_text(url)
        if text:
            try:
                cur.execute("""--sql
                SELECT insert_tresc_chpl(%s, %s, %s);
                """, (id_produktu, nazwa_produktu, text))
                conn.commit()
                print(f"Inserted CHPL content for {nazwa_produktu} (ID: {id_produktu})")
            except Exception as e:
                print(f"Error inserting CHPL content for {nazwa_produktu} (ID: {id_produktu}):", e)
                conn.rollback()
        else:
            print(f"No text extracted for {nazwa_produktu} (ID: {id_produktu})")
    # url = "https://rejestry.ezdrowie.gov.pl/api/rpl/medicinal-products/2/characteristic"
    # text = pdf_to_text(url)
    # print(text[:1000])

if __name__ == "__main__":
    cur, conn = get_psql_cursor()
    if cur and conn:
        main(conn, cur)
    conn.close()