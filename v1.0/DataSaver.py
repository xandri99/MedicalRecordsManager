import os


filename = 'database.txt'
directory = 'Data'


# Function to move to the directory where the script is located. 
def moveToMainDirectory():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Function to move to the indicated directory from the current location.
def moveToDirectory(directory):
    os.chdir(directory)

    


class SaveMedicalFormData():
    # Class to save the data from de Medical Form in a .txt following the structure of a DataFrame

    def __init__(self, data):
        self.patient_data = data
        
        #Implementar metodo para verificar si el paciente ya existe, o si es un paciente nevo. Maybe usando ubicacion y nombre completo?
        

    def saveAsDataFrame(self):
        moveToMainDirectory()
        moveToDirectory(directory)
        
        # Evaluate if it is a new patient or one that already exists and the history is being updated.
        self.updateExistingPatient()
        
        
    def updateExistingPatient(self):     
        
        with open(filename, 'a') as file:
            patient_record = ("Name:" + self.patient_data['Name'] + 
                            ";Surname:" + self.patient_data['Surname'] +
                            ";Birthday:" + self.patient_data['Birthday'] +
                            ";Address:" + self.patient_data['Address'] +
                            ";Patology:" + self.patient_data['Patology'] +
                            ";Comments:" + self.patient_data['Comments'] + 
                            ";\n")
            
            file.write(patient_record)
        print("Data saved correctly.")
            
