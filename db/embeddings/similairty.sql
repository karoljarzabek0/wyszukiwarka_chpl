---- Badanie podobieństwa
WITH target_vector AS (
SELECT AVG(embedded_vector) as vector
FROM fragmenty
WHERE id_produktu = 100031871
GROUP BY id_produktu
)

SELECT f.id_produktu,
	l.nazwa_produktu,
	AVG(f.embedded_vector),
	MIN(f.embedded_vector <=> t.vector)
FROM fragmenty f
CROSS JOIN target_vector t
LEFT JOIN leki l ON l.id_produktu = f.id_produktu
GROUP BY f.id_produktu, l.nazwa_produktu
ORDER BY MIN(f.embedded_vector <=> t.vector)
LIMIT 100
;