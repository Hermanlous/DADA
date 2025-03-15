
-- 1. FLYPLASSER 
INSERT INTO Flyplass (FlyplassKode, FlyplassNavn) VALUES 
('BOO', 'Bodø Lufthavn'),
('BGO', 'Bergen Lufthavn, Flesland'),
('OSL', 'Oslo Lufthavn, Gardermoen'),
('SVG', 'Stavanger Lufthavn, Sola'),
('TRD', 'Trondheim Lufthavn, Værnes');

-- 2. FLYSELSKAPER 
INSERT INTO Flyselskap (FlyselskapsKode, SelskapsNavn) VALUES 
('DY', 'Norwegian'),
('SK', 'SAS'),
('WF', 'Widerøe');


-- 3. FLYPRODUSENTER 
INSERT INTO FlyProdusent (ProdusentNavn, Nasjonalitet, Stiftelsesaar) VALUES 
('The Boeing Company', 'USA', 1916),
('Airbus Group', 'Frankrike/Tyskland/Spania/Storbritannia', 1970),
('De Havilland Canada', 'Canada', 1928);

-- 4. FLYTYPER 

INSERT INTO FlyType (FlyTypeNavn, ProdusentNavn, FoersteProduksjonsAar, SisteProduksjonsAar) VALUES 
('Boeing 737 800', 'The Boeing Company', 1997, 2020),
('Airbus a320neo', 'Airbus Group', 2016, NULL),  -- Fortsatt i produksjon
('Dash-8 100', 'De Havilland Canada', 1984, 2005);


INSERT INTO Flaate (FlyselskapsKode) VALUES 
('DY'),  -- Norwegian
('SK'),  -- SAS
('WF');  -- Widerøe


-- Norwegian fly
INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, Navn, DriftAar) VALUES 
('LN-ENU', 1, 'Boeing 737 800', NULL, 2015),
('LN-ENR', 1, 'Boeing 737 800', 'Jan Bålsrud', 2018),
('LN-NIQ', 1, 'Boeing 737 800', 'Max Manus', 2011),
('LN-ENS', 1, 'Boeing 737 800', NULL, 2017);

-- SAS fly
INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, Navn, DriftAar) VALUES 
('SE-RUB', 2, 'Airbus a320neo', 'Birger Viking', 2020),
('SE-DIR', 2, 'Airbus a320neo', 'Nora Viking', 2023),
('SE-RUP', 2, 'Airbus a320neo', 'Ragnhild Viking', 2024),
('SE-RZE', 2, 'Airbus a320neo', 'Ebbe Viking', 2024);

-- Widerøe fly
INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, Navn, DriftAar) VALUES 
('LN-WIH', 3, 'Dash-8 100', 'Oslo', 1994),
('LN-WIA', 3, 'Dash-8 100', 'Nordland', 1993),
('LN-WIL', 3, 'Dash-8 100', 'Narvik', 1995);


INSERT INTO SerienummerertAv (Registreringsnummer, ProdusentNavn, Serienummer) VALUES 
('LN-ENU', 'The Boeing Company', '42069'),
('LN-ENR', 'The Boeing Company', '42093'),
('LN-NIQ', 'The Boeing Company', '39403'),
('LN-ENS', 'The Boeing Company', '42281'),
('SE-RUB', 'Airbus Group', '9518'),
('SE-DIR', 'Airbus Group', '11421'),
('SE-RUP', 'Airbus Group', '12066'),
('SE-RZE', 'Airbus Group', '12166'),
('LN-WIH', 'De Havilland Canada', '383'),
('LN-WIA', 'De Havilland Canada', '359'),
('LN-WIL', 'De Havilland Canada', '298');


-- For Boeing 737 800 (Norwegian) - LN-ENU


INSERT INTO Sete (RegistreringsNummer, Rad, Bokstav, NoedUtgang) VALUES 
('LN-ENU', 1, 'A', 0),
('LN-ENU', 1, 'B', 0),
('LN-ENU', 1, 'C', 0),
('LN-ENU', 1, 'D', 0),
('LN-ENU', 1, 'E', 0),
('LN-ENU', 1, 'F', 0);

