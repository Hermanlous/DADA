import sqlite3
import os

def opprett_flydatabase(db_navn='flydatabase.db'):
    """Oppretter en SQLite3-database for flysystem"""
    # Fjern databasen hvis den allerede eksisterer
    if os.path.exists(db_navn):
        os.remove(db_navn)
    
    # Koble til databasen
    conn = sqlite3.connect(db_navn)
    cursor = conn.cursor()
    
    # Aktiver foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Opprett tabeller
    
    # Flyprodusent
    cursor.execute('''
    CREATE TABLE Flyprodusent (
        ProdusentNavn TEXT PRIMARY KEY,
        Nasjonalitet TEXT NOT NULL,
        Stiftelsesaar INTEGER NOT NULL
    )
    ''')
    
    # Flytype
    cursor.execute('''
    CREATE TABLE Flytype (
        TypeNavn TEXT PRIMARY KEY,
        ProdusentNavn TEXT NOT NULL,
        FoersteProdusjonsaar INTEGER NOT NULL,
        SisteProdusjonsaar INTEGER,
        FOREIGN KEY (ProdusentNavn) REFERENCES Flyprodusent(ProdusentNavn)
    )
    ''')
    
    # Flyselskap
    cursor.execute('''
    CREATE TABLE Flyselskap (
        FlyselskapID TEXT PRIMARY KEY,
        Navn TEXT NOT NULL,
        Hjemland TEXT,
        Grunnlagt INTEGER
    )
    ''')
    
    # Fordelsprogram
    cursor.execute('''
    CREATE TABLE Fordelsprogram (
        ProgramID INTEGER PRIMARY KEY,
        FlyselskapID TEXT NOT NULL,
        FOREIGN KEY (FlyselskapID) REFERENCES Flyselskap(FlyselskapID)
    )
    ''')
    
    # Fly
    cursor.execute('''
    CREATE TABLE Fly (
        RegistreringsNummer TEXT PRIMARY KEY,
        SerieNummer TEXT NOT NULL,
        TypeNavn TEXT NOT NULL,
        FlyselskapID TEXT NOT NULL,
        Navn TEXT,
        DriftsAar INTEGER NOT NULL,
        FOREIGN KEY (TypeNavn) REFERENCES Flytype(TypeNavn),
        FOREIGN KEY (FlyselskapID) REFERENCES Flyselskap(FlyselskapID)
    )
    ''')
    
    # Flyplass
    cursor.execute('''
    CREATE TABLE Flyplass (
        FlyplasskodeIATA TEXT PRIMARY KEY,
        Navn TEXT UNIQUE NOT NULL,
        By TEXT NOT NULL,
        Fylke TEXT
    )
    ''')
    
    # Flyrute
    cursor.execute('''
    CREATE TABLE Flyrute (
        FlyruteNummer TEXT,
        FlyselskapID TEXT NOT NULL,
        TypeNavn TEXT NOT NULL,
        StartFlyplass TEXT NOT NULL,
        EndeFlyplass TEXT NOT NULL,
        PlanlagtAvgangTid TIME NOT NULL,
        PlanlagtAnkomstTid TIME NOT NULL,
        Ukedagskode TEXT NOT NULL,
        OppstartDato DATE NOT NULL,
        SluttDato DATE,
        PRIMARY KEY (FlyruteNummer, FlyselskapID),
        FOREIGN KEY (FlyselskapID) REFERENCES Flyselskap(FlyselskapID),
        FOREIGN KEY (TypeNavn) REFERENCES Flytype(TypeNavn),
        FOREIGN KEY (StartFlyplass) REFERENCES Flyplass(FlyplasskodeIATA),
        FOREIGN KEY (EndeFlyplass) REFERENCES Flyplass(FlyplasskodeIATA)
    )
    ''')
    
    # Mellomlanding (svak entitet)
    cursor.execute('''
    CREATE TABLE Mellomlanding (
        FlyruteNummer TEXT,
        FlyselskapID TEXT,
        Flyplass TEXT NOT NULL,
        AnkomstTid DATETIME NOT NULL,
        AvgangTid DATETIME NOT NULL,
        Sekvens INTEGER NOT NULL,
        PRIMARY KEY (FlyruteNummer, FlyselskapID, Flyplass),
        FOREIGN KEY (FlyruteNummer, FlyselskapID) REFERENCES Flyrute(FlyruteNummer, FlyselskapID),
        FOREIGN KEY (Flyplass) REFERENCES Flyplass(FlyplasskodeIATA)
    )
    ''')
    
    # Setekonfigurasjon
    cursor.execute('''
    CREATE TABLE Setekonfigurasjon (
        TypeNavn TEXT,
        SeteID TEXT,
        Klasse TEXT NOT NULL,
        PRIMARY KEY (TypeNavn, SeteID),
        FOREIGN KEY (TypeNavn) REFERENCES Flytype(TypeNavn)
    )
    ''')
    
    # Pris
    cursor.execute('''
    CREATE TABLE Pris (
        FlyruteNummer TEXT,
        FlyselskapID TEXT,
        StartFlyplass TEXT NOT NULL,
        SluttFlyplass TEXT NOT NULL,
        Kategori TEXT NOT NULL,
        Pris DECIMAL(10,2) NOT NULL,
        GyldigFra DATETIME NOT NULL,
        GyldigTil DATETIME,
        PRIMARY KEY (FlyruteNummer, FlyselskapID, StartFlyplass, SluttFlyplass, Kategori, GyldigFra),
        FOREIGN KEY (FlyruteNummer, FlyselskapID) REFERENCES Flyrute(FlyruteNummer, FlyselskapID),
        FOREIGN KEY (StartFlyplass) REFERENCES Flyplass(FlyplasskodeIATA),
        FOREIGN KEY (SluttFlyplass) REFERENCES Flyplass(FlyplasskodeIATA)
    )
    ''')
    
    # Kunde
    cursor.execute('''
    CREATE TABLE Kunde (
        KundeNr INTEGER PRIMARY KEY,
        Fornavn TEXT NOT NULL,
        Etternavn TEXT NOT NULL,
        Telefon TEXT NOT NULL,
        Epost TEXT NOT NULL,
        Nasjonalitet TEXT NOT NULL
    )
    ''')
    
    # KundeFordelsprogram (svak entitet)
    cursor.execute('''
    CREATE TABLE KundeFordelsprogram (
        KundeNr INTEGER,
        ProgramID INTEGER,
        MedlemsNr TEXT NOT NULL,
        Status TEXT,
        PRIMARY KEY (KundeNr, ProgramID),
        FOREIGN KEY (KundeNr) REFERENCES Kunde(KundeNr),
        FOREIGN KEY (ProgramID) REFERENCES Fordelsprogram(ProgramID)
    )
    ''')
    
    # Flyvning
    cursor.execute('''
    CREATE TABLE Flyvning (
        FlyvningsID INTEGER PRIMARY KEY AUTOINCREMENT,
        FlyruteNummer TEXT NOT NULL,
        FlyselskapID TEXT NOT NULL,
        Dato DATE NOT NULL,
        Status TEXT NOT NULL CHECK (Status IN ('Planlagt', 'Aktiv', 'Fullført', 'Kansellert')),
        RegistreringsNummer TEXT,
        FOREIGN KEY (FlyruteNummer, FlyselskapID) REFERENCES Flyrute(FlyruteNummer, FlyselskapID),
        FOREIGN KEY (RegistreringsNummer) REFERENCES Fly(RegistreringsNummer)
    )
    ''')
    
    # FlyvningTider
    cursor.execute('''
    CREATE TABLE FlyvningTider (
        FlyvningsID INTEGER,
        Flyplass TEXT,
        AvgangTid DATETIME,
        AnkomstTid DATETIME,
        PRIMARY KEY (FlyvningsID, Flyplass),
        FOREIGN KEY (FlyvningsID) REFERENCES Flyvning(FlyvningsID),
        FOREIGN KEY (Flyplass) REFERENCES Flyplass(FlyplasskodeIATA)
    )
    ''')
    
    # Billettkjøp
    cursor.execute('''
    CREATE TABLE Billettkjop (
        BillettReferanse TEXT PRIMARY KEY,
        KundeNr INTEGER NOT NULL,
        KjopsDato DATETIME NOT NULL,
        TotalPris DECIMAL(10,2) NOT NULL,
        TurRetur BOOLEAN NOT NULL,
        FOREIGN KEY (KundeNr) REFERENCES Kunde(KundeNr)
    )
    ''')
    
    # Reiseetappe
    cursor.execute('''
    CREATE TABLE Reiseetappe (
        EtappeID INTEGER PRIMARY KEY AUTOINCREMENT,
        BillettReferanse TEXT NOT NULL,
        Retning TEXT NOT NULL CHECK (Retning IN ('Utreise', 'Hjemreise')),
        SekvensNr INTEGER NOT NULL,
        FOREIGN KEY (BillettReferanse) REFERENCES Billettkjop(BillettReferanse)
    )
    ''')
    
    # ReiseDetalj (svak entitet)
    cursor.execute('''
    CREATE TABLE ReiseDetalj (
        EtappeID INTEGER,
        FlyvningsID INTEGER,
        SeteID TEXT,
        Kategori TEXT NOT NULL,
        Pris DECIMAL(10,2) NOT NULL,
        InnsjekketTid DATETIME,
        BagasjeAntall INTEGER DEFAULT 0,
        PRIMARY KEY (EtappeID, FlyvningsID),
        FOREIGN KEY (EtappeID) REFERENCES Reiseetappe(EtappeID),
        FOREIGN KEY (FlyvningsID) REFERENCES Flyvning(FlyvningsID)
    )
    ''')
    
    # Bagasje
    cursor.execute('''
    CREATE TABLE Bagasje (
        BagasjeID INTEGER PRIMARY KEY AUTOINCREMENT,
        EtappeID INTEGER NOT NULL,
        FlyvningsID INTEGER NOT NULL,
        Vekt DECIMAL(5,2) NOT NULL,
        FOREIGN KEY (EtappeID, FlyvningsID) REFERENCES ReiseDetalj(EtappeID, FlyvningsID)
    )
    ''')
    
    # Opprett noen enkle indekser
    cursor.execute("CREATE INDEX idx_flyvning_rute ON Flyvning(FlyruteNummer, FlyselskapID)")
    cursor.execute("CREATE INDEX idx_reiseetappe_billett ON Reiseetappe(BillettReferanse)")
    
    # Lagre endringer og lukk tilkobling
    conn.commit()
    conn.close()

