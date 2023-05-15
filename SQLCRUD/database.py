from config import DB_CONFIG
import mysql.connector

db = mysql.connector.connect(DB_CONFIG)
cursor = db.cursor()

