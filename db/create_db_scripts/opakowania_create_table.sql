CREATE TABLE opakowania (
    id_opakowania SERIAL PRIMARY KEY,
    id_produktu integer NOT NULL,
    FOREIGN KEY (id_produktu) REFERENCES leki(id_produktu) ON DELETE CASCADE,