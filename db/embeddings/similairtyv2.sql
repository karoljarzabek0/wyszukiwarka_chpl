WITH target_vector AS (
    SELECT AVG(embedded_vector) AS vector
    FROM fragmenty
    WHERE id_produktu = 100000936
),
product_vectors AS (
    SELECT 
        f.id_produktu,
        AVG(f.embedded_vector) AS vector
    FROM fragmenty f
    GROUP BY f.id_produktu
),
distances AS (
    SELECT 
        p.id_produktu,
        (p.vector <=> t.vector) AS distance
    FROM product_vectors p
    CROSS JOIN target_vector t
)
SELECT
    d.id_produktu,
    l.nazwa_produktu,
    l.kod_atc,
    ROUND(1 - d.distance::numeric, 4) AS avg_similarity
FROM distances d
LEFT JOIN leki l ON l.id_produktu = d.id_produktu
ORDER BY avg_similarity DESC
LIMIT 10;
