import os
import torch
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
import psycopg2

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
    

def insert_embedding(cur, conn, id_produktu, tresc, wektor):
    typ_fragmentu = 'chpl'
    try:
        cur.execute(
            """
            SELECT insert_fragment (%s, %s, %s, %s::vector);
            """,
            (id_produktu, tresc, typ_fragmentu, wektor.tolist())
        )
        conn.commit()
        #print(f"Inserted embedding for product ID {id_produktu}")
    except Exception as e:
        print("Error inserting embedding:", e)
        conn.rollback()  

def process_text(id_produktu, text):
    chunks = text_splitter.create_documents([text])
    # Shape: 1024
    # chunks = chunk_text(text)

    print(f"Total chunks created: {len(chunks)}")
    for chunk in chunks:
        #print(chunk)
        #print(f"Length of chunk in chars: {len(chunk.page_content)}")
        token_ids = tokenizer.encode(chunk.page_content)
        #print("Number of tokens:", len(token_ids))
        embeddings = model.encode(chunk.page_content, convert_to_numpy=True)
        #print("Embedding shape:", embeddings.shape)
        insert_embedding(cur, conn, id_produktu, chunk.page_content, embeddings)
        #print("------")


load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

print("Imported transformers")

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=2000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=True,
)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model_name = 'sdadas/mmlw-retrieval-roberta-large'
model = SentenceTransformer(model_name, device=device, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("sdadas/mmlw-retrieval-roberta-large", trust_remote_code=True)

print("Imported models")

###########################################
cur, conn = get_psql_cursor()

cur.execute("SELECT COUNT(*) FROM tresc_chpl WHERE LENGTH(tresc_chpl) > 5;")
count = cur.fetchone()[0]
print(f"Total records in tresc_chpl: {count}")

for i in range(count):
    print(f"Processing record {i+1}/{count}")
    cur.execute("""
    SELECT id_produktu, nazwa_produktu, tresc_chpl
    FROM tresc_chpl
    WHERE LENGTH(tresc_chpl) > 5
    ORDER BY id_produktu
    LIMIT 1
    OFFSET %s;
    """, (i,))

    id_produktu, nazwa_produktu, tresc_chpl = cur.fetchone()

    process_text(id_produktu, tresc_chpl)

conn.close()
