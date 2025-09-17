-- Function for websearch-style full text search with highlighting
CREATE OR REPLACE FUNCTION websearch_chpl(query text)
RETURNS TABLE (
    id_produktu integer,
    fragment text,
    rank real
)
LANGUAGE sql
AS $$
    SELECT
        t.id_produktu,
        ts_headline(
            'simple',                          -- dictionary
            t.tresc_chpl,                      -- original text
            websearch_to_tsquery('simple', query), -- query
            'StartSel=<b>, StopSel=</b>, MaxFragments=3, MinWords=5, MaxWords=15'
        ) AS fragment,
        ts_rank(t.fts_vector, websearch_to_tsquery('simple', query)) AS rank
    FROM tresc_chpl t
    WHERE t.fts_vector @@ websearch_to_tsquery('simple', query)
    ORDER BY rank DESC;
$$;
