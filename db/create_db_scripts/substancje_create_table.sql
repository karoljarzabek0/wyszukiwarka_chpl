CREATE TABLE IF NOT EXISTS substancje
(
    id_produktu integer NOT NULL,
    nazwa_substancji VARCHAR(255),
    ilosc_substancji VARCHAR(100),
    jednostka_miary_ilosci_substancji VARCHAR(100),
    ilosc_preparatu VARCHAR(100),
    jednostka_miar_ilosci_preparatu VARCHAR(50),
    informacje_dodatkowe TEXT
);

CREATE OR REPLACE FUNCTION insert_substancje(
    p_id_produktu integer,
    p_nazwa_substancji VARCHAR(255),
    p_ilosc_substancji VARCHAR(100),
    p_jednostka_miary_ilosci_substancji VARCHAR(100),
    p_ilosc_preparatu VARCHAR(100),
    p_jednostka_miar_ilosci_preparatu VARCHAR(50),
    p_informacje_dodatkowe TEXT
)
RETURNS void AS $$
BEGIN
    INSERT INTO substancje (id_produktu, nazwa_substancji, ilosc_substancji, jednostka_miary_ilosci_substancji, ilosc_preparatu, jednostka_miar_ilosci_preparatu, informacje_dodatkowe)
    VALUES (p_id_produktu, p_nazwa_substancji, p_ilosc_substancji, p_jednostka_miary_ilosci_substancji, p_ilosc_preparatu, p_jednostka_miar_ilosci_preparatu, p_informacje_dodatkowe);
END;
$$ LANGUAGE plpgsql;
