CREATE TABLE IF NOT EXISTS tresc_ulotki
(
    id_produktu integer NOT NULL,
    FOREIGN KEY (id_produktu) REFERENCES leki(id_produktu) ON DELETE CASCADE,
    tresc_ulotki TEXT,
    fts_vector tsvector GENERATED ALWAYS AS (
    to_tsvector('polishv2', coalesce(tresc_ulotki, ''))
    -- pl_ispell
    ) STORED
);

CREATE INDEX IF NOT EXISTS idx_tresc_ulotki_fts
    ON tresc_ulotki USING GIN (fts_vector);

CREATE OR REPLACE FUNCTION insert_tresc_ulotki(
    p_id_produktu integer,
    p_tresc_ulotki text
)
RETURNS void AS $$
BEGIN
    INSERT INTO tresc_ulotki (id_produktu, tresc_ulotki)
    VALUES (p_id_produktu, p_tresc_ulotki);
END;
$$ LANGUAGE plpgsql;