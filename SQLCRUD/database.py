import mysql.connector

config = {
    'user':'root',
    'password':'27041991',
    'host':'localhost',
    'database':'premier'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

