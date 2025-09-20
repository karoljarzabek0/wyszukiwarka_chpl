CREATE TABLE IF NOT EXISTS fragmenty (
    id_fragmentu SERIAL PRIMARY KEY,
    id_produktu INTEGER NOT NULL,
    FOREIGN KEY (id_produktu) REFERENCES leki(id_produktu),
    tresc_fragmentu TEXT,
    typ_fragmentu VARCHAR(20), -- ulotka, chpl
    embedded_vector VECTOR(1536) -- assuming 1536 dimensions for the embedding vector
)

CREATE OR REPLACE FUNCTION insert_fragment(
    p_id_produktu INTEGER,
    p_tresc_fragmentu TEXT,
    p_typ_fragmentu VARCHAR(20),
    p_embedded_vector VECTOR(1536)
) RETURNS INTEGER AS $$
DECLARE
    new_id INTEGER;
BEGIN
    INSERT INTO fragmenty (id_produktu, tresc_fragmentu, typ_fragmentu, embedded_vector)
    VALUES (p_id_produktu, p_tresc_fragmentu, p_typ_fragmentu, p_embedded_vector)
    RETURNING id_fragmentu INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;