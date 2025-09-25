SELECT l.id_produktu,
       l.nazwa_produktu,
       slugify(l.nazwa_produktu) AS slug,
	   l.nazwa_powszechna,
	   l.moc,
	   l.nazwa_postaci_farmaceutycznej,
	   l.droga_podania,
	   l.charakterystyka,
	   l.podmiot_odpowiedzialny,
	   l.nazwa_wytwórcy_importera,
	   l.kraj_wytwórcy_importera,
	   a.name,
	   atc.name
FROM leki l
LEFT JOIN grupy_atc a ON a.code = LEFT(l.kod_atc, 1)
LEFT JOIN grupy_atc atc ON atc.code = LEFT(l.kod_atc, 3)
WHERE slugify(l.nazwa_produktu) = %s
LIMIT 1
;