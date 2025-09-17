CREATE TABLE IF NOT EXISTS fragmenty (
    id_fragmentu SERIAL PRIMARY KEY,
    id_produktu INTEGER NOT NULL,
    FOREIGN KEY (id_produktu) REFERENCES leki(id_produktu),
    tresc_fragmentu TEXT,
    typ_fragmentu VARCHAR(20), -- ulotka, chpl
    embedded_vector VECTOR(1536) -- assuming 1536 dimensions for the embedding vector
)