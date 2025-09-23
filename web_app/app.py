from flask import Flask, render_template, request, jsonify, Response
import torch
from sentence_transformers import SentenceTransformer
import json
import os
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras


app = Flask(__name__)

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model_name = 'sdadas/mmlw-retrieval-roberta-large'
model = SentenceTransformer(model_name, device=device, trust_remote_code=True)

with open('kody_atc.json', 'r', encoding='utf-8') as f:
    kody_atc = json.load(f)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# API endpoint: Get all users
@app.route('/api/search', methods=['GET'])
def get_users():
    q = request.args.get('q')
    query_embedding = model.encode("zapytanie: " + q, convert_to_numpy=True)
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
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
    (q, query_embedding.tolist(), query_embedding.tolist())
)
    rows = cur.fetchall()
    
    results = [dict(row) for row in rows]  # convert rows to dict
    for result in results:
        kod_atc = result.get('kod_atc')
        if kod_atc:
            main_group = kod_atc[0]  # Get the first character for the main group
            second_group = kod_atc[:3]  # Get the first three characters for the second group
            result['nazwa_atc'] = kody_atc.get(main_group, {}).get('name', 'Unknown')
            result['podgrupa_atc'] = kody_atc.get(main_group, {}).get('subgroups', {}).get(second_group, 'Brak')
            print(second_group)
        else:
            result['nazwa_atc'] = 'Brak'

    cur.close()
    conn.close()
    
    return Response(
    json.dumps(results, ensure_ascii=False),
    content_type='application/json; charset=utf-8'
)

# API endpoint: Get single user by id
@app.route('/api/leki/<int:id_produktu>', methods=['GET'])
def get_user(id_produktu):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute("SELECT nazwa_produktu, kod_atc FROM leki WHERE id_produktu = %s;", (id_produktu,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row is None:
        return jsonify({"error": "Nie znaleziono leku"}), 404
    return jsonify(dict(row))

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5001)