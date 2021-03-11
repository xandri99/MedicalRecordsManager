import sqlite3

# DB Manager class. The database used has one table:
#   - Patients, with several fields:
#       - first_name (String)
#       - last_name (String)
#       - birthday (String, YYYY-MM-DD)
#       - id (Int, unique)

class DBManager:
    def __init__(self, path):
        self.path = path
        connection = sqlite3.connect(path)
        self.cursor = connection.cursor()

    def newPatient(self, name, surname, birthday, id):
        self.cursor.execute("INSERT INTO Patients VALUES ('" + name + "','"+ surname +"','" + birthday + "'," +  1)")
