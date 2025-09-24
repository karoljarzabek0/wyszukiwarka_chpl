-- Drop table if it already exists
DROP TABLE IF EXISTS grupy_atc;

-- Create unified table
CREATE TABLE grupy_atc (
    code VARCHAR(5) PRIMARY KEY,        -- e.g. 'A', 'A01'
    name TEXT NOT NULL,                 -- e.g. "Przewód pokarmowy i metabolizm"
    parent_code VARCHAR(5) REFERENCES grupy_atc(code)  -- NULL dla grup głównych
);

-- Insert main groups
INSERT INTO grupy_atc (code, name, parent_code) VALUES
('A', 'Przewód pokarmowy i metabolizm', NULL),
('B', 'Krew i układ krwiotwórczy', NULL),
('C', 'Układ sercowo-naczyniowy', NULL),
('D', 'Preparaty dermatologiczne', NULL),
('G', 'Układ moczowo-płciowy i hormony płciowe', NULL),
('H', 'Hormony (z wyłączeniem płciowych)', NULL),
('J', 'Leki przeciwzakaźne (przeciwinfekcyjne)', NULL),
('L', 'Leki przeciwnowotworowe i immunomodulujące', NULL),
('M', 'Układ mięśniowo-szkieletowy', NULL),
('N', 'Ośrodkowy układ nerwowy', NULL),
('P', 'Leki przeciwpasożytnicze, owadobójcze i repelenty', NULL),
('R', 'Układ oddechowy', NULL),
('S', 'Narządy wzroku i słuchu', NULL),
('V', 'Różne', NULL);

-- Insert subgroups (with parent_code)
INSERT INTO grupy_atc (code, name, parent_code) VALUES
-- A
('A01', 'Preparaty stomatologiczne', 'A'),
('A02', 'Leki stosowane w zaburzeniach wydzielania soku żołądkowego', 'A'),
('A03', 'Leki stosowane w czynnościowych zaburzeniach przewodu pokarmowego', 'A'),
('A04', 'Leki przeciwwymiotne i przeciw nudnościom', 'A'),
('A05', 'Leki stosowane w chorobach dróg żółciowych i wątroby', 'A'),
('A06', 'Leki przeczyszczające', 'A'),
('A07', 'Leki przeciwbiegunkowe, przeciwzapalne i przeciwdrobnoustrojowe stosowane w chorobach przewodu pokarmowego', 'A'),
('A08', 'Leki przeciw otyłości z wyłączeniem preparatów dietetycznych', 'A'),
('A09', 'Preparaty trawienne, w tym enzymy', 'A'),
('A10', 'Leki stosowane w cukrzycy', 'A'),
('A11', 'Witaminy', 'A'),
('A12', 'Preparaty mineralne', 'A'),
('A13', 'Leki wzmacniające', 'A'),
('A14', 'Anaboliczne preparaty ogólnoustrojowe', 'A'),
('A15', 'Leki pobudzające apetyt', 'A'),
('A16', 'Inne leki działające na przewód pokarmowy i metabolizm', 'A'),

-- B
('B01', 'Leki przeciwzakrzepowe', 'B'),
('B02', 'Leki przeciwkrwotoczne', 'B'),
('B03', 'Leki stosowane w niedokrwistości', 'B'),
('B05', 'Preparaty krwiozastępcze i roztwory do wlewów', 'B'),
('B06', 'Inne leki hematologiczne', 'B'),

-- C
('C01', 'Leki stosowane w chorobach serca', 'C'),
('C02', 'Leki stosowane w chorobie nadciśnieniowej', 'C'),
('C03', 'Leki moczopędne', 'C'),
('C04', 'Leki rozszerzające naczynia obwodowe', 'C'),
('C05', 'Leki ochraniające ścianę naczyń', 'C'),
('C07', 'Leki β-adrenolityczne (Beta-blokery ?)', 'C'),
('C08', 'Antagonisty kanału wapniowego', 'C'),
('C09', 'Leki działające na układ renina–angiotensyna', 'C'),
('C10', 'Leki zmniejszające stężenie lipidów', 'C'),