def legg_inn_data(db_navn='flydatabase.db'):
    """Legger inn data fra vedleggene i databasen"""
    conn = sqlite3.connect(db_navn)
    cursor = conn.cursor()
    
    # 1. Legg inn flyplasser (Vedlegg 1)
    flyplasser = [
        ('BOO', 'Bodø Lufthavn', 'Bodø', 'Nordland'),
        ('BGO', 'Bergen lufthavn, Flesland', 'Bergen', 'Vestland'),
        ('OSL', 'Oslo lufthavn, Gardermoen', 'Oslo', 'Viken'),
        ('SVG', 'Stavanger lufthavn, Sola', 'Stavanger', 'Rogaland'),
        ('TRD', 'Trondheim lufthavn, Værnes', 'Trondheim', 'Trøndelag')
    ]
    cursor.executemany(
        "INSERT INTO Flyplass (FlyplasskodeIATA, Navn, By, Fylke) VALUES (?, ?, ?, ?)",
        flyplasser
    )
    
    # 2. Legg inn flyprodusenter
    flyprodusenter = [
        ('The Boeing Company', 'USA', 1916),
        ('Airbus Group', 'Europa', 1970),
        ('De Havilland Canada', 'Canada', 1928)
    ]
    cursor.executemany(
        "INSERT INTO Flyprodusent (ProdusentNavn, Nasjonalitet, Stiftelsesaar) VALUES (?, ?, ?)",
        flyprodusenter
    )
    
    # 3. Legg inn flytyper
    flytyper = [
        ('Boeing 737 800', 'The Boeing Company', 1997, 2020),
        ('Airbus a320neo', 'Airbus Group', 2016, None),
        ('Dash-8 100', 'De Havilland Canada', 1984, 2005)
    ]
    cursor.executemany(
        "INSERT INTO Flytype (TypeNavn, ProdusentNavn, FoersteProdusjonsaar, SisteProdusjonsaar) VALUES (?, ?, ?, ?)",
        flytyper
    )
    
    # 4. Legg inn flyselskaper
    flyselskaper = [
        ('DY', 'Norwegian', 'Norge', 2002),
        ('SK', 'SAS', 'Norge', 1946),
        ('WF', 'Widerøe', 'Norge', 1934)
    ]
    cursor.executemany(
        "INSERT INTO Flyselskap (FlyselskapID, Navn, Hjemland, Grunnlagt) VALUES (?, ?, ?, ?)",
        flyselskaper
    )
    
    # 5. Legg inn fly for hvert flyselskap
    fly = [
        # Norwegian - Boeing 737 800
        ('LN-ENU', '42069', 'Boeing 737 800', 'DY', None, 2015),
        ('LN-ENR', '42093', 'Boeing 737 800', 'DY', 'Jan Bålsrud', 2018),
        ('LN-NIQ', '39403', 'Boeing 737 800', 'DY', 'Max Manus', 2011),
        ('LN-ENS', '42281', 'Boeing 737 800', 'DY', None, 2017),
        
        # SAS - Airbus a320neo
        ('SE-RUB', '9518', 'Airbus a320neo', 'SK', 'Birger Viking', 2020),
        ('SE-DIR', '11421', 'Airbus a320neo', 'SK', 'Nora Viking', 2023),
        ('SE-RUP', '12066', 'Airbus a320neo', 'SK', 'Ragnhild Viking', 2024),
        ('SE-RZE', '12166', 'Airbus a320neo', 'SK', 'Ebbe Viking', 2024),
        
        # Widerøe - Dash-8 100
        ('LN-WIH', '383', 'Dash-8 100', 'WF', 'Oslo', 1994),
        ('LN-WIA', '359', 'Dash-8 100', 'WF', 'Nordland', 1993),
        ('LN-WIL', '298', 'Dash-8 100', 'WF', 'Narvik', 1995)
    ]
    cursor.executemany(
        "INSERT INTO Fly (RegistreringsNummer, SerieNummer, TypeNavn, FlyselskapID, Navn, DriftsAar) VALUES (?, ?, ?, ?, ?, ?)",
        fly
    )
    
    # 6. Legg inn setekonfigurasjoner
    
    # Boeing 737 800 har 31 rader med 6 seter (A-F)
    boeing_seter = []
    for rad in range(1, 32):
        for sete in ['A', 'B', 'C', 'D', 'E', 'F']:
            # Bestem seteklasse basert på plassering
            if rad <= 5:
                klasse = 'Premium'
            elif rad == 13:  # Nødutgang
                klasse = 'Økonomi Plus'
            else:
                klasse = 'Økonomi'
            boeing_seter.append(('Boeing 737 800', f'{rad}{sete}', klasse))
    
    # Airbus a320neo har 30 rader med 6 seter (A-F)
    airbus_seter = []
    for rad in range(1, 31):
        for sete in ['A', 'B', 'C', 'D', 'E', 'F']:
            # Bestem seteklasse basert på plassering
            if rad <= 4:
                klasse = 'Premium'
            elif rad in [11, 12]:  # Nødutgang
                klasse = 'Økonomi Plus'
            else:
                klasse = 'Økonomi'
            airbus_seter.append(('Airbus a320neo', f'{rad}{sete}', klasse))
    
    # Dash-8 100 har 10 rader med varierende antall seter
    dash_seter = []
    # Rad 1 har bare C-D
    for sete in ['C', 'D']:
        dash_seter.append(('Dash-8 100', f'1{sete}', 'Premium'))
    
    # Rad 2-10 har A-D
    for rad in range(2, 11):
        for sete in ['A', 'B', 'C', 'D']:
            # Bestem seteklasse
            if rad <= 3:
                klasse = 'Premium'
            elif rad == 5:  # Nødutgang
                klasse = 'Økonomi Plus'
            else:
                klasse = 'Økonomi'
            dash_seter.append(('Dash-8 100', f'{rad}{sete}', klasse))
    
    # Slå sammen alle seter og legg dem inn
    alle_seter = boeing_seter + airbus_seter + dash_seter
    cursor.executemany(
        "INSERT INTO Setekonfigurasjon (TypeNavn, SeteID, Klasse) VALUES (?, ?, ?)",
        alle_seter
    )
    
    # 7. Legg inn flyruter (Vedlegg 3)
    flyruter = [
        ('WF1311', 'WF', 'Dash-8 100', 'TRD', 'BOO', '15:15', '16:20', '12345', '2023-01-01', None),
        ('WF1302', 'WF', 'Dash-8 100', 'BOO', 'TRD', '07:35', '08:40', '12345', '2023-01-01', None),
        ('DY753', 'DY', 'Boeing 737 800', 'TRD', 'OSL', '10:20', '11:15', '1234567', '2023-01-01', None),
        ('SK332', 'SK', 'Airbus a320neo', 'OSL', 'TRD', '08:00', '09:05', '1234567', '2023-01-01', None),
        ('SK888', 'SK', 'Airbus a320neo', 'TRD', 'SVG', '10:00', '12:10', '12345', '2023-01-01', None)
    ]
    cursor.executemany(
        "INSERT INTO Flyrute (FlyruteNummer, FlyselskapID, TypeNavn, StartFlyplass, EndeFlyplass, PlanlagtAvgangTid, PlanlagtAnkomstTid, Ukedagskode, OppstartDato, SluttDato) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        flyruter
    )
    
    # 8. Legg inn mellomlanding for SK888
    cursor.execute("""
    INSERT INTO Mellomlanding 
    (FlyruteNummer, FlyselskapID, Flyplass, AnkomstTid, AvgangTid, Sekvens) 
    VALUES ('SK888', 'SK', 'BGO', '11:10', '11:40', 1)
    """)
    
    # 9. Legg inn priser for flyrutene
    priser = [
        # WF1311: TRD-BOO
        ('WF1311', 'WF', 'TRD', 'BOO', 'Premium', 2018.00, '2023-01-01 00:00:00', None),
        ('WF1311', 'WF', 'TRD', 'BOO', 'Økonomi', 899.00, '2023-01-01 00:00:00', None),
        ('WF1311', 'WF', 'TRD', 'BOO', 'Budsjett', 599.00, '2023-01-01 00:00:00', None),
        
        # WF1302: BOO-TRD
        ('WF1302', 'WF', 'BOO', 'TRD', 'Premium', 2018.00, '2023-01-01 00:00:00', None),
        ('WF1302', 'WF', 'BOO', 'TRD', 'Økonomi', 899.00, '2023-01-01 00:00:00', None),
        ('WF1302', 'WF', 'BOO', 'TRD', 'Budsjett', 599.00, '2023-01-01 00:00:00', None),
        
        # DY753: TRD-OSL
        ('DY753', 'DY', 'TRD', 'OSL', 'Premium', 1500.00, '2023-01-01 00:00:00', None),
        ('DY753', 'DY', 'TRD', 'OSL', 'Økonomi', 1000.00, '2023-01-01 00:00:00', None),
        ('DY753', 'DY', 'TRD', 'OSL', 'Budsjett', 500.00, '2023-01-01 00:00:00', None),
        
        # SK332: OSL-TRD
        ('SK332', 'SK', 'OSL', 'TRD', 'Premium', 1500.00, '2023-01-01 00:00:00', None),
        ('SK332', 'SK', 'OSL', 'TRD', 'Økonomi', 1000.00, '2023-01-01 00:00:00', None),
        ('SK332', 'SK', 'OSL', 'TRD', 'Budsjett', 500.00, '2023-01-01 00:00:00', None),
        
        # SK888: TRD-BGO-SVG (delpris TRD-BGO)
        ('SK888', 'SK', 'TRD', 'BGO', 'Premium', 2000.00, '2023-01-01 00:00:00', None),
        ('SK888', 'SK', 'TRD', 'BGO', 'Økonomi', 1500.00, '2023-01-01 00:00:00', None),
        ('SK888', 'SK', 'TRD', 'BGO', 'Budsjett', 800.00, '2023-01-01 00:00:00', None),
        
        # SK888: TRD-BGO-SVG (delpris BGO-SVG)
        ('SK888', 'SK', 'BGO', 'SVG', 'Premium', 1000.00, '2023-01-01 00:00:00', None),
        ('SK888', 'SK', 'BGO', 'SVG', 'Økonomi', 700.00, '2023-01-01 00:00:00', None),
        ('SK888', 'SK', 'BGO', 'SVG', 'Budsjett', 350.00, '2023-01-01 00:00:00', None),
        
        # SK888: TRD-BGO-SVG (totalpris TRD-SVG)
        ('SK888', 'SK', 'TRD', 'SVG', 'Premium', 2200.00, '2023-01-01 00:00:00', None),
        ('SK888', 'SK', 'TRD', 'SVG', 'Økonomi', 1700.00, '2023-01-01 00:00:00', None),
        ('SK888', 'SK', 'TRD', 'SVG', 'Budsjett', 1000.00, '2023-01-01 00:00:00', None)
    ]
    cursor.executemany(
        "INSERT INTO Pris (FlyruteNummer, FlyselskapID, StartFlyplass, SluttFlyplass, Kategori, Pris, GyldigFra, GyldigTil) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        priser
    )
    
    # 10. Legg inn flyvninger for 1. april 2025 (Brukstilfelle 4)
    flyvninger = [
        (None, 'WF1302', 'WF', '2025-04-01', 'Planlagt', 'LN-WIH'),  # BOO-TRD med Oslo-flyet
        (None, 'DY753', 'DY', '2025-04-01', 'Planlagt', 'LN-ENR'),   # TRD-OSL med Jan Bålsrud-flyet
        (None, 'SK888', 'SK', '2025-04-01', 'Planlagt', 'SE-RUB')    # TRD-BGO-SVG med Birger Viking-flyet
    ]
    cursor.executemany(
        "INSERT INTO Flyvning (FlyvningsID, FlyruteNummer, FlyselskapID, Dato, Status, RegistreringsNummer) VALUES (?, ?, ?, ?, ?, ?)",
        flyvninger
    )
    
    # Lagre endringer og lukk tilkobling
    conn.commit()
    conn.close()

