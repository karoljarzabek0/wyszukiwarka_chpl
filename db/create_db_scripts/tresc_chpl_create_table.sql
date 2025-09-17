CREATE TABLE IF NOT EXISTS tresc_chpl
(
    id_produktu integer NOT NULL,
    tresc_chpl TEXT,
    fts_vector tsvector GENERATED ALWAYS AS (
    to_tsvector('simple', coalesce(tresc_chpl, ''))
    -- pl_ispell
    ) STORED
);

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