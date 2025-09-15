CREATE TABLE IF NOT EXISTS substancje
(
    id_leku integer NOT NULL,
    nazwa_substancji VARCHAR(255),
    ilosc VARCHAR(255),
    jednostka VARCHAR(50),
    wartosc VARCHAR(255),
    jednostka_miary VARCHAR(50),
    dodatkowe_info TEXT
)