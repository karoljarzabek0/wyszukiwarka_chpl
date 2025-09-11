# Konstrukacja bazy danych
## Główna tabela
- Kolumny: id, nazwa leku, nazwa łacińska, moc, kod atc, forma, producent, rodzaj (ludzki, zwierzęcy), nazwa psotaci farmacetycznej, link do ulotki, link do chpl, droga podania
## Tabela z substacjami czynnymi
- id, id leku, iosc substacji, miara ilosc, ilosc prepartu, miara ilosci prepratu
## Tabela z zawartością chpl i ulotek
- id fragmentu, id leku, tresc fragmentu, zwektoryzowany fragment, fragment zwektoryzowany pod fts, 
## (Opcjonalnie) Tabela z klucozwymi aspektami danego leku ywgenerowane przez AI
- Kolumny: id leku, zastosowanie, przeciwskazania, efekty uboczne, czy mozna stoswac w ciązy, czy moga stsowac dzieci, interakcje z innymi lekami
