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

    def newPatient(self, name, surname, birthday, db_id):
        # self.cursor.execute("INSERT INTO Patients VALUES ('" + name + "','" + surname + "','" + birthday + "','" + str(db_id) + "')") DO NOT DO THIS! THIS IS INSECURE!
        patient = (name, surname, birthday, db_id)
        self.cursor.execute("INSERT INTO Patients VALUES (?,?,?,?)", patient)
