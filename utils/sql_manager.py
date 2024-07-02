import sqlite3

from data.var import dataDbFilePath

def connectDB():
    conn = sqlite3.connect(dataDbFilePath)
    cur = conn.cursor()
    return conn, cur
def initDB():
    try:
        conn, cur = connectDB()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS casinoAccount (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userID INTEGER,
                balance INTEGER
            );"""
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS rankData (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userID INTEGER,
                xp INTEGER,
                level INTEGER
            );"""
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cooldownTime (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userID INTEGER,
                utcTime INTEGER
            );"""
        )
        cur.execute(
                """
                CREATE TABLE IF NOT EXISTS badwordDatabase (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    words STRING
                );"""
            )
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit("1")
def insertCooldownData(data):
    try:
        userID = data[0]
        if readData("cooldownTime", userID):
            print(f"User {userID} already exists in the database")
            return True
        conn, cur = connectDB()
        cur.execute(f"""INSERT INTO cooldownTime (userID, utcTime) VALUES {data}""")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit("1")
def insertCasinoData(data):
    try:
        userID = data[0]
        if readData("casinoAccount", userID):
            print(f"User {userID} already exists in the database")
            return True
        conn, cur = connectDB()
        cur.execute(f"""INSERT INTO casinoAccount (userID, balance) VALUES {data}""")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit("1")
def insertRankData(dataInsert):
    try:
        userID = dataInsert
        if readData("rankData", userID):
            print(f"User {userID} already exists in the database")
            return True
        conn, cur = connectDB()
        cur.execute(f"INSERT INTO rankData (userID, xp, level) VALUES {dataInsert}")  # Supply the correct number of bindings
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit()
def insertBadWordData(dataInsert):
    try:
        if readBadWord(dataInsert):
            print(f"Word {dataInsert} already exists in the database")
            return True
        conn, cur = connectDB()
        cur.execute(f"INSERT INTO badwordDatabase (words) VALUES {dataInsert}")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit()
def updateRankData(data):
    try:
        userID = data[0]
        if not readData("rankData", userID):
            print(f"User {userID} does not exist in the database")
            return False
        conn, cur = connectDB()
        cur.execute(f"""UPDATE rankData SET xp = {data[1]}, level = {data[2]} WHERE userID = {userID}""")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit("1")
def updateCasinoData(data):
    try:
        userID = data[0]
        if not readData("casinoAccount", userID):
            print(f"User {userID} does not exist in the database")
            return False
        conn, cur = connectDB()
        cur.execute(f"""UPDATE casinoAccount SET balance = {data[1]} WHERE userID = {userID}""")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit("1")
def updateCooldownData(data):
    try:
        userID = data[0]
        if not readData("cooldownTime", userID):
            print(f"User {userID} does not exist in the database")
            return False
        conn, cur = connectDB()
        cur.execute(f"""UPDATE cooldownTime SET utcTime = {data[1]} WHERE userID = {userID}""")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit("1")
def readData(table, userID):
    """
    Simple solution to read data of a db table

    Args:
        table (str): the name of the table
        userID (int): user discord id

    Returns:
        data (csv): return (id, userID, value1, value2, ...)
    """
    try:
        conn, cur = connectDB()
        cur.execute(f"SELECT * FROM {table} WHERE userID = ?", (str(userID),))  # Convert userID to string
        data = cur.fetchall()
        conn.close()
        return data
    except Exception as e:
        print(e)
        exit()
def readBadWord(dataInsert):
    try:
        conn, cur = connectDB()
        cur.execute(f"SELECT * FROM badwordDatabase WHERE words = ?", dataInsert,)  # Convert userID to string
        data = cur.fetchall()
        conn.close()
        return data
    except Exception as e:
        print(e)
        exit()
def executeQuery(query):
    try:
        conn, cur = connectDB()
        cur.execute(query)
        result = cur.fetchall()
        conn.close()
        return result
    except Exception as e:
        print(e)
        exit("1")