-- Rad 13 (nødutgang)
INSERT INTO Sete (RegistreringsNummer, Rad, Bokstav, NoedUtgang) VALUES 
('LN-ENU', 13, 'A', 1),
('LN-ENU', 13, 'B', 1),
('LN-ENU', 13, 'C', 1),
('LN-ENU', 13, 'D', 1),
('LN-ENU', 13, 'E', 1),
('LN-ENU', 13, 'F', 1);

-- For Airbus a320neo (SAS) - SE-RUB

INSERT INTO Sete (RegistreringsNummer, Rad, Bokstav, NoedUtgang) VALUES 
('SE-RUB', 1, 'A', 0),
('SE-RUB', 1, 'B', 0),
('SE-RUB', 1, 'C', 0),
('SE-RUB', 1, 'D', 0),
('SE-RUB', 1, 'E', 0),
('SE-RUB', 1, 'F', 0);


INSERT INTO Sete (RegistreringsNummer, Rad, Bokstav, NoedUtgang) VALUES 
('SE-RUB', 11, 'A', 1),
('SE-RUB', 11, 'B', 1),
('SE-RUB', 11, 'C', 1),
('SE-RUB', 11, 'D', 1),
('SE-RUB', 11, 'E', 1),
('SE-RUB', 11, 'F', 1),
('SE-RUB', 12, 'A', 1),
('SE-RUB', 12, 'B', 1),
('SE-RUB', 12, 'C', 1),
('SE-RUB', 12, 'D', 1),
('SE-RUB', 12, 'E', 1),
('SE-RUB', 12, 'F', 1);


INSERT INTO Sete (RegistreringsNummer, Rad, Bokstav, NoedUtgang) VALUES 
('LN-WIH', 1, 'C', 0),
('LN-WIH', 1, 'D', 0);

INSERT INTO Sete (RegistreringsNummer, Rad, Bokstav, NoedUtgang) VALUES 
('LN-WIH', 2, 'A', 0),
('LN-WIH', 2, 'B', 0),
('LN-WIH', 2, 'C', 0),
('LN-WIH', 2, 'D', 0);

INSERT INTO Sete (RegistreringsNummer, Rad, Bokstav, NoedUtgang) VALUES 
('LN-WIH', 5, 'A', 1),
('LN-WIH', 5, 'B', 1),
('LN-WIH', 5, 'C', 1),
('LN-WIH', 5, 'D', 1);


INSERT INTO FlyRute (FlyRuteNummer, OppstartDato, SluttDato, Ukedagskode) VALUES 
('WF1311', '2025-01-01', NULL, '12345'),   -- TRD-BOO, mandag til fredag
('WF1302', '2025-01-01', NULL, '12345'),   -- BOO-TRD, mandag til fredag
('DY753', '2025-01-01', NULL, '1234567'),  -- TRD-OSL, alle dager
('SK332', '2025-01-01', NULL, '1234567'),  -- OSL-TRD, alle dager
('SK888', '2025-01-01', NULL, '12345'),    -- TRD-BGO, mandag til fredag
('SK889', '2025-01-01', NULL, '12345');    -- BGO-SVG, mandag til fredag (del av SK888)


INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeFra, FlyplassKodeTil, PlanlagtAvgang, PlanlagtAnkomst) VALUES 
('1', 'WF1311', 'TRD', 'BOO', '15:15', '16:20'),  -- TRD-BOO
('1', 'WF1302', 'BOO', 'TRD', '07:35', '08:40'),  -- BOO-TRD
('1', 'DY753', 'TRD', 'OSL', '10:20', '11:15'),   -- TRD-OSL
('1', 'SK332', 'OSL', 'TRD', '08:00', '09:05'),   -- OSL-TRD
('1', 'SK888', 'TRD', 'BGO', '10:00', '11:10'),   -- TRD-BGO
('2', 'SK888', 'BGO', 'SVG', '11:40', '12:10');   -- BGO-SVG (del av samme rute)


