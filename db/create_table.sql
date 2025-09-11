CREATE TABLE leki (
    id SERIAL PRIMARY KEY,
    nazwa_leku VARCHAR(255) NOT NULL,
    nazwa_lacinska VARCHAR(255),
    moc VARCHAR(100),
    kod_atc VARCHAR(20),
    forma VARCHAR(100),
    producent VARCHAR(255),
    rodzaj VARCHAR(50), -- ludzki, zwierzęcy
    nazwa_postaci_farmaceutycznej VARCHAR(255),
    link_do_ulotki VARCHAR(500),
    link_do_chpl VARCHAR(500),
    droga_podania VARCHAR(100)
);