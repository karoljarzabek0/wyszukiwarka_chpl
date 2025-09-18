CREATE TABLE opakowania (
    id_opakowania SERIAL PRIMARY KEY,
    id_produktu integer NOT NULL,
    FOREIGN KEY (id_produktu) REFERENCES leki(id_produktu) ON DELETE CASCADE,
    kod_gtin VARCHAR(50),
    kategoria_dostepnosci VARCHAR(255),
    skasowane VARCHAR(50),
    numerEU VARCHAR(50),
    dystrybutor_rownolegly VARCHAR(255),
    id_xml VARCHAR(10),
    liczba_opakowan VARCHAR(50),
    rodzaj_opakowania VARCHAR(50),
    pojemnosc VARCHAR(50),
    jednostka_pojemnosci VARCHAR(50),
    informacje_dodatkowe VARCHAR(255)
);
CREATE OR REPLACE FUNCTION insert_opakowania(
    p_id_produktu integer,
    p_kod_gtin VARCHAR(50),
    p_kategoria_dostepnosci VARCHAR(255),
    p_skasowane VARCHAR(50),
    p_numerEU VARCHAR(50),
    p_dystrybutor_rownolegly VARCHAR(255),
    p_id_xml VARCHAR(10),
    p_liczba_opakowan VARCHAR(50),
    p_rodzaj_opakowania VARCHAR(50),
    p_pojemnosc VARCHAR(50),
    p_jednostka_pojemnosci VARCHAR(50),
    p_informacje_dodatkowe VARCHAR(255)
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO opakowania (
        id_produktu,
        kod_gtin,
        kategoria_dostepnosci,
        skasowane,
        numerEU,
        dystrybutor_rownolegly,
        id_xml,
        liczba_opakowan,
        rodzaj_opakowania,
        pojemnosc,
        jednostka_pojemnosci,
        informacje_dodatkowe
    ) VALUES (
        p_id_produktu,
        p_kod_gtin,
        p_kategoria_dostepnosci,
        p_skasowane,
        p_numerEU,
        p_dystrybutor_rownolegly,
        p_id_xml,
        p_liczba_opakowan,
        p_rodzaj_opakowania,
        p_pojemnosc,
        p_jednostka_pojemnosci,
        p_informacje_dodatkowe
    );
END;
$$ LANGUAGE plpgsql;