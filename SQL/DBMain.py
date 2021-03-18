# DB Manager Tester
from DBManager import DBManager

db = DBManager("records.db")



db.new_patient("1", "Name", "1999-01-01", "Male", "Missirah", "2108", "Pathology 1", "Sample Comment")
db.new_patient("2", "Name2", "1999-01-02", "Female", "Missira2h", "21208", "Paxthology 1", "Samxple Comment")

db.search_patient_by_name("name")

db.update_patient_by_id("2", "Sample name", "2021-03-17", "Male", "Barcelona", "763857", "Nada", "Bien")

db.search_patient_by_name("sample")

db.search_patient_by_name("")

db.delete_record("1")
db.delete_record("2")

db.close()
