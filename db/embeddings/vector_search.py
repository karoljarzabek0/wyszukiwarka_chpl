import os
from dotenv import load_dotenv
import psycopg2
import torch
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer
import pandas as pd

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
    query_embedding = model.encode("zapytanie: " + query_text, convert_to_numpy=True)

    # Run similarity search
    if True:
        cur.execute(
            """
            WITH query_cte AS (
            SELECT websearch_to_tsquery('polishv2', %s) AS query_text
            ),
            fts_ranked AS (
            SELECT
            t.id_produktu,
            t.nazwa_produktu,
            ts_rank(t.fts_vector, q.query_text) AS fts_rank
            FROM tresc_chpl t
            CROSS JOIN query_cte q
            WHERE t.fts_vector @@ q.query_text
            ORDER BY fts_rank DESC
            LIMIT 100
            ),
            vector_search AS (
            SELECT
                f.id_produktu,
                MIN(embedded_vector <=> %s::vector)::float AS vector_rank
            FROM fragmenty f
            GROUP BY f.id_produktu
            ORDER BY MIN(embedded_vector <=> %s::vector)
            LIMIT 1000
            )
            SELECT 
                COALESCE(f.id_produktu, v.id_produktu) AS id_produktu,
                t.nazwa_produktu, t.kod_atc, t.nazwa_powszechna,
                ROUND(CAST(COALESCE(f.fts_rank, 0) AS NUMERIC), 2)::float AS fts_rank,
                ROUND(CAST(COALESCE(1 - v.vector_rank, 0) AS NUMERIC), 2)::float AS vector_rank,
                ROUND(CAST(((COALESCE(f.fts_rank, 0) * 0.3) + (COALESCE(1 - v.vector_rank, 0) * 0.7)) AS NUMERIC), 2)::float AS combined_rank,
                jsonb_agg(s.nazwa_substancji) AS substancje
            FROM fts_ranked f
            FULL JOIN vector_search v ON f.id_produktu = v.id_produktu
            LEFT JOIN leki t ON COALESCE(f.id_produktu, v.id_produktu) = t.id_produktu
            LEFT JOIN substancje s ON COALESCE(f.id_produktu, v.id_produktu) = s.id_produktu
            GROUP BY COALESCE(f.id_produktu, v.id_produktu), t.nazwa_produktu, t.kod_atc, t.nazwa_powszechna, f.fts_rank, v.vector_rank
            ORDER BY combined_rank DESC
            LIMIT 20;
            """,
            (query_text, query_embedding.tolist(), query_embedding.tolist())
        )
    else:
    # other option
        cur.execute(
            """
            WITH ranked_fragments AS (
            SELECT
            --f.id_fragmentu,
            f.id_produktu,
            t.nazwa_produktu, t.kod_atc --, f.tresc_fragmentu
            FROM fragmenty f
            LEFT JOIN leki t ON f.id_produktu = t.id_produktu
            ORDER BY embedded_vector <=> %s::vector
            LIMIT 100
            )
            SELECT kod_atc, COUNT(*) as fragment_count
            FROM ranked_fragments
            GROUP BY kod_atc
            ORDER BY fragment_count DESC
            """,
            (query_embedding.tolist(),)
        )

    return cur.fetchall()

results = search_similar(cur, "narcyzm", 50)
df = pd.DataFrame(results, columns=['id_produktu', 'nazwa_produktu', 'kod_atc', 'nazwa_powszechna', 'fts_rank', 'vector_rank', 'combined_rank', 'substancje'])
print(df)
# for row in results:
#     print(row)

conn.close()