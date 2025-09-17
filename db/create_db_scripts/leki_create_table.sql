CREATE TABLE leki (
    id_produktu SERIAL PRIMARY KEY,
    nazwa_produktu VARCHAR(255) NOT NULL,
    rodzaj_preparatu VARCHAR(255), -- ludzki, zwierzęcy
    nazwa_powszechna VARCHAR(255),
    moc VARCHAR(255),
    nazwa_postaci_farmaceutycznej VARCHAR(255),
    podmiot_odpowiedzialny VARCHAR(255), 
    nazwa_postaci_farmaceutycznej VARCHAR(255),
    typ_procedury VARCHAR(255),
    waznosc_pozwolenia VARCHAR(255),
    podstawa_prawna VARCHAR(255),
    zakaz_stosowania_zwierzeta VARCHAR(255),
    ulotka VARCHAR(255),
    charakterystyka VARCHAR(255),
    kod_ATC VARCHAR(50),
    droga_podania VARCHAR(255),
    nazwa_wytwórcy_importera VARCHAR(255),
    kraj_wytwórcy_importera VARCHAR(100)
);