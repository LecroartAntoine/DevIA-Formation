import requests, json, time
import mysql.connector as cnt

def connect_db(host, user, pswd, database = None):
    db = cnt.connect(
        host = host,
        user = user,
        passwd = pswd,
        database = database
    )
    return(db)

def exe(db, request, value = None, verbose = False, name = False):
    cursor = db.cursor(buffered = True)
    
    if value:
        cursor.execute(request, value)

    else :
        cursor.execute(request)

    db.commit()
    
    if verbose:
        result = cursor.fetchall()
        if name:
            result.insert(0, cursor.column_names)
        return(result)

def create_db():    
    db = connect_db('192.168.20.118', 'grogu', 'grogu')

    queries = ['CREATE DATABASE IF NOT EXISTS RaspberryPi;']

    queries.append("""
        CREATE TABLE IF NOT EXISTS RaspberryPi.Capteurs (
            Date timestamp PRIMARY KEY,
            Movemt BOOLEAN NOT NULL,
            Temp FLOAT,
            Humid FLOAT,
            Dist INT
        )ENGINE = InnoDB;    
    """)

    for query in queries:
        exe(db, query)

def aquisition():
    try:
        db = connect_db('192.168.20.118', 'grogu', 'grogu')

        data = json.loads(requests.get('http://192.168.20.27/modulesGrove.php?all').text)

        while data['PIR'] == '?' or data['temperature'] == '?' or data['humidite'] == '?' or data['US'] > 505:
            time.sleep(1)

        query = (f"""
            INSERT INTO RaspberryPi.Capteurs (Movemt, Temp, Humid, Dist) VALUES (
                                                                                {data['PIR']}, 
                                                                                {data['temperature']}, 
                                                                                {data['humidite']}, 
                                                                                {data['US']});
        """)

        exe(db, query)

    except Exception as e:
        print(e)

create_db()
aquisition()