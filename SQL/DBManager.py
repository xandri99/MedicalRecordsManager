import sqlite3

'''
 DB Manager class. The database used has two tables:
   - Patients, with several fields:
       - patient_id (string, unique)
       - name (string)
       - birthday (string)
       - gender (string)
       - town (string)
       - phone (string)
       - pathologies (string)
       - comments (string)
       - dental_chart (string)
       - is_synced (integer)
       - last_modified (string)

    - Material:
        - timestamp (string, unique)
        - category (string)
        - quantity (integer)
        - is_synced (integer)
        
 It can be created with:
     CREATE TABLE "Patients" (
         "patient_id"	TEXT UNIQUE,
         "name"	TEXT,
         "birthday"	TEXT,
         "gender"	TEXT,
         "town"	TEXT,
         "phone"	TEXT,
         "pathologies"	TEXT,
         "comments"	TEXT,
         "dental_chart" TEXT,
         "is_synced"    INTEGER,
         "last_modified" TEXT,
         PRIMARY KEY("patient_id")
     );
     
     
'''
class DBManager:
    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def new_patient(self, patient_id, name, birthday, gender, town, phone, pathologies, comments, dental_chart, last_modified):
        # self.cursor.execute("INSERT INTO Patients VALUES ('" + name + "','" + surname + "','" + birthday + "',
        # '" + str(db_id) + "')") DO NOT DO THIS! THIS IS INSECURE!
        patient = (patient_id, name, birthday, gender, town, phone, pathologies, comments, dental_chart, last_modified)
        self.cursor.execute("INSERT INTO Patients VALUES (?,?,?,?,?,?,?,?,?,0,?)", patient)
        self.connection.commit()

    def search_patient_by_name(self, name):
        self.cursor.execute("SELECT * FROM Patients WHERE name LIKE (?)", ('%'+name+'%',))
        #patients = self.cursor.fetchall()
        #print("Search for: " + name)
        #for p in patients:
        #    print(p)
        #Return patients
        return self.cursor.fetchall() # List of tuples

    def get_all_db_names(self):
        self.cursor.execute("SELECT name FROM Patients")
        p_list =self.cursor.fetchall()
        names = []
        for p in p_list:
            names.append(p[0])
        return names # List of strings

    def get_patient_by_id(self, patient_id):
        self.cursor.execute("SELECT * FROM Patients WHERE patient_id = ?", str(patient_id))
        #patient = self.cursor.fetchall()
        #print(patient)
        #Return patient
        return self.cursor.fetchall() # List with 1 tuple

    def update_patient_by_id(self, patient_id, name, birthday, gender, town, phone, pathologies, comments, dental_chart, last_modified):
        patient = (patient_id, name, birthday, gender, town, phone, pathologies, comments, dental_chart, last_modified)
        self.cursor.execute("REPLACE INTO Patients VALUES (?,?,?,?,?,?,?,?,?,0,?)", patient)
        self.connection.commit()

    def update_material(self, timestamp, category, quantity):
        expense = (timestamp, category, quantity)
        self.cursor.execute("REPLACE INTO Materials VALUES (?,?,?,0)", expense)

    def delete_record(self, patient_id):
        self.cursor.execute("DELETE FROM Patients WHERE patient_id = ?;", patient_id)
        self.connection.commit()

    def sync_new_records(self):
        operation = """
        UPDATE Patients
        SET is_synced = 1
        WHERE is_synced = 0
        """
        self.cursor.executescript(operation)
        self.connection.commit()

    def sync_new_material(self):
        operation = """
        UPDATE Materials
        SET is_synced = 1
        WHERE is_synced = 0
        """
        self.cursor.executescript(operation)
        self.connection.commit()


    def get_new_records(self):
        self.cursor.execute("SELECT * FROM Patients WHERE is_synced = 0")
        return self.cursor.fetchall()

    def get_new_used_material(self):
        self.cursor.execute("SELECT * FROM Materials WHERE is_synced = 0")
        return self.cursor.fetchall()

    def update_patients_by_record(self, record):                    # DB SYNC USE ONLY
        self.cursor.execute("REPLACE INTO Patients VALUES (?,?,?,?,?,?,?,?,?,?,?)", record)
        self.connection.commit()

    def add_new_material_expense(self, timestamp, category, expense):
        self.cursor.execute("INSERT INTO Materials VALUES (?,?,?,0)", timestamp, category, quantity)

    def close(self):
        self.connection.close()
