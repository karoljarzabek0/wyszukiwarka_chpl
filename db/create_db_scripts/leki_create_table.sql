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
CREATE OR REPLACE FUNCTION insert_leki(
    p_nazwa_produktu VARCHAR(255),
    p_rodzaj_preparatu VARCHAR(255),
    p_nazwa_powszechna VARCHAR(255),
    p_moc VARCHAR(255),
    p_nazwa_postaci_farmaceutycznej VARCHAR(255),
    p_podmiot_odpowiedzialny VARCHAR(255),
    p_typ_procedury VARCHAR(255),
    p_waznosc_pozwolenia VARCHAR(255),
    p_podstawa_prawna VARCHAR(255),
    p_zakaz_stosowania_zwierzeta VARCHAR(255),
    p_ulotka VARCHAR(255),
    p_charakterystyka VARCHAR(255),
    p_kod_ATC VARCHAR(50),
    p_droga_podania VARCHAR(255),
    p_nazwa_wytwórcy_importera VARCHAR(255),
    p_kraj_wytwórcy_importera VARCHAR(100)
)
RETURNS void AS $$
BEGIN
    INSERT INTO leki (nazwa_produktu, rodzaj_preparatu, nazwa_powszechna, moc, nazwa_postaci_farmaceutycznej, podmiot_odpowiedzialny, typ_procedury, waznosc_pozwolenia, podstawa_prawna, zakaz_stosowania_zwierzeta, ulotka, charakterystyka, kod_ATC, droga_podania, nazwa_wytwórcy_importera, kraj_wytwórcy_importera)
    VALUES (p_nazwa_produktu, p_rodzaj_preparatu, p_nazwa_powszechna, p_moc, p_nazwa_postaci_farmaceutycznej, p_podmiot_odpowiedzialny, p_typ_procedury, p_waznosc_pozwolenia, p_podstawa_prawna, p_zakaz_stosowania_zwierzeta, p_ulotka, p_charakterystyka, p_kod_ATC, p_droga_podania, p_nazwa_wytwórcy_importera, p_kraj_wytwórcy_importera);
END;
$$ LANGUAGE plpgsql;
