<?xml version="1.0" encoding="UTF-8"?><sqlb_project><db path="Flydatabase_gruppe52.db" readonly="0" foreign_keys="1" case_sensitive_like="0" temp_store="0" wal_autocheckpoint="1000" synchronous="2"/><attached/><window><main_tabs open="structure browser pragmas query" current="3"/></window><tab_structure><column_width id="0" width="300"/><column_width id="1" width="0"/><column_width id="2" width="100"/><column_width id="3" width="2991"/><column_width id="4" width="0"/><expanded_item id="0" parent="1"/><expanded_item id="1" parent="1"/><expanded_item id="2" parent="1"/><expanded_item id="3" parent="1"/></tab_structure><tab_browse><table title="Baggasje" custom_title="0" dock_id="1" table="4,8:mainBaggasje"/><dock_state state="000000ff00000000fd00000001000000020000000000000000fc0100000001fb000000160064006f0063006b00420072006f00770073006500310100000000ffffffff0000010100ffffff000000000000000000000004000000040000000800000008fc00000000"/><default_encoding codec=""/><browse_table_settings/></tab_browse><tab_sql><sql name="SQL 1*">PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS SerienummerertAv;
DROP TABLE IF EXISTS FlyddAv;
DROP TABLE IF EXISTS Medlem;
DROP TABLE IF EXISTS TilhorendeSete;
DROP TABLE IF EXISTS Baggasje;
DROP TABLE IF EXISTS Billett;
DROP TABLE IF EXISTS Billettkjop;
DROP TABLE IF EXISTS Pris;
DROP TABLE IF EXISTS Flyvning;
DROP TABLE IF EXISTS MellomReise;
DROP TABLE IF EXISTS Sete;
DROP TABLE IF EXISTS Fly;
DROP TABLE IF EXISTS Flaate;
DROP TABLE IF EXISTS FlyType;
DROP TABLE IF EXISTS FlyProdusent;
DROP TABLE IF EXISTS FlyRute;
DROP TABLE IF EXISTS Fordelsprogram;
DROP TABLE IF EXISTS Flyselskap;
DROP TABLE IF EXISTS Kunde;
DROP TABLE IF EXISTS Flyplass;

-- Legger til en sjekk slik at programmet faktisk oppretter tabellene når scriptet kjøres. De sletter tabellene hvis de allerede finnes.

CREATE TABLE Flyplass (
    FlyplassKode TEXT PRIMARY KEY,
    FlyplassNavn TEXT NOT NULL
);

CREATE TABLE Kunde (
    KundeID INTEGER PRIMARY KEY AUTOINCREMENT,
    Navn TEXT NOT NULL,
    Telefon TEXT NOT NULL,
    Epost TEXT NOT NULL,
    Nasjonalitet TEXT NOT NULL
);

CREATE TABLE Flyselskap (
    FlyselskapsKode TEXT PRIMARY KEY,
    SelskapsNavn TEXT NOT NULL
);

CREATE TABLE Fordelsprogram (
    FordelsprogramID TEXT,
    FlyselskapsKode TEXT,
    PRIMARY KEY (FordelsprogramID, FlyselskapsKode),
    FOREIGN KEY(FlyselskapsKode) REFERENCES Flyselskap(FlyselskapsKode) ON DELETE CASCADE
);

CREATE TABLE FlyRute (
    FlyRuteNummer TEXT PRIMARY KEY,
    OppstartDato DATE NOT NULL,
    SluttDato DATE,
    Ukedagskode TEXT NOT NULL
);

CREATE TABLE FlyProdusent (
    ProdusentNavn TEXT PRIMARY KEY,
    Nasjonalitet TEXT NOT NULL,
    Stiftelsesaar INTEGER NOT NULL
);

CREATE TABLE FlyType (
    FlyTypeNavn TEXT PRIMARY KEY,
    ProdusentNavn TEXT,
    FoersteProduksjonsAar INTEGER NOT NULL,
    SisteProduksjonsAar INTEGER,
    FOREIGN KEY (ProdusentNavn) REFERENCES FlyProdusent(ProdusentNavn)
);

CREATE TABLE Flaate (
    FlaateID INTEGER PRIMARY KEY AUTOINCREMENT,
    FlyselskapsKode TEXT,
    FOREIGN KEY (FlyselskapsKode) REFERENCES Flyselskap(FlyselskapsKode) ON DELETE CASCADE
);

CREATE TABLE Fly (
    RegistreringsNummer TEXT PRIMARY KEY,
    FlaateID INTEGER,
    FlyTypeNavn TEXT,
    Navn TEXT,
    DriftAar INTEGER NOT NULL,
    FOREIGN KEY (FlaateID) REFERENCES Flaate(FlaateID) ON DELETE CASCADE,
    FOREIGN KEY (FlyTypeNavn) REFERENCES FlyType(FlyTypeNavn)
);

CREATE TABLE Sete (
    SeteID INTEGER PRIMARY KEY AUTOINCREMENT,
    RegistreringsNummer TEXT,
    Rad INTEGER NOT NULL,
    Bokstav CHAR NOT NULL,
    NoedUtgang INTEGER NOT NULL CHECK (NoedUtgang IN (0,1)),
    FOREIGN KEY (RegistreringsNummer) REFERENCES Fly(RegistreringsNummer) ON DELETE CASCADE
);

