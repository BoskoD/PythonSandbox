import mysql.connector

config = {
    'user':'root',
    'password':'testPass',
    'host':'localhost',
    'database':'premier'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

