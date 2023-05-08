import mysql.connector
from mysql.connector import errorcode
from database import cursor

DB_NAME = 'premier'

TABLES = {}

TABLES['logs'] = (
    "CREATE TABLE `logs` ("
        " `id` int(11) NOT NULL AUTO_INCREMENT,"
        " `text` varchar(250) NOT NULL,"
        " `user` varchar(250) NOT NULL,"
        " `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,"
        " PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB"
)

def create_database():
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    print(f"Database {DB_NAME} created.")
    
def create_tables():
    cursor.execute(f"USE {DB_NAME}")
    
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table alrady exiists.")
            else:
                print(err.msg)
    
create_database()
create_tables()
    