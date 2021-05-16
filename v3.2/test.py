import DBManager
from datetime import datetime
db = DBManager.DBManager("Data/records.db")
'''materials = db.get_used_material()
counts = [0] * 4
for m in materials:
    if m[1] == "Gasas":
        counts[0] = counts[0] + m[2]
    elif m[1] == "Anestesia":
        counts[1] = counts[1] + m[2]
    elif m[1] == "Gomas":
        counts[2] = counts[2] + m[2]
    elif m[1] == "Brackets":
        counts[3] = counts[3] + m[2]

print(materials)
print(counts)'''
conditions = db.get_all_conditions()
counts = [0] * 10
print(conditions)
for c in conditions:
    if c[0] == "Caries dental":
        counts[0] += 1
    elif c[0] == "Enfermedad de las encías":
        counts[1] += 1
    elif c[0] == "Cáncer oral":
        counts[2] += 1
    elif c[0] == "Úlceras bucales":
        counts[3] += 1
    elif c[0] == "Dolor de muela":
        counts[4] += 1
    elif c[0] == "Erosión dental":
        counts[5] += 1
    elif c[0] == "Sensibilidad dental":
        counts[6] += 1
    elif c[0] == "Traumatismos dentales":
        counts[7] += 1
    elif c[0] == "Maloclousión":
        counts[8] += 1
    elif c[0] == "Tinción dental":
        counts[9] += 1

print(counts)