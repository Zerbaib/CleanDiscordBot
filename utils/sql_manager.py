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

def insertData(table, data):
    try:
        userID = data[0]
        if readData(table, userID):
            print(f"User {userID} already exists in the database")
            return True
        conn, cur = connectDB()
        cur.execute(f"""INSERT INTO {table} (userID, xp, level) VALUES {data}""")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit("1")

def updateData(table, data):
    try:
        userID = data[0]
        if not readData(table, userID):
            print(f"User {userID} does not exist in the database")
            return False
        conn, cur = connectDB()
        cur.execute(f"""UPDATE {table} SET xp = {data[1]}, level = {data[2]} WHERE userID = {userID}""")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exit("1")

def readData(table, userID):
    try:
        conn, cur = connectDB()
        cur.execute(f"SELECT * FROM {table} WHERE userID = {userID}")
        data = cur.fetchall()
        conn.close()
        return data[0]
    except Exception as e:
        print(e)
        exit("1")