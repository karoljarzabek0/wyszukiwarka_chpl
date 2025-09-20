CREATE TABLE IF NOT EXISTS fragmenty (
    id_fragmentu SERIAL PRIMARY KEY,
    id_produktu INTEGER NOT NULL,
    FOREIGN KEY (id_produktu) REFERENCES leki(id_produktu),
    tresc_fragmentu TEXT,
    typ_fragmentu VARCHAR(20), -- ulotka, chpl
    embedded_vector VECTOR(1024) -- assuming 1024 dimensions for the embedding vector
)

CREATE OR REPLACE FUNCTION insert_fragment(
    p_id_produktu INTEGER,
    p_tresc_fragmentu TEXT,
    p_typ_fragmentu VARCHAR(20),
    p_embedded_vector VECTOR(1024)
) RETURNS void AS $$
BEGIN
    INSERT INTO fragmenty (id_produktu, tresc_fragmentu, typ_fragmentu, embedded_vector)
    VALUES (p_id_produktu, p_tresc_fragmentu, p_typ_fragmentu, p_embedded_vector);
END;
$$ LANGUAGE plpgsql;