-- WF1311: TRD-BOO
INSERT INTO Pris (KlasseID, FlyRuteNummer, MellomLandingID, PrisForKlasse) VALUES 
('premium', 'WF1311', '1', 2018),
('økonomi', 'WF1311', '1', 899),
('budsjett', 'WF1311', '1', 599);

-- WF1302: BOO-TRD
INSERT INTO Pris (KlasseID, FlyRuteNummer, MellomLandingID, PrisForKlasse) VALUES 
('premium', 'WF1302', '1', 2018),
('økonomi', 'WF1302', '1', 899),
('budsjett', 'WF1302', '1', 599);

-- DY753: TRD-OSL
INSERT INTO Pris (KlasseID, FlyRuteNummer, MellomLandingID, PrisForKlasse) VALUES 
('premium', 'DY753', '1', 1500),
('økonomi', 'DY753', '1', 1000),
('budsjett', 'DY753', '1', 500);

-- SK332: OSL-TRD
INSERT INTO Pris (KlasseID, FlyRuteNummer, MellomLandingID, PrisForKlasse) VALUES 
('premium', 'SK332', '1', 1500),
('økonomi', 'SK332', '1', 1000),
('budsjett', 'SK332', '1', 500);

-- SK888: TRD-BGO
INSERT INTO Pris (KlasseID, FlyRuteNummer, MellomLandingID, PrisForKlasse) VALUES 
('premium', 'SK888', '1', 2000),
('økonomi', 'SK888', '1', 1500),
('budsjett', 'SK888', '1', 800);

-- SK888: BGO-SVG
INSERT INTO Pris (KlasseID, FlyRuteNummer, MellomLandingID, PrisForKlasse) VALUES 
('premium', 'SK888', '2', 1000),
('økonomi', 'SK888', '2', 700),
('budsjett', 'SK888', '2', 350);


INSERT INTO Flyvning (LøpeNummer, FlyRuteNummer, MellomLandingID, RegistreringsNummer, Status, Avgang, Ankomst) VALUES 
(1, 'WF1302', '1', 'LN-WIH', 'Planlagt', '07:35', '08:40'),  -- Widerøe BOO-TRD
(1, 'DY753', '1', 'LN-ENU', 'Planlagt', '10:20', '11:15'),   -- Norwegian TRD-OSL
(1, 'SK888', '1', 'SE-RUB', 'Planlagt', '10:00', '11:10'),   -- SAS TRD-BGO
(1, 'SK888', '2', 'SE-RUB', 'Planlagt', '11:40', '12:10');   -- SAS BGO-SVG (del av samme rute)



INSERT INTO FlyddAv (FlyRuteNummer, LøpeNummer, FlaateID) VALUES 
('WF1302', 1, 3),  -- Widerøe BOO-TRD
('DY753', 1, 1),   -- Norwegian TRD-OSL
('SK888', 1, 2);   -- SAS TRD-BGO(-SVG)


INSERT INTO Kunde (Navn, Telefon, Epost, Nasjonalitet) VALUES 
('Ola Nordmann', '99988777', 'ola.nordmann@email.no', 'Norsk');


INSERT INTO Billettkjop (KundeID, Kostnad) VALUES 
(1, 2018), 
(1, 2018), 
(1, 899),  
(1, 899),  
(1, 899),  
(1, 899),  
(1, 599),  
(1, 599),  
(1, 599),  
(1, 599);  


INSERT INTO Billett (LøpeNummer, FlyRuteNummer, ReferanseNummerTur, ReferanseNummerRetur, Innsjekking, Kategori) VALUES 
(1, 'WF1302', 1, NULL, NULL, 'premium'),
(1, 'WF1302', 2, NULL, NULL, 'premium'),
(1, 'WF1302', 3, NULL, NULL, 'økonomi'),
(1, 'WF1302', 4, NULL, NULL, 'økonomi'),
(1, 'WF1302', 5, NULL, NULL, 'økonomi'),
(1, 'WF1302', 6, NULL, NULL, 'økonomi'),
(1, 'WF1302', 7, NULL, NULL, 'budsjett'),
(1, 'WF1302', 8, NULL, NULL, 'budsjett'),
(1, 'WF1302', 9, NULL, NULL, 'budsjett'),
(1, 'WF1302', 10, NULL, NULL, 'budsjett');


