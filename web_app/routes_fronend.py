from flask import Blueprint, render_template
from db_helper import get_db_connection
import os

frontend_bp = Blueprint("frontend", __name__)

@frontend_bp.route("/")
def index():
    return render_template("index.html")

@frontend_bp.route('/leki/<slug>')
def produkt(slug):
    conn = get_db_connection()
    cur = conn.cursor()

    sql_path = os.path.join(os.path.dirname(__file__), 'queries', 'individual_med.sql')
    print(f"Loading SQL from: {sql_path}")
    with open(sql_path, 'r', encoding='utf-8') as f:
        lek_query = f.read()
    cur.execute(lek_query, (slug,))
    bases = cur.fetchall()

    base = { 

    }
    refundacja = {}

    cur.close()
    conn.close()
    
    return render_template('lek.html', base=base, refundacja=refundacja)
