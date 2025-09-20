import os
from dotenv import load_dotenv
import psycopg2
import torch
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model_name = 'sdadas/mmlw-retrieval-roberta-large'
model = SentenceTransformer(model_name, device=device, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("sdadas/mmlw-retrieval-roberta-large", trust_remote_code=True)
print("Imported models")


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

cur, conn = get_psql_cursor()

#QUERY = "zapytanie: działania nieporządane"

def search_similar(cur, query_text, top_k=5):
    # Create embedding for the query
    query_embedding = model.encode(query_text, convert_to_numpy=True)

    # Run similarity search
    cur.execute(
        """
        SELECT f.id_fragmentu, f.id_produktu, t.nazwa_produktu -- tresc_fragmentu
        FROM fragmenty f
        LEFT JOIN leki t ON f.id_produktu = t.id_produktu
        ORDER BY embedded_vector <=> %s::vector
        LIMIT %s;
        """,
        (query_embedding.tolist(), top_k)
    )
    return cur.fetchall()

results = search_similar(cur, "zapytanie: xanax działania nieporządane", 10)
for row in results:
    print(row)

conn.close()