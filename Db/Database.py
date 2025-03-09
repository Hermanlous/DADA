import sqlite3
import os

def opprett_flydatabase(db_navn='flydatabase.db'):

    if os.path.exists(db_navn):
        os.remove(db_navn)

    conn = sqlite3.connect(db_navn)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute('''
        CREATE TABLE Flyplass (
            FlyplassKode TEXT PRIMARY KEY,
            FlyplassNavn TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE MellomReise (
            MellomLandingID TEXT,
            FlyRuteNummer TEXT,
            FlyplassKodeTil TEXT,
            FlyplassKodeFra TEXT,
            PlanlagtAvgang TEXT NOT NULL,
            PlanlagtAnkomst TEXT NOT NULL,
            PRIMARY KEY (MellomLandingID, FlyruteNummer),
            FOREIGN KEY (FlyplassKodeFra) REFERENCES Flyplass(FlyplassKode),
            FOREIGN KEY (FlyplassKodeTil) REFERENCES Flyplass(FlyplassKode),
            FOREIGN KEY (FlyRuteNummer) REFERENCES FlyRute(FlyRuteNummer)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Flyselskap (
            FlyselskapKode TEXT PRIMARY KEY,
            SelskapsNavn TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE FlyRute (
        FlyRuteNummer TEXT PRIMARY KEY,
        OppstartDato TEXT NOT NULL, 
        SluttDato TEXT,
        Ukedagskode TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE Flaate (
            FlaateID INTEGER PRIMARY KEY AUTOINCREMENT,
            FlyselskapKode TEXT,
            FOREIGN KEY (FlyselskapKode) REFERENCES Flyselskap(FlyselskapKode)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Fly (
            RegistreringsNummer TEXT PRIMARY KEY,
            FlaateID TEXT,
            FlyTypeNavn TEXT,
            ProdusentNavn TEXT,
            Navn TEXT,
            DriftAar INTEGER NOT NULL,
            FOREIGN KEY (FlaateID) REFERENCES Flåte(FlaateID),
            FOREIGN KEY (FlyTypeNavn) REFERENCES FlyType(FlyTypeNavn),
            FOREIGN KEY (ProdusentNavn) REFERENCES FlyProdusent(ProdusentNavn)
        )
    ''')

    cursor.execute('''
        CREATE TABLE FlyProdusent (
            ProdusentNavn TEXT PRIMARY KEY,
            Nasjonalitet TEXT NOT NULL,
            Stiftelsesaar INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE FlyType (
            FlyTypeNavn TEXT PRIMARY KEY,
            ProdusentNavn TEXT,
            FoersteProduksjonsAar INTEGER NOT NULL,
            SisteProduksjonsAar INTEGER,
            FOREIGN KEY (ProdusentNavn) REFERENCES FlyProdusent(ProdusentNavn)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Sete (
            SeteID TEXT PRIMARY KEY,
            RegistreringsNummer TEXT,
            Rad INTEGER NOT NULL,
            Bokstav CHAR NOT NULL,
            FOREIGN KEY (RegistreringsNummer) REFERENCES Fly(RegistreringsNummer)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Kunde (
            KundeID TEXT PRIMARY KEY,
            Navn TEXT NOT NULL,
            Telefon TEXT NOT NULL,
            Epost TEXT NOT NULL,
            Nasjonalitet TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE Fordelsprogram (
            PK TEXT PRIMARY KEY
        )
    ''')

    cursor.execute('''
        CREATE TABLE Baggasje (
            BaggasjeID TEXT PRIMARY KEY,
            BillettID TEXT,
            Vekt INTEGER NOT NULL,
            InnleveringsTidspunkt TEXT NOT NULL,
            FOREIGN KEY (BillettID) REFERENCES Billett(BillettID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Flyvning (
            LøpeNummer INTEGER NOT NULL,
            FlyRuteNummer TEXT NOT NULL,
            MellomLandingID TEXT,
            RegistreringsNummer TEXT,
            Status TEXT NOT NULL CHECK (Status IN ('Planlagt', 'Aktiv', 'Fullført', 'Kansellert')),
            Avgang TEXT,
            Ankomst TEXT,
            PRIMARY KEY (LøpeNummer, FlyRuteNummer),
            FOREIGN KEY (MellomLandingID, FlyRuteNummer) REFERENCES MellomReise(MellomLandingID, FlyRuteNummer),
            FOREIGN KEY (RegistreringsNummer) REFERENCES Fly(RegistreringsNummer)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Pris (
            KlasseID TEXT NOT NULL,
            FlyRuteNummer TEXT NOT NULL,
            MellomLandingID TEXT NOT NULL,
            Pris TEXT NOT NULL,
            PRIMARY KEY (KlasseID, FlyRuteNummer, MellomLandingID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Billett (
            BillettID TEXT PRIMARY KEY NOT NULL,
            LøpeNummer TEXT NOT NULL,
            FlyRuteNummer TEXT NOT NULL,
            ReferanseNummerTur TEXT NOT NULL,
            ReferanseNummerRetur TEXT NOT NULL,
            Innsjekking TEXT NOT NULL,
            Kategori TEXT NOT NULL CHECK (Kategori IN ('premium', 'økonomi', 'budsjett')),
            FOREIGN KEY (LøpeNummer, FlyRuteNummer) REFERENCES Flyvning(LøpeNummer, FlyRuteNummer),
            FOREIGN KEY (ReferanseNummerTur) REFERENCES Billettkjop(ReferanseNummer),
            FOREIGN KEY (ReferanseNummerRetur) REFERENCES Billettkjop(ReferanseNummer)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Billettkjop (
            ReferanseNummer TEXT PRIMARY KEY,
            KundeID TEXT,
            Pris DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (KundeID) REFERENCES Kunde(KundeID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE TilhorendeSete (
            BillettID TEXT,
            SeteID TEXT,
            PRIMARY KEY (BillettID, SeteID),
            FOREIGN KEY (BillettID) REFERENCES Billett(BillettID),
            FOREIGN KEY (SeteID) REFERENCES Sete(SeteID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Medlem (
            KundeID TEXT PRIMARY KEY,
            UnikFordelsRef TEXT,
            FOREIGN KEY (KundeID) REFERENCES Kunde(KundeID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE FlyddAv (
            FlyRuteNummer TEXT PRIMARY KEY,
            FlåteID TEXT,
            FOREIGN KEY (FlyRuteNummer) REFERENCES Flyvning(FlyRuteNummer),
            FOREIGN KEY (FlåteID) REFERENCES Flåte(FlåteID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE DrivesAv (
            FlyselskapKode TEXT PRIMARY KEY,
            FordelsprogramID TEXT,
            FOREIGN KEY (FlyselskapKode) REFERENCES Flyselskap(FlyselskapKode),
            FOREIGN KEY (FordelsprogramID) REFERENCES Fordelsprogram(PK)
        )
    ''')

    cursor.execute('''
        CREATE TABLE SerienummerertAv (
            ProdusentNavn TEXT,
            Registreringsnummer TEXT,
            Serienummer TEXT,
            PRIMARY KEY (ProdusentNavn, Registreringsnummer),
            FOREIGN KEY (ProdusentNavn) REFERENCES FlyProdusent(ProdusentNavn),
            FOREIGN KEY (Registreringsnummer) REFERENCES Fly(RegistreringsNummer)
        )
    ''')

    conn.commit()
    conn.close()

