SELECT l.id_produktu,
       l.nazwa_produktu,
	   l.moc,
       CONCAT(o.pojemnosc, ' ', o.jednostka_pojemnosci) AS ilosc,
	   COALESCE(CAST(r.cena_detaliczna AS TEXT), 'Brak danych') AS cena_detaliczna,
	   COALESCE(r.poziom_odplatnosci, 'Brak') AS poziom_odplatnosci,
	   COALESCE(r.wysokosc_doplata_swiadczeniobiorcy, '0') AS wysokosc_doplaty,
	COALESCE(r.zakres_wskazan_objetych_refundacja, 'Brak') AS zakres_objety_refundacja
FROM leki l
LEFT JOIN opakowania o ON o.id_produktu = l.id_produktu
LEFT JOIN refundacja r ON r.numer_gtin = o.kod_gtin
LEFT JOIN grupy_atc a ON a.code = LEFT(l.kod_atc, 1)
LEFT JOIN grupy_atc atc ON atc.code = LEFT(l.kod_atc, 3)
WHERE slugify(l.nazwa_produktu) = %s
ORDER BY r.poziom_odplatnosci, l.id_produktu,  CAST(o.pojemnosc AS NUMERIC) DESC
;