# Hovedprogram
# if __name__ == "__main__":
#     db_navn = 'flydatabase.db'
#     opprett_flydatabase(db_navn)
#     legg_inn_data(db_navn)

def test_flydatabase():
    """Et enkelt testprogram for flydatabasen"""
    db_navn = 'flydatabase.db'
    
    # Koble til databasen for testing
    conn = sqlite3.connect(db_navn)
    conn.row_factory = sqlite3.Row  # Gjør det lettere å få data med kolonnenavn
    cursor = conn.cursor()
    
    # Test 1: Flyplasser
    print("\n=== Flyplasser ===")
    cursor.execute("SELECT FlyplasskodeIATA, Navn FROM Flyplass")
    for row in cursor.fetchall():
        print(f"{row['FlyplasskodeIATA']}: {row['Navn']}")
    
    # Test 2: Fly og flyselskaper
    print("\n=== Fly med flyselskap ===")
    cursor.execute("""
    SELECT f.RegistreringsNummer, f.Navn AS FlyNavn, fs.Navn AS SelskapNavn
    FROM Fly f
    JOIN Flyselskap fs ON f.FlyselskapID = fs.FlyselskapID
    LIMIT 5
    """)
    for row in cursor.fetchall():
        flynavn = row['FlyNavn'] if row['FlyNavn'] else "(uten navn)"
        print(f"{row['RegistreringsNummer']} - {flynavn} ({row['SelskapNavn']})")
    
    # Test 3: Flyruter med mellomlanding
    print("\n=== Flyruter med mellomlanding ===")
    cursor.execute("""
    SELECT r.FlyruteNummer, fs.Navn, fp_start.FlyplasskodeIATA, fp_end.FlyplasskodeIATA,
           m.Flyplass AS MellomlandingFlyplass
    FROM Flyrute r
    JOIN Flyselskap fs ON r.FlyselskapID = fs.FlyselskapID
    JOIN Flyplass fp_start ON r.StartFlyplass = fp_start.FlyplasskodeIATA
    JOIN Flyplass fp_end ON r.EndeFlyplass = fp_end.FlyplasskodeIATA
    JOIN Mellomlanding m ON r.FlyruteNummer = m.FlyruteNummer AND r.FlyselskapID = m.FlyselskapID
    """)
    for row in cursor.fetchall():
        print(f"{row['FlyruteNummer']} ({row['Navn']}): {row['FlyplasskodeIATA']}-{row['MellomlandingFlyplass']}-{row['FlyplasskodeIATA']}")
    
    # Test 4: Flyvninger for 1. april 2025
    print("\n=== Flyvninger 1. april 2025 ===")
    cursor.execute("""
    SELECT fv.FlyruteNummer, fs.Navn, fl.RegistreringsNummer, fl.Navn AS FlyNavn
    FROM Flyvning fv
    JOIN Flyselskap fs ON fv.FlyselskapID = fs.FlyselskapID
    JOIN Fly fl ON fv.RegistreringsNummer = fl.RegistreringsNummer
    WHERE fv.Dato = '2025-04-01'
    """)
    for row in cursor.fetchall():
        flynavn = row['FlyNavn'] if row['FlyNavn'] else "(uten navn)"
        print(f"{row['FlyruteNummer']} ({row['Navn']}): Fly {row['RegistreringsNummer']} - {flynavn}")
    
    # Test 5: Setekonfigurasjon oppsummering
    print("\n=== Setekonfigurasjon oppsummering ===")
    cursor.execute("""
    SELECT TypeNavn, Klasse, COUNT(*) AS Antall
    FROM Setekonfigurasjon
    GROUP BY TypeNavn, Klasse
    ORDER BY TypeNavn, Klasse
    """)
    current_type = None
    for row in cursor.fetchall():
        if current_type != row['TypeNavn']:
            current_type = row['TypeNavn']
            print(f"\n{current_type}:")
        print(f"  {row['Klasse']}: {row['Antall']} seter")
    
    # Test 6: Priser for utvalgte ruter
    print("\n=== Priser for utvalgte ruter ===")
    cursor.execute("""
    SELECT fr.FlyruteNummer, fs.Navn, fp_start.FlyplasskodeIATA, fp_end.FlyplasskodeIATA, 
           p.Kategori, p.Pris
    FROM Pris p
    JOIN Flyrute fr ON p.FlyruteNummer = fr.FlyruteNummer AND p.FlyselskapID = fr.FlyselskapID
    JOIN Flyselskap fs ON fr.FlyselskapID = fs.FlyselskapID
    JOIN Flyplass fp_start ON p.StartFlyplass = fp_start.FlyplasskodeIATA
    JOIN Flyplass fp_end ON p.SluttFlyplass = fp_end.FlyplasskodeIATA
    WHERE (fr.FlyruteNummer = 'DY753' OR fr.FlyruteNummer = 'SK888')
    ORDER BY fr.FlyruteNummer, p.StartFlyplass, p.SluttFlyplass, p.Pris DESC
    """)
    current_segment = None
    for row in cursor.fetchall():
        route_segment = f"{row['FlyruteNummer']} {row['FlyplasskodeIATA']}-{row['FlyplasskodeIATA']}"
        if current_segment != route_segment:
            current_segment = route_segment
            print(f"\n{row['FlyruteNummer']} ({row['Navn']}): {row['FlyplasskodeIATA']}-{row['FlyplasskodeIATA']}")
        print(f"  {row['Kategori']}: {row['Pris']} NOK")
    
    conn.close()
    print("\nDatabase testet!")

# Kjør testen når skriptet kjøres direkte
if __name__ == "__main__":
    test_flydatabase()