INSERT INTO TilhorendeSete (BillettID, SeteID) VALUES 
(1, 1),  
(2, 2),  
(3, 3),  
(4, 4),  
(5, 5),  
(6, 6),  
(7, 7),  
(8, 8),  
(9, 9),  
(10, 10); 

-- 7. Bestilling av billetter på samme person

INSERT INTO Kunde (Navn, Telefon, Epost, Nasjonalitet)
SELECT 'Ola Nordmann', '99988777', 'ola.nordmann@example.no', 'Norsk'
WHERE NOT EXISTS (SELECT 1 FROM Kunde WHERE Navn = 'Ola Nordmann');

INSERT INTO Billettkjop (KundeID, Kostnad) VALUES 
(1, 2018), (1, 2018), 
(1, 899), (1, 899), (1, 899), (1, 899), 
(1, 599), (1, 599), (1, 599), (1, 599);

INSERT INTO Billett (LøpeNummer, FlyRuteNummer, ReferanseNummerTur, ReferanseNummerRetur, Innsjekking, Kategori) VALUES 
(1, 'WF1302', 1, NULL, NULL, NULL,'premium'),
(1, 'WF1302', 2, NULL, NULL, NULL ,'premium'),
(1, 'WF1302', 3, NULL, NULL, NULL,'økonomi'),
(1, 'WF1302', 4, NULL, NULL, NULL,'økonomi'),
(1, 'WF1302', 5, NULL, NULL, NULL,'økonomi'),
(1, 'WF1302', 6, NULL, NULL, NULL,'økonomi'),
(1, 'WF1302', 7, NULL, NULL, NULL,'budsjett'),
(1, 'WF1302', 8, NULL, NULL, NULL,'budsjett'),
(1, 'WF1302', 9, NULL, NULL, NULL,'budsjett'),
(1, 'WF1302', 10, NULL, NULL, NULL,'budsjett');

INSERT INTO TilhorendeSete (BillettID, SeteID) VALUES 
(1, (SELECT SeteID FROM Sete WHERE RegistreringsNummer = 'LN-WIH' AND Rad = 1 AND Bokstav = 'C')),
(2, (SELECT SeteID FROM Sete WHERE RegistreringsNummer = 'LN-WIH' AND Rad = 1 AND Bokstav = 'D')),
(3, (SELECT SeteID FROM Sete WHERE RegistreringsNummer = 'LN-WIH' AND Rad = 2 AND Bokstav = 'A')),
(4, (SELECT SeteID FROM Sete WHERE RegistreringsNummer = 'LN-WIH' AND Rad = 2 AND Bokstav = 'B')),
(5, (SELECT SeteID FROM Sete WHERE RegistreringsNummer = 'LN-WIH' AND Rad = 2 AND Bokstav = 'C')),
(6, (SELECT SeteID FROM Sete WHERE RegistreringsNummer = 'LN-WIH' AND Rad = 2 AND Bokstav = 'D')),
(7, (SELECT SeteID FROM Sete WHERE RegistreringsNummer = 'LN-WIH' AND Rad = 5 AND Bokstav = 'A')),
(8, (SELECT SeteID FROM Sete WHERE RegistreringsNummer = 'LN-WIH' AND Rad = 5 AND Bokstav = 'B')),
(9, (SELECT SeteID FROM Sete WHERE RegistreringsNummer = 'LN-WIH' AND Rad = 5 AND Bokstav = 'C')),
(10, (SELECT SeteID FROM Sete WHERE RegistreringsNummer = 'LN-WIH' AND Rad = 5 AND Bokstav = 'D'));