CREATE TABLE MellomReise (
    MellomLandingID TEXT,
    FlyRuteNummer TEXT,
    FlyplassKodeTil TEXT,
    FlyplassKodeFra TEXT,
    PlanlagtAvgang TIME NOT NULL,
    PlanlagtAnkomst TIME NOT NULL,
    PRIMARY KEY (MellomLandingID, FlyRuteNummer),
    FOREIGN KEY (FlyplassKodeFra) REFERENCES Flyplass(FlyplassKode),
    FOREIGN KEY (FlyplassKodeTil) REFERENCES Flyplass(FlyplassKode),
    FOREIGN KEY (FlyRuteNummer) REFERENCES FlyRute(FlyRuteNummer) ON DELETE SET NULL
);

CREATE TABLE Flyvning (
    LøpeNummer INTEGER,
    FlyRuteNummer TEXT,
    MellomLandingID TEXT,
    RegistreringsNummer TEXT,
    Status TEXT NOT NULL CHECK (Status IN ('Planlagt', 'Aktiv', 'Fullført', 'Kansellert')),
    Avgang TIME,
    Ankomst TIME,
    PRIMARY KEY (LøpeNummer, FlyRuteNummer),
    FOREIGN KEY (MellomLandingID, FlyRuteNummer) REFERENCES MellomReise(MellomLandingID, FlyRuteNummer) ON DELETE SET NULL,
    FOREIGN KEY (RegistreringsNummer) REFERENCES Fly(RegistreringsNummer) ON DELETE SET NULL
);

CREATE TABLE Pris (
    KlasseID TEXT NOT NULL,
    FlyRuteNummer TEXT NOT NULL,
    MellomLandingID TEXT NOT NULL,
    PrisForKlasse INTEGER NOT NULL,
    PRIMARY KEY (KlasseID, FlyRuteNummer, MellomLandingID),
    FOREIGN KEY(FlyRuteNummer, MellomLandingID) REFERENCES MellomReise(MellomLandingID, FlyRuteNummer) ON DELETE CASCADE
);

CREATE TABLE Billettkjop (
    ReferanseNummer INTEGER PRIMARY KEY AUTOINCREMENT,
    KundeID INTEGER,
    Kostnad INTEGER NOT NULL,
    FOREIGN KEY (KundeID) REFERENCES Kunde(KundeID)
);

CREATE TABLE Billett (
    BillettID INTEGER PRIMARY KEY AUTOINCREMENT,
    LøpeNummer INTEGER NOT NULL,
    FlyRuteNummer TEXT NOT NULL,
    ReferanseNummerTur INTEGER NOT NULL,
    ReferanseNummerRetur INTEGER,
    Innsjekking TEXT,
    Kategori TEXT NOT NULL CHECK (Kategori IN ('premium', 'økonomi', 'budsjett')),
    FOREIGN KEY (LøpeNummer, FlyRuteNummer) REFERENCES Flyvning(LøpeNummer, FlyRuteNummer) ON DELETE CASCADE,
    FOREIGN KEY (ReferanseNummerTur) REFERENCES Billettkjop(ReferanseNummer),
    FOREIGN KEY (ReferanseNummerRetur) REFERENCES Billettkjop(ReferanseNummer)
);

CREATE TABLE Baggasje (
    BaggasjeID TEXT PRIMARY KEY,
    BillettID INTEGER,
    Vekt INTEGER NOT NULL,
    InnleveringsTidspunkt DATETIME NOT NULL,
    FOREIGN KEY (BillettID) REFERENCES Billett(BillettID) ON DELETE CASCADE
);

CREATE TABLE TilhorendeSete (
    BillettID INTEGER,
    SeteID INTEGER,
    PRIMARY KEY (BillettID, SeteID),
    FOREIGN KEY (BillettID) REFERENCES Billett(BillettID) ON DELETE CASCADE,
    FOREIGN KEY (SeteID) REFERENCES Sete(SeteID)
);

CREATE TABLE Medlem (
    KundeID INTEGER,
    FordelsprogramID TEXT, 
    FlyselskapsKode TEXT,
    UnikFordelsRef TEXT,
    PRIMARY KEY (KundeID, FordelsprogramID, FlyselskapsKode),
    FOREIGN KEY (KundeID) REFERENCES Kunde(KundeID) ON DELETE CASCADE,
    FOREIGN KEY (FordelsprogramID, FlyselskapsKode) REFERENCES Fordelsprogram(FordelsprogramID, FlyselskapsKode) ON DELETE CASCADE
);

CREATE TABLE FlyddAv (
    FlyRuteNummer TEXT,
    LøpeNummer INTEGER,
    FlaateID INTEGER,
    PRIMARY KEY (LøpeNummer, FlyRuteNummer, FlaateID),
    FOREIGN KEY (LøpeNummer, FlyRuteNummer) REFERENCES Flyvning(LøpeNummer, FlyRuteNummer),
    FOREIGN KEY (FlaateID) REFERENCES Flaate(FlaateID)
);

CREATE TABLE SerienummerertAv (
    Registreringsnummer TEXT,
    ProdusentNavn TEXT,
    Serienummer TEXT,
    PRIMARY KEY (Registreringsnummer),
    FOREIGN KEY (ProdusentNavn) REFERENCES FlyProdusent(ProdusentNavn),
    FOREIGN KEY (Registreringsnummer) REFERENCES Fly(RegistreringsNummer) ON DELETE CASCADE
);</sql><current_tab id="0"/></tab_sql></sqlb_project>
