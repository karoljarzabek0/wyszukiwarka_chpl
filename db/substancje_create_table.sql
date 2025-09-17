CREATE TABLE IF NOT EXISTS substancje
(
    id_produktu integer NOT NULL,
    nazwa_substancji VARCHAR(255),
    ilosc_substancji VARCHAR(100),
    jednostka_miary_ilosci_substancji VARCHAR(100),
    ilosc_preparatu VARCHAR(100),
    jednostka_miar_ilosci_preparatu VARCHAR(50),
    informacje_dodatkowe TEXT
)