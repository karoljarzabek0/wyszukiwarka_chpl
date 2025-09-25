from flask import Blueprint, render_template
from db_helper import get_db_connection
import os
import json

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
    bases = cur.fetchone()

    if bases:
        base = {
            "id_produktu": bases[0],
            "nazwa_produktu": bases[1],
            "slug": bases[2],
            "nazwa_powszechna": bases[3],
            "moc": bases[4],
            "nazwa_postaci_farmaceutycznej": bases[5],
            "droga_podania": bases[6],
            "charakterystyka": bases[7],
            "podmiot_odpowiedzialny": bases[8],
            "nazwa_wytwórcy_importera": bases[9],
            "kraj_wytwórcy_importera": bases[10],
            "name": bases[11],
            "atc_name": bases[12],
            "kod_atc": bases[13]
        }
    else:
        base = {}

    sql_path = os.path.join(os.path.dirname(__file__), 'queries', 'refundacja.sql')
    print(f"Loading SQL from: {sql_path}")
    with open(sql_path, 'r', encoding='utf-8') as f:
        refundacja_query = f.read()
    cur.execute(refundacja_query, (slug,))
    refundacja_data = cur.fetchall()

    refundacja = []
    for row in refundacja_data:
        refundacja.append({
            "id_produktu": row[0],
            "nazwa_produktu": row[1],
            "moc": row[2],
            "ilosc": row[3],
            "cena_detaliczna": row[4],
            "poziom_odplatnosci": row[5],
            "wysokosc_doplaty": row[6],
            "zakres_objety_refundacja": row[7]
        })

    atc_letter = bases['kod_atc'][0:1]
    icons = {'A': 'stomach.svg',
             'B': 'blood.svg',
             'C': 'heart.svg',
             'D': 'skin.svg',
             'H': 'hormones.svg',
             'J': 'virus.svg',
             'L': 'cancer.svg',
             'M': 'bones.svg',
             'N': 'brain.svg',
             'P': 'bug.svg',
             'R': 'lungs.svg',
             'S': 'eye.svg',
             'V': 'other.svg'
             }
    try:
        svg = icons[atc_letter]
    except Exception as e:
        svg = 'other.svg'

    cur.close()
    conn.close()
    
    return render_template('lek.html', base=base, refundacja=refundacja, svg=svg)
