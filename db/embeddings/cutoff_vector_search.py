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
    cur.execute(
        """
WITH query_cte AS (
SELECT websearch_to_tsquery('polishv2', %s) AS query_text
),
vector_search AS (
	SELECT id_produktu, id_fragmentu, vector_rank
	FROM (
		SELECT
			f.id_produktu,
			f.id_fragmentu,
			(f.embedded_vector <=> %s::vector)::float AS vector_rank,
			ROW_NUMBER() OVER (
				PARTITION BY f.id_produktu
				ORDER BY f.embedded_vector <=> %s::vector ASC
			) AS rn
		FROM fragmenty f
	) AS vec
	WHERE rn = 1
	ORDER BY vector_rank ASC
	LIMIT 1000
), 
fts_filter AS (
    SELECT 
    v.id_produktu,
    v.id_fragmentu,
    v.vector_rank,
    ts_rank(t.fts_vector, q.query_text, 32) AS fts_rank
    FROM vector_search v
    LEFT JOIN tresc_chpl t ON v.id_produktu = t.id_produktu
    CROSS JOIN query_cte q
    WHERE t.fts_vector @@ q.query_text AND ts_rank(t.fts_vector, q.query_text, 32) >= 0.05
)
SELECT f.id_produktu, l.nazwa_produktu, l.kod_atc, ROUND(f.vector_rank::numeric, 4)::float, ROUND(f.fts_rank::numeric, 4)::float
,ts_headline('polishv2', fr.tresc_fragmentu, q.query_text,'MaxFragments=2, MaxWords=10, MinWords=5, StartSel=<<, StopSel=>>')--, fr.tresc_fragmentu
FROM fts_filter f
CROSS JOIN query_cte q
LEFT JOIN leki l ON f.id_produktu = l.id_produktu
LEFT JOIN tresc_chpl t ON f.id_produktu = t.id_produktu
LEFT JOIN fragmenty fr ON f.id_fragmentu = fr.id_fragmentu
ORDER BY f.vector_rank ASC
LIMIT 30;
        """,
        (query_text, query_embedding.tolist(), query_embedding.tolist())
    )

    return cur.fetchall()

results = search_similar(cur, "cukrzyca", 50)
# df = pd.DataFrame(results, columns=['id_produktu', 'nazwa_produktu', 'kod_atc', 'nazwa_powszechna', 'fts_rank', 'vector_rank', 'combined_rank', 'substancje'])
# print(df)
print("nazwa_produktu, kod_atc, vector_rank, fts_rank, snippet")
for row in results:
    print(row)

conn.close()