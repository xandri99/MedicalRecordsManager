import sqlite3


# DB Manager class. The database used has one table:
#   - Patients, with several fields:
#       - patient_id (int, unique)
#       - name (string)
#       - birthday (string)
#       - gender (integer)
#       - town (string)
#       - phone (string)
#       - pathologies (string for the time being)
#       - comments (string)
#
# It can be created with:
#     CREATE TABLE "Patients" (
#         "patient_id"	INTEGER UNIQUE,
#         "name"	TEXT,
#         "birthday"	TEXT,
#         "gender"	NUMERIC,
#         "town"	TEXT,
#         "phone"	TEXT,
#         "pathologies"	TEXT,
#         "comments"	TEXT,
#         PRIMARY KEY("patient_id" AUTOINCREMENT?)
#     );

class DBManager:
    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def new_patient(self, patient_id, name, birthday, gender, town, phone, pathologies, comments):
        # self.cursor.execute("INSERT INTO Patients VALUES ('" + name + "','" + surname + "','" + birthday + "',
        # '" + str(db_id) + "')") DO NOT DO THIS! THIS IS INSECURE!
        patient = (patient_id, name, birthday, gender, town, phone, pathologies, comments)
        self.cursor.execute("INSERT INTO Patients VALUES (?,?,?,?,?,?,?,?)", patient)
        self.connection.commit()

    def search_patient_by_name(self, name):
        self.cursor.execute("SELECT * FROM Patients WHERE name LIKE (?)", ('%'+name+'%',))
        patients = self.cursor.fetchall()
        print("Search for: " + name)
        for p in patients:
            print(p)

    def update_patient_by_id(self, patient_id, name, birthday, gender, town, phone, pathologies, comments):
        patient = (patient_id, name, birthday, gender, town, phone, pathologies, comments)
        self.cursor.execute("REPLACE INTO Patients VALUES (?,?,?,?,?,?,?,?)", patient)
        self.connection.commit()

    def delete_record(self, patient_id):
        self.cursor.execute("DELETE FROM Patients WHERE patient_id = ?;", str(patient_id))
        self.connection.commit()

    def close(self):
        self.connection.close()
