WITH query_cte AS (
SELECT websearch_to_tsquery('polishv2', %s) AS query_text
),
vector_search AS (
	SELECT id_produktu, id_fragmentu, vector_rank
	FROM (
		SELECT
			f.id_produktu,
			f.id_fragmentu,
			(f.embedded_vector <=> %s::vector)::float AS vector_rank,
			ROW_NUMBER() OVER (
				PARTITION BY f.id_produktu
				ORDER BY f.embedded_vector <=> %s::vector ASC
			) AS rn
		FROM fragmenty f
	) AS vec
	WHERE rn = 1
	ORDER BY vector_rank ASC
	LIMIT 1000
), 
fts_filter AS (
    SELECT 
    v.id_produktu,
    v.id_fragmentu,
    v.vector_rank,
    ts_rank(t.fts_vector, q.query_text, 32) AS fts_rank
    FROM vector_search v
    LEFT JOIN tresc_chpl t ON v.id_produktu = t.id_produktu
    CROSS JOIN query_cte q
    WHERE t.fts_vector @@ q.query_text AND ts_rank(t.fts_vector, q.query_text, 32) >= 0.05
)
SELECT f.id_produktu,
    l.nazwa_produktu,
    l.kod_atc,
    l.nazwa_powszechna,
    l.moc,
    g.name AS grupa_atc,
    ROUND(f.vector_rank::numeric, 4)::float AS vector_rank, 
    ROUND(f.fts_rank::numeric, 4)::float AS fts_rank,
    ts_headline('polishv2', fr.tresc_fragmentu, q.query_text,'MaxFragments=1, MaxWords=50, MinWords=40')--, fr.tresc_fragmentu , StartSel=<<, StopSel=>>
FROM fts_filter f
CROSS JOIN query_cte q
LEFT JOIN leki l ON f.id_produktu = l.id_produktu
LEFT JOIN fragmenty fr ON f.id_fragmentu = fr.id_fragmentu
LEFT JOIN grupy_atc g ON LEFT(l.kod_atc, 1) = g.code
ORDER BY f.vector_rank ASC
LIMIT 30;