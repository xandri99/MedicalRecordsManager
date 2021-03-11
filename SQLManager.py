import mysql.connector
from mysql.connector import Error

class SQLManager:

    def __init__(self, host_name, user_name, user_password):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password
            )
        except Error as e:
            pass

    def create_database(connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            print("Database created successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