def legg_inn_data(db_navn='flydatabase.db'):

    conn = sqlite3.connect(db_navn)
    cursor = conn.cursor()
    
    # 1. Flyplasser

    cursor.execute(
        "INSERT INTO Flyplass (FlyplassKode, FlyplassNavn) VALUES ('BOO', 'Bodø Lufthavn')"
    ),
    cursor.execute(
        "INSERT INTO Flyplass (FlyplassKode, FlyplassNavn) VALUES ('BGO', 'Bergen lufthavn, Fesland')"
    )
    cursor.execute(
        "INSERT INTO Flyplass (FlyplassKode, FlyplassNavn) VALUES ('OSL', 'Oslo lufthavn, Gardermoen')"
    )
    cursor.execute(
        "INSERT INTO Flyplass (FlyplassKode, FlyplassNavn) VALUES ('SVG', 'Stavanger lufthavn, Sola')"
    )
    cursor.execute(
        "INSERT INTO Flyplass (FlyplassKode, FlyplassNavn) VALUES ('TRD', 'Trondheim lufthavn, Værnes')"
    )

    # 2. Flyprodusenter

    cursor.execute(
        "INSERT INTO Flyprodusent (ProdusentNavn, Nasjonalitet, Stiftelsesaar) VALUES ('The Boeing Company', 'USA', 1916)"

    )
    cursor.execute(
        "INSERT INTO Flyprodusent (ProdusentNavn, Nasjonalitet, Stiftelsesaar) VALUES ('Airbus Group', 'Europa', 1970)"

    )
    cursor.execute(
        "INSERT INTO Flyprodusent (ProdusentNavn, Nasjonalitet, Stiftelsesaar) VALUES ('De Havilland Canada', 'Canada', 1928)"

    )
    
    # 3. Flytyper

    cursor.execute(
        "INSERT INTO Flytype (FlyTypeNavn, ProdusentNavn, FoersteProduksjonsAar, SisteProduksjonsAar) VALUES ('Boeing 737 800', 'The Boeing Company', 1997, 2020)",
    )
    cursor.execute(
        "INSERT INTO Flytype (FlyTypeNavn, ProdusentNavn, FoersteProduksjonsAar, SisteProduksjonsAar) VALUES ('Airbus a320neo', 'Airbus Group', 2016, NULL)",
    )
    cursor.execute(
        "INSERT INTO Flytype (FlyTypeNavn, ProdusentNavn, FoersteProduksjonsAar, SisteProduksjonsAar) VALUES ('Dash-8 100', 'De Havilland Canada', 1984, 2005)",
    )
    
    # 4. Flyselskaper

    cursor.execute(
        "INSERT INTO Flyselskap (FlyselskapKode, SelskapsNavn) VALUES ('DY', 'Norwegian')"
    )
    cursor.execute(
        "INSERT INTO Flyselskap (FlyselskapKode, SelskapsNavn) VALUES ('SK', 'SAS')"
    )
    cursor.execute(
        "INSERT INTO Flyselskap (FlyselskapKode, SelskapsNavn) VALUES ('WF', 'Widerøe')"
    )
    
    # 5. Fly
    # Norwegian
    # KAnskje generere FlåteID? Autoincrement?
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-ENU', 1, 'Boeing 737 800', 'The Boeing Company', NULL, 2015)",
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-ENR', 1, 'Boeing 737 800', 'The Boeing Company', 'Jan Bålsrud', 2018)",
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-NIQ', 1, 'Boeing 737 800', 'The Boeing Company', 'Max Manus', 2011)",
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-ENS', 1, 'Boeing 737 800', 'The Boeing Company', NULL, 2017)",
    )
    # SAS
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('SE-RUB', 2, 'Airbus a320neo', 'Airbus Group', 'Birger Viking', 2020)",
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('SE-DIR', 2, 'Airbus a320neo', 'Airbus Group', 'Nora Viking', 2023)",
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('SE-RUP', 2, 'Airbus a320neo', 'Airbus Group', 'Ragnhild Viking', 2024)",
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('SE-RZE', 2, 'Airbus a320neo', 'Airbus Group', 'Ebbe Viking', 2024)",
    )

    # Widerøe
    #Autoincrement FlåteID
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-WIH', 3, 'Dash-8 100', 'De Havilland Canada', 'Oslo', 1994)",
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-WIA', 3, 'Dash-8 100', 'De Havilland Canada', 'Nordland', 1993)",
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-WIL', 3, 'Dash-8 100', 'De Havilland Canada', 'Narvik', 1995)",
    )

    
    # 7. Flyruter
    # Start dato
    cursor.execute(
        "INSERT INTO FlyRute (FlyRuteNummer, OppstartDato, SluttDato, Ukedagskode) VALUES ('WF1311', '12.01.2001', NULL, '12345')",
    )
    cursor.execute(
        "INSERT INTO FlyRute (FlyRuteNummer, OppstartDato, SluttDato, Ukedagskode) VALUES ('WF1302', '12.01.2001', NULL, '12345')",
    )
    cursor.execute(
        "INSERT INTO FlyRute (FlyRuteNummer, OppstartDato, SluttDato, Ukedagskode) VALUES ('DY753', '12.01.2001', NULL, '1234567')",
    )
    cursor.execute(
        "INSERT INTO FlyRute (FlyRuteNummer, OppstartDato, SluttDato, Ukedagskode) VALUES ('SK332', '12.01.2001', NULL, '1234567')",
    )
    cursor.execute(
        "INSERT INTO FlyRute (FlyRuteNummer, OppstartDato, SluttDato, Ukedagskode) VALUES ('SK888', '12.01.2001', NULL, '12345')",
    )
    
    # 8. Legger inn reiser
    # SK888
    cursor.execute("""
        INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('TRD-BGO', 'BGO', 'TRD','SK888', '10:00', '11:10')
    """)
    cursor.execute("""
        INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('BGO-SVG', 'SVG', 'BGO','SK888', '11:40', '12:10')
        """)

    cursor.execute("""
            INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('TRD-BGO-SVG', 'SVG', 'TRD','SK888', '10:00', '12:10')
            """)
    # SK332
    cursor.execute("""
            INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('OSL-TRD', 'TRD', 'OSL','SK332', '08:00', '09:05')
        """)
    # DY753
    cursor.execute("""
            INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('TRD-OSL', 'OSL', 'TRD','DY753', '10:20', '11:15')
        """)
    # WF1302
    cursor.execute("""
            INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('BOO-TRD', 'TRD', 'BOO','WF1302', '07:35', '08:40')
        """)
    # WF1311
    cursor.execute("""
            INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('TRD-BOO', 'BOO', 'TRD','WF1311', '15:15', '16:20')
            """)
    
    # 9. Priser
    # SK888
    #
    cursor.execute(
        "INSERT INTO Pris (KlasseID, FlyRuteNummer, MellomLandingID, pris) VALUES ('premium','SK888','TRD-BGO-SVG', 2200  )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('økonomi','SK888','TRD-BGO-SVG', 1700 )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('budsjett','SK888','TRD-BGO-SVG', 1000 )"

    )
    #TRD-BGO
    cursor.execute(
        "INSERT INTO Pris (KlasseID, FlyRuteNummer, MellomLandingID, pris) VALUES ('premium','SK888','TRD-BGO', 2000  )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('økonomi','SK888', 'TRD-BGO', 1500 )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('budsjett','SK888','TRD-BGO', 800 )"

    )
    #BGO-SVG
    cursor.execute(
        "INSERT INTO Pris (KlasseID, FlyRuteNummer, MellomLandingID, pris) VALUES ('premium','SK888','BGO-SVG', 1000  )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('økonomi','SK888','BGO-SVG',700 )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('budsjett','SK888','BGO-SVG', 350 )"

    )
    # SK322
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('premium','SK322','OSL-TRD', 1500 )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('økonomi','SK322','OSL-TRD', 1000 )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('budsjett', 'SK322','OSL-TRD', 500)"

    )
    # DY753
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('premium','DY753','TRD-OSL', 1500 )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('økonomi','DY753','TRD-OSL',1000 )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('budsjett','DY753','TRD-OSL', 500)"

    )
    # WF1302
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('premium','WF1302','BOO-TRD', 2018 )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('økonomi','WF1302','BOO-TRD', 899 )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('budsjett','WF1302','BOO-TRD', 599 )"

    )
    # WF1311
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('premium','WF1311','TRD-BOO', 2018 )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('økonomi','WF1311','TRD-BOO', 899 )"

    )
    cursor.execute(
        "INSERT INTO Pris (KlasseID,FlyRuteNummer, MellomLandingID,pris) VALUES ('budsjett','WF1311','TRD-BOO',599 )"

    )
    # 10. Flyrtuer for 1. april 2025
    # Autoincrement på LøpeNummer, skal vi bestemme fly?
    cursor.execute(
        "INSERT INTO Flyvning (LøpeNummer, FlyRuteNummer, MellomLandingID, RegistreringsNummer,Status, Avgang, Ankomst) VALUES (1, 'WF1302', 'BOO-TRD', 'LN-ENU', 'Planlagt',NULL, NULL)"
    )
    cursor.execute(
        "INSERT INTO Flyvning (LøpeNummer, FlyRuteNummer, MellomLandingID, RegistreringsNummer,Status, Avgang, Ankomst) VALUES (2, 'DY753', 'TRD-OSL', 'SE-RUB', 'Planlagt', NULL, NULL)"
    )
    cursor.execute(
        "INSERT INTO Flyvning (LøpeNummer, FlyRuteNummer, MellomLandingID, RegistreringsNummer,Status, Avgang, Ankomst) VALUES (3, 'SK888', 'TRD-BGO-SVG', 'LN-WIH', 'Planlagt',NULL, NULL)"
    )


    conn.commit()
    conn.close()
opprett_flydatabase()
legg_inn_data()



