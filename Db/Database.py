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
            PRIMARY KEY (MellomLandingID, FlyRuteNummer),
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
            FOREIGN KEY (FlaateID) REFERENCES Flaate(FlaateID),
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
            SeteID INTEGER PRIMARY KEY AUTOINCREMENT,
            RegistreringsNummer TEXT,
            Rad INTEGER NOT NULL,
            Bokstav CHAR NOT NULL,
            NoedUtgang INTEGER NOT NULL CHECK (NoedUtgang IN (0,1)),
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
            FlyRuteNummer INTEGER NOT NULL,
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
            BillettID INTEGER PRIMARY KEY AUTOINCREMENT,
            LøpeNummer INTEGER NOT NULL,
            FlyRuteNummer INTEGER NOT NULL,
            ReferanseNummerTur INTEGER NOT NULL,
            ReferanseNummerRetur INTEGER,
            Innsjekking TEXT,
            Kategori TEXT NOT NULL CHECK (Kategori IN ('premium', 'økonomi', 'budsjett')),
            FOREIGN KEY (LøpeNummer, FlyRuteNummer) REFERENCES Flyvning(LøpeNummer, FlyRuteNummer),
            FOREIGN KEY (ReferanseNummerTur) REFERENCES Billettkjop(ReferanseNummer),
            FOREIGN KEY (ReferanseNummerRetur) REFERENCES Billettkjop(ReferanseNummer)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Billettkjop (
            ReferanseNummer INTEGER PRIMARY KEY,
            KundeID INTEGER,
            Pris INTEGER NOT NULL,
            FOREIGN KEY (KundeID) REFERENCES Kunde(KundeID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE TilhorendeSete (
            BillettID INTEGER,
            SeteID INTEGER,
            PRIMARY KEY (BillettID, SeteID),
            FOREIGN KEY (BillettID) REFERENCES Billett(BillettID),
            FOREIGN KEY (SeteID) REFERENCES Sete(SeteID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Medlem (
            KundeID INTEGER PRIMARY KEY,
            UnikFordelsRef TEXT,
            FOREIGN KEY (KundeID) REFERENCES Kunde(KundeID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE FlyddAv (
            FlyRuteNummer TEXT PRIMARY KEY,
            FlaateID TEXT,
            FOREIGN KEY (FlyRuteNummer) REFERENCES Flyvning(FlyRuteNummer),
            FOREIGN KEY (FlaateID) REFERENCES Flaate(FlaateID)
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
    cursor.execute("PRAGMA foreign_keys = ON")
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
    conn.commit()
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
    conn.commit()
    # 3. Flytyper

    cursor.execute(
        "INSERT INTO Flytype (FlyTypeNavn, ProdusentNavn, FoersteProduksjonsAar, SisteProduksjonsAar) VALUES ('Boeing 737 800', 'The Boeing Company', 1997, 2020)"
    )
    cursor.execute(
        "INSERT INTO Flytype (FlyTypeNavn, ProdusentNavn, FoersteProduksjonsAar, SisteProduksjonsAar) VALUES ('Airbus a320neo', 'Airbus Group', 2016, NULL)"
    )
    cursor.execute(
        "INSERT INTO Flytype (FlyTypeNavn, ProdusentNavn, FoersteProduksjonsAar, SisteProduksjonsAar) VALUES ('Dash-8 100', 'De Havilland Canada', 1984, 2005)"
    )
    conn.commit()
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
    conn.commit()
    # Flåte
    cursor.execute(
        "INSERT INTO Flaate (FlaateID, FlyselskapKode) VALUES (1, 'DY')",
    )
    cursor.execute(
        "INSERT INTO Flaate (FlaateID, FlyselskapKode) VALUES (2, 'SK')",
    )
    cursor.execute(
        "INSERT INTO Flaate (FlaateID, FlyselskapKode) VALUES (3, 'WF')",
    )
    conn.commit()
    # 5. Fly
    # Norwegian
    # KAnskje generere FlåteID? Autoincrement?
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-ENU', 1, 'Boeing 737 800', 'The Boeing Company', NULL, 2015)"
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-ENR', 1, 'Boeing 737 800', 'The Boeing Company', 'Jan Bålsrud', 2018)"
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-NIQ', 1, 'Boeing 737 800', 'The Boeing Company', 'Max Manus', 2011)"
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-ENS', 1, 'Boeing 737 800', 'The Boeing Company', NULL, 2017)"
    )
    # SAS
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('SE-RUB', 2, 'Airbus a320neo', 'Airbus Group', 'Birger Viking', 2020)"
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('SE-DIR', 2, 'Airbus a320neo', 'Airbus Group', 'Nora Viking', 2023)"
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('SE-RUP', 2, 'Airbus a320neo', 'Airbus Group', 'Ragnhild Viking', 2024)"
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('SE-RZE', 2, 'Airbus a320neo', 'Airbus Group', 'Ebbe Viking', 2024)"
    )
    conn.commit()
    # Widerøe
    #Autoincrement FlåteID
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-WIH', 3, 'Dash-8 100', 'De Havilland Canada', 'Oslo', 1994)"
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-WIA', 3, 'Dash-8 100', 'De Havilland Canada', 'Nordland', 1993)"
    )
    cursor.execute(
        "INSERT INTO Fly (RegistreringsNummer, FlaateID, FlyTypeNavn, ProdusentNavn, Navn, DriftAar) VALUES ('LN-WIL', 3, 'Dash-8 100', 'De Havilland Canada', 'Narvik', 1995)"
    )
    conn.commit()
    
    # 7. Flyruter
    # Start dato
    cursor.execute(
        "INSERT INTO FlyRute (FlyRuteNummer, OppstartDato, SluttDato, Ukedagskode) VALUES ('WF1311', '12.01.2001', NULL, '12345')"
    )
    cursor.execute(
        "INSERT INTO FlyRute (FlyRuteNummer, OppstartDato, SluttDato, Ukedagskode) VALUES ('WF1302', '12.01.2001', NULL, '12345')"
    )
    cursor.execute(
        "INSERT INTO FlyRute (FlyRuteNummer, OppstartDato, SluttDato, Ukedagskode) VALUES ('DY753', '12.01.2001', NULL, '1234567')"
    )
    cursor.execute(
        "INSERT INTO FlyRute (FlyRuteNummer, OppstartDato, SluttDato, Ukedagskode) VALUES ('SK332', '12.01.2001', NULL, '1234567')"
    )
    cursor.execute(
        "INSERT INTO FlyRute (FlyRuteNummer, OppstartDato, SluttDato, Ukedagskode) VALUES ('SK888', '12.01.2001', NULL, '12345')"
    )
    conn.commit()
    # 8. Legger inn reiser
    # SK888
    cursor.execute("""
        INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('TRD-BGO','SK888', 'BGO', 'TRD', '10:00', '11:10')
    """)
    cursor.execute("""
        INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('BGO-SVG','SK888', 'SVG', 'BGO', '11:40', '12:10')
        """)

    cursor.execute("""
            INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('TRD-BGO-SVG','SK888', 'SVG', 'TRD', '10:00', '12:10')
            """)
    # SK332
    cursor.execute("""
            INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('OSL-TRD','SK332', 'TRD', 'OSL', '08:00', '09:05')
        """)
    # DY753
    cursor.execute("""
            INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('TRD-OSL','DY753', 'OSL', 'TRD', '10:20', '11:15')
        """)
    # WF1302
    cursor.execute("""
            INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('BOO-TRD','WF1302', 'TRD', 'BOO', '07:35', '08:40')
        """)
    # WF1311
    cursor.execute("""
            INSERT INTO MellomReise (MellomLandingID, FlyRuteNummer, FlyplassKodeTil, FlyplassKodeFra,  PlanlagtAvgang, PlanlagtAnkomst) VALUES ('TRD-BOO','WF1311', 'BOO', 'TRD', '15:15', '16:20')
            """)
    conn.commit()
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
    conn.commit()
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
    #Sete konfigurasjon.
    #ChatGPT ble benyttet for å rette feil og refaktorere koden riktig.
    # Boeing 737 800
    for rad in range(1, 33):  # Rows 1 to 31
        for sete in ['A', 'B', 'C', 'D', 'E', 'F']:
            nødUtgang = 1 if rad == 13 else 0

            cursor.executemany(
                "INSERT INTO Sete (RegistreringsNummer, Rad, Bokstav, NoedUtgang) VALUES (?, ?, ?, ?)",
                [
                    ('LN-ENU', rad, sete, nødUtgang),
                    ('LN-ENR', rad, sete, nødUtgang),
                    ('LN-NIQ', rad, sete, nødUtgang),
                    ('LN-ENS', rad, sete, nødUtgang)
                ]
            )
    #Airbus a320neo
    for rad in range(1, 31):
        for sete in ['A', 'B', 'C', 'D', 'E', 'F']:
            nødUtgang = 1 if rad == 12 or rad == 11 else 0

            cursor.executemany(
                "INSERT INTO Sete (RegistreringsNummer, Rad, Bokstav, NoedUtgang) VALUES (?, ?, ?, ?)",
                [
                    ('SE-RUB', rad, sete, nødUtgang),
                    ('SE-DIR', rad, sete, nødUtgang),
                    ('SE-RUP', rad, sete, nødUtgang),
                    ('SE-RZE', rad, sete, nødUtgang)
                ]
            )
    #Dash - 8 100
    # ChatGPT ble benyttet for å sette de første radene.
    for sete in ['C','D']:
        cursor.executemany(#Fra her, til
            "INSERT INTO Sete (RegistreringsNummer, Rad, Bokstav, NoedUtgang) VALUES (?, ?, ?, ?)",
            [
                ('LN-WIH', 1, sete, 0),
                ('LN-WIA', 1, sete, 0),
                ('LN-WIL', 1, sete, 0)
            ]
        )#Her

    for rad in range(2, 11):
        for sete in ['A', 'B', 'C', 'D']:
            nødUtgang = 1 if rad == 5 else 0

            cursor.executemany(
                "INSERT INTO Sete (RegistreringsNummer, Rad, Bokstav, NoedUtgang) VALUES (?, ?, ?, ?)",
                [
                    ('LN-WIH', rad, sete, nødUtgang),
                    ('LN-WIA', rad, sete, nødUtgang),
                    ('LN-WIL', rad, sete, nødUtgang)
                ]
            )
    conn.commit()
    conn.close()
opprett_flydatabase()
legg_inn_data()

def bruks_tilfelle_fem(db_navn='flydatabase.db'):
    conn = sqlite3.connect(db_navn)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    querry = """
        SELECT F.SelskapsNavn, T.FlyTypeNavn, COUNT(L.RegistreringsNummer) AS AntallFly
        FROM Fly L
        JOIN Flaate FL ON L.FlaateID = FL.FlaateID
        JOIN Flyselskap F ON FL.FlyselskapKode = F.FlyselskapKode
        JOIN FlyType T ON L.FlyTypeNavn = T.FlyTypeNavn
        GROUP BY F.SelskapsNavn, T.FlyTypeNavn;
    """

    cursor.execute(querry)
    resultater = cursor.fetchall()
    conn.close()
    return resultater

#print(bruks_tilfelle_fem())


def bruks_tilfelle_seks(db_navn='flydatabase.db'):
    flyplasser ={1: "Bodø lufthavn", 2: "Bergen lufthavn", 3: "Oslo lufthavn", 4: "Stavanger lufthavn", 5: "Trondheim lufthavn"}
    print('\n God dag kjære reisende, hvilken flyplass vil du reise fra? \n Du kan velge mellom: \n 1: Bode lufthavn \n 2: Bergen lufthavn \n 3: Oslo lufthavn \n 4: Stavanger lufthavn \n 5: Trondheim lufthavn \n ')
    flyplassValg = int(input("Svar med å skrive inn nummeret til flyplassen du velger. \n"))

    if flyplassValg in flyplasser:
        print("Du ønsker å fly fra " + flyplasser[flyplassValg])
    else:
        print("Dumming, du kan velge mellom 1-5.") # må sende dem tilbake til start her.
    
    ukedager = {1:"mandag", 2: "tirsdag", 3: "onsdag", 4: "torsdag", 5: "fredag", 6: "lørdag", 7: "søndag"}
    print("\n Hvilken ukedag er du interessert i? \n 1: Mandag \n 2: Tirsdag \n 3: Onsdag \n 4: Torsdag \n 5: Fredag \n 6: Lørdag \n 7: Søndag"  )
    ukedagValg = int(input("\nSvar med å skrive in nummeret på ukedagen du velger: \n"))

    if ukedagValg in ukedager:
        print("Du er interrisert i " + ukedager[ukedagValg] + "\n")
    else:
        print("Du kan velge mellom 1-7 dummen.") # Må sende dem tilbake til start her.

    an = {1: "Ankomster", 2: "Avganger"} #Hvis du kommer på et bedre navn enn "an" bare endre
    print ("Hva ønsker du å se? Du kan velge mellom \n 1: Avganger fra " + flyplasser[flyplassValg] + " på " + ukedager[ukedagValg] + "\n 2: Ankomster til " + flyplasser[flyplassValg] + " på " + ukedager[ukedagValg])
    anValg = int(input("\nSkriv inn nummeret til det du ønsker å se:\n"))

    if anValg == 1:
        print("Du ønsker å se avganger fra " + flyplasser[flyplassValg] + " på " + ukedager[ukedagValg])
    elif anValg == 2:
        print("Du ønsker å se ankomster til " + flyplasser[flyplassValg] + " på " + ukedager[ukedagValg])
    else:
        print("Du kan velge mellom 1 og 2 dummen") #Må sende tilbake til start


    return 0 # sånn at vscode ikke blir sint på meg. Fjern denne linjen hvis du ser den, da har Oline glemt å fjerne den. 

bruks_tilfelle_seks()

def bruks_tilfelle_syv(db_navn='flydatabase.db'):
    conn = sqlite3.connect(db_navn)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    OppretteKunde =[
        (1, 'August', '42424242', 'TooCoolForSchool@mail.com', 'Norge') # Stolt nederlender
    ]
    sql_query_ny_kunde = """
    INSERT INTO Kunde VALUES (?, ?, ?, ?, ?)
    """
    cursor.executemany(sql_query_ny_kunde, OppretteKunde)
    BillettKjopAvEnKunde = [
        (1, 1, 599)

    ]

    sql_query_kjop = """
    INSERT INTO BillettKjop (ReferanseNummer, KundeID, Pris) VALUES (?, ?, ?)
    """
    cursor.executemany(sql_query_kjop, BillettKjopAvEnKunde)

    TiBilletter = [
        (1, 'WF1302', 1, None, None, 'budsjett'),
        (1, 'WF1302', 1, None, None, 'budsjett'),
        (1, 'WF1302', 1, None, None, 'budsjett'),
        (1, 'WF1302', 1, None, None, 'budsjett'),
        (1, 'WF1302', 1, None, None, 'budsjett'),
        (1, 'WF1302', 1, None, None, 'budsjett'),
        (1, 'WF1302', 1, None, None, 'budsjett'),
        (1, 'WF1302', 1, None, None, 'budsjett'),
        (1, 'WF1302', 1, None, None, 'budsjett'),
        (1, 'WF1302', 1, None, None, 'budsjett'),

    ]
    query_billett = """
    INSERT INTO Billett (LøpeNummer, FlyRuteNummer, ReferanseNummerTur, ReferanseNummerRetur, Innsjekking, Kategori) 
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(query_billett, TiBilletter)

    TiSeter = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),

    ]

    query_sete_reservasjon = """
    INSERT INTO TilhorendeSete (BillettID, SeteID) VALUES (?, ?)
    """
    cursor.executemany(query_sete_reservasjon, TiSeter)

    query_billett_kjop = """
        SELECT * FROM Billettkjop
    """
    query_billetter = """
            SELECT * FROM Billett
        """
    conn.commit()
    query_tilhorende_seter = """
            SELECT * FROM TilhorendeSete
        """

    #cursor.execute(query_billett_kjop)
    #cursor.execute(query_billetter)
    cursor.execute(query_tilhorende_seter)
    resultater = cursor.fetchall()
    conn.close()
    return resultater

#print(bruks_tilfelle_syv())