-- D
('D01', 'Leki przeciwgrzybicze', 'D'),
('D02', 'Leki keratolityczne i działające ochronnie', 'D'),
('D03', 'Leki stosowane w leczeniu ran i owrzodzeń', 'D'),
('D04', 'Leki przeciwświądowe', 'D'),
('D05', 'Leki przeciwłuszczycowe', 'D'),
('D06', 'Antybiotyki i chemioterapeutyki', 'D'),
('D07', 'Kortykosteroidy', 'D'),
('D08', 'Antyseptyki i środki dezynfekujące', 'D'),
('D09', 'Opatrunki lecznicze', 'D'),
('D10', 'Leki przeciwtrądzikowe', 'D'),
('D11', 'Inne dermatologiczne', 'D'),

-- G
('G01', 'Leki przeciwzakaźne i antyseptyczne ginekologiczne', 'G'),
('G02', 'Inne leki ginekologiczne', 'G'),
('G03', 'Hormony płciowe i modulatory układu płciowego', 'G'),
('G04', 'Leki urologiczne', 'G'),

-- H
('H01', 'Hormony przysadki, podwzgórza i ich analogi', 'H'),
('H02', 'Kortykosteroidy do stosowania wewnętrznego', 'H'),
('H03', 'Preparaty tarczycowe', 'H'),
('H04', 'Hormony trzustki', 'H'),
('H05', 'Preparaty wapnia do regulacji gospodarki hormonalnej', 'H'),

-- J
('J01', 'Leki przeciwbakteryjne (antybiotyki)', 'J'),
('J02', 'Leki przeciwgrzybicze', 'J'),
('J04', 'Leki przeciwprątkowe', 'J'),
('J05', 'Leki przeciwwirusowe', 'J'),
('J06', 'Surowice i immunoglobuliny', 'J'),
('J07', 'Szczepionki', 'J'),

-- L
('L01', 'Cytostatyki', 'L'),
('L02', 'Leki hormonalne', 'L'),
('L03', 'Immunostymulanty', 'L'),
('L04', 'Immunosupresanty', 'L'),

-- M
('M01', 'Leki przeciwzapalne i przeciwreumatyczne', 'M'),
('M02', 'Preparaty miejscowe przeciwzapalne i przeciwreumatyczne', 'M'),
('M03', 'Leki zwiotczające mięśnie', 'M'),
('M04', 'Leki przeciw dnie', 'M'),
('M05', 'Leki stosowane w chorobach układu kostnego', 'M'),
('M09', 'Inne leki stosowane w zaburzeniach układu mięśniowo-szkieletowego', 'M'),

-- N
('N01', 'Leki znieczulające', 'N'),
('N02', 'Leki przeciwbólowe', 'N'),
('N03', 'Leki przeciwpadaczkowe', 'N'),
('N04', 'Leki przeciw chorobie Parkinsona', 'N'),
('N05', 'Leki psycholeptyczne', 'N'),
('N06', 'Psychoanaleptyki', 'N'),
('N07', 'Inne leki wpływające na układ nerwowy', 'N'),

-- P
('P01', 'Leki przeciwpierwotniakowe', 'P'),
('P02', 'Leki przeciwrobacze', 'P'),
('P03', 'Środki przeciw pasożytom zewnętrznym', 'P'),

-- R
('R01', 'Leki stosowane w chorobach nosa', 'R'),
('R02', 'Leki stosowane w chorobach gardła', 'R'),
('R03', 'Leki stosowane w obturacyjnych chorobach dróg oddechowych', 'R'),
('R05', 'Leki stosowane w kaszlu i przeziębieniu', 'R'),
('R06', 'Leki przeciwhistaminowe do stosowania wewnętrznego', 'R'),
('R07', 'Inne preparaty stosowane w chorobach układu oddechowego', 'R'),

-- S
('S01', 'Leki oftalmologiczne (okulistyczne)', 'S'),
('S02', 'Leki otologiczne', 'S'),
('S03', 'Leki oftalmologiczne oraz otologiczne', 'S'),

-- V
('V01', 'Alergeny', 'V'),
('V03', 'Pozostałe produkty lecznicze', 'V'),
('V04', 'Środki diagnostyczne', 'V'),
('V06', 'Preparaty dietetyczne', 'V'),
('V07', 'Wszystkie inne preparaty nieterapeutuczne', 'V'),
('V08', 'Środki cieniuące (kontrastowe)', 'V'),
('V09', 'Radiofarmaceutyki diagnostyczne', 'V'),
('V10', 'Radiofarmaceutyki lecznicze', 'V'),
('V20', 'Inne', 'V');