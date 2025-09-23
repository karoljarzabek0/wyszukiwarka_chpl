    WITH query_cte AS (
    SELECT websearch_to_tsquery('polishv2', %s) AS query_text
    ),
    fts_ranked AS (
    SELECT
    t.id_produktu,
    t.nazwa_produktu,
    ts_rank(t.fts_vector, q.query_text) AS fts_rank
    FROM tresc_chpl t
    CROSS JOIN query_cte q
    WHERE t.fts_vector @@ q.query_text
    ORDER BY fts_rank DESC
    LIMIT 100
    ),
    vector_search AS (
    SELECT
        f.id_produktu,
        MIN(embedded_vector <=> %s::vector)::float AS vector_rank
    FROM fragmenty f
    GROUP BY f.id_produktu
    ORDER BY MIN(embedded_vector <=> %s::vector)
    LIMIT 1000
    )
    SELECT 
        COALESCE(f.id_produktu, v.id_produktu) AS id_produktu,
        t.nazwa_produktu, t.kod_atc, t.nazwa_powszechna,
        ROUND(CAST(COALESCE(f.fts_rank, 0) AS NUMERIC), 2)::float AS fts_rank,
        ROUND(CAST(COALESCE(1 - v.vector_rank, 0) AS NUMERIC), 2)::float AS vector_rank,
        ROUND(CAST(((COALESCE(f.fts_rank, 0) * 0.3) + (COALESCE(1 - v.vector_rank, 0) * 0.7)) AS NUMERIC), 2)::float AS combined_rank,
        jsonb_agg(s.nazwa_substancji) AS substancje
    FROM fts_ranked f
    FULL JOIN vector_search v ON f.id_produktu = v.id_produktu
    LEFT JOIN leki t ON COALESCE(f.id_produktu, v.id_produktu) = t.id_produktu
    LEFT JOIN substancje s ON COALESCE(f.id_produktu, v.id_produktu) = s.id_produktu
    GROUP BY COALESCE(f.id_produktu, v.id_produktu), t.nazwa_produktu, t.kod_atc, t.nazwa_powszechna, f.fts_rank, v.vector_rank
    ORDER BY combined_rank DESC
    LIMIT 20;