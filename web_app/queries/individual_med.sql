SELECT l.id_produktu,
       l.nazwa_produktu,
       slugify(l.nazwa_produktu) AS slug,
	   --l.rodzaj_preparatu,
	   l.nazwa_powszechna,
	   l.moc,
	   l.nazwa_postaci_farmaceutycznej,
	   l.droga_podania,
	   l.charakterystyka,
	   l.podmiot_odpowiedzialny,
	   l.nazwa_wytwórcy_importera,
	   l.kraj_wytwórcy_importera,
	   a.name,
	   atc.name,
       CONCAT(o.pojemnosc, ' ', o.jednostka_pojemnosci) AS dawka,
	   r.poziom_odplatnosci, r. wysokosc_doplata_swiadczeniobiorcy,
		r.zakres_wskazan_objetych_refundacja
FROM leki l
LEFT JOIN opakowania o ON o.id_produktu = l.id_produktu
LEFT JOIN refundacja r ON r.numer_gtin = o.kod_gtin
LEFT JOIN grupy_atc a ON a.code = LEFT(l.kod_atc, 1)
LEFT JOIN grupy_atc atc ON atc.code = LEFT(l.kod_atc, 3)
WHERE slugify(l.nazwa_produktu) = %s
ORDER BY r.poziom_odplatnosci, CAST(o.pojemnosc AS NUMERIC)
;