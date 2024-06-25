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
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit("1")

def insertCooldownData(table, data):
    try:
        userID = data[0]
        if readData(table, userID):
            print(f"User {userID} already exists in the database")
            return True
        conn, cur = connectDB()
        cur.execute(f"""INSERT INTO {table} (userID, utcTime) VALUES {data}""")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit("1")

def insertCasinoData(table, data):
    try:
        userID = data[0]
        if readData(table, userID):
            print(f"User {userID} already exists in the database")
            return True
        conn, cur = connectDB()
        cur.execute(f"""INSERT INTO {table} (userID, balance) VALUES {data}""")
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

def updateCasinoData(table, data):
    try:
        userID = data[0]
        if not readData(table, userID):
            print(f"User {userID} does not exist in the database")
            return False
        conn, cur = connectDB()
        cur.execute(f"""UPDATE {table} SET balance = {data[1]} WHERE userID = {userID}""")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit("1")

def updateCooldownData(table, data):
    try:
        userID = data[0]
        if not readData(table, userID):
            print(f"User {userID} does not exist in the database")
            return False
        conn, cur = connectDB()
        cur.execute(f"""UPDATE {table} SET utcTime = {data[1]} WHERE userID = {userID}""")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit("1")

def readData(table, userID):
    try:
        conn, cur = connectDB()
        cur.execute(f"SELECT * FROM {table} WHERE userID = ?", (str(userID),))  # Convert userID to string
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