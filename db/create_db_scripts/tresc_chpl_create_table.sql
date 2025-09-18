CREATE TABLE IF NOT EXISTS tresc_chpl
(
    id_produktu integer NOT NULL,
    FOREIGN KEY (id_produktu) REFERENCES leki(id_produktu) ON DELETE CASCADE,
    tresc_chpl TEXT,
    fts_vector tsvector GENERATED ALWAYS AS (
    to_tsvector('simple', coalesce(tresc_chpl, ''))
    -- pl_ispell
    ) STORED
);

CREATE INDEX IF NOT EXISTS idx_tresc_chpl_fts
    ON tresc_chpl USING GIN (fts_vector);

CREATE OR REPLACE FUNCTION insert_tresc_chpl(
    p_id_produktu integer,
    p_tresc_chpl text
)
RETURNS void AS $$
BEGIN
    INSERT INTO tresc_chpl (id_produktu, tresc_chpl)
    VALUES (p_id_produktu, p_tresc_chpl);
END;
$$ LANGUAGE plpgsql;