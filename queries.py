import sqlite3
conn = sqlite3.connect('flydatabase.db')
curs = conn.cursor()

def getflightinfo():
    query = """
        SELECT 
            fs.SelskapsNavn AS Flyselskap, 
            f.FlyTypeNavn AS Flytype, 
            COUNT(f.RegistreringsNummer) AS AntallFly
        FROM 
            Flyselskap fs
        JOIN 
            Flaate fl ON fs.FlyselskapsKode = fl.FlyselskapsKode
        JOIN 
            Fly f ON fl.FlaateID = f.FlaateID
        GROUP BY 
            fs.SelskapsNavn, f.FlyTypeNavn
        ORDER BY 
            fs.SelskapsNavn, f.FlyTypeNavn;
        """
    curs.execute(query)
    information = curs.fetchall()
    return information
   
def find_available_seats(cursor, flight_route, segment_id, flight_number=1):
    
    query_aircraft = """
    SELECT RegistreringsNummer
    FROM Flyvning
    WHERE FlyRuteNummer = ? AND MellomLandingID = ? AND LøpeNummer = ?
    """
    cursor.execute(query_aircraft, (flight_route, segment_id, flight_number))
    aircraft_result = cursor.fetchone()
    
    if not aircraft_result:
        return []
    
    aircraft_reg = aircraft_result[0]
    
    # Hent alle seter for flyet
    query_all_seats = """
    SELECT SeteID, Rad, Bokstav, NoedUtgang
    FROM Sete
    WHERE RegistreringsNummer = ?
    ORDER BY Rad, Bokstav
    """
    cursor.execute(query_all_seats, (aircraft_reg,))
    all_seats = cursor.fetchall()
    
    # Hent opptatte seter for denne flygningen
    query_booked_seats = """
    SELECT s.SeteID
    FROM Sete s
    JOIN TilhorendeSete ts ON s.SeteID = ts.SeteID
    JOIN Billett b ON ts.BillettID = b.BillettID
    JOIN Flyvning f ON b.LøpeNummer = f.LøpeNummer AND b.FlyRuteNummer = f.FlyRuteNummer
    WHERE f.FlyRuteNummer = ? AND f.MellomLandingID = ? AND f.LøpeNummer = ?
    """
    cursor.execute(query_booked_seats, (flight_route, segment_id, flight_number))
    booked_seats_result = cursor.fetchall()
    booked_seat_ids = [seat[0] for seat in booked_seats_result]
    
    # Filtrer ut ledige seter
    available_seats = [seat for seat in all_seats if seat[0] not in booked_seat_ids]
    
    return available_seats