from flask import Blueprint, request, jsonify, Response
import json
import psycopg2.extras
from .db_helper import get_db_connection, log_query
from .roberta import model
import os



api_bp = Blueprint("api", __name__)

@api_bp.route("/search", methods=["GET"])
def search():
    sql_path = os.path.join(os.path.dirname(__file__), 'queries', 'hybrid_search.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        hybrid_search_query = f.read()

    q = request.args.get("q")
    query_embedding = model.encode("zapytanie: " + q, convert_to_numpy=True)
    q = " OR ".join(q.split())  # Simple tokenization by spaces
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute(
        hybrid_search_query,
        (q, query_embedding.tolist(), query_embedding.tolist())
    )
    rows = cur.fetchall()
    results = [dict(row) for row in rows]
    cur.close()
    log_query(conn=conn, is_index=True, query_name=q.replace(" OR ", " "))
    conn.close()

    return Response(
        json.dumps(results, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )

@api_bp.route("/leki/<int:id_produktu>", methods=["GET"])
def get_leki(id_produktu):
    return jsonify({"error": "bad_url"})
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute("SELECT nazwa_produktu, kod_atc FROM leki WHERE id_produktu = %s;", (id_produktu,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if row is None:
        return jsonify({"error": "Nie znaleziono leku"}), 404
    return jsonify(dict(row))
