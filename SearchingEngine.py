import os


filename = 'database.txt'
directory = 'Data'


# Function to move to the directory where the script is located. 
def moveToMainDirectory():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Function to move to the indicated directory from the current location.
def moveToDirectory(directory):
    os.chdir(directory)


class ReadDatabase():

    def __init__(self):
        self.full_data = {} 
        self.name_list = []
            

    def readtxtDataBase(self):
        moveToMainDirectory()
        moveToDirectory(directory)
        
        with open(filename, 'r') as file:
            for line in file:
                patient = [] 
                line = line.strip('\n')
                raw_d = line.split(';')
                for elem in raw_d:
                    raw = elem.split(':')
                    patient.append(raw[1] if len(raw) > 1 else '')
                    
                self.full_data[patient[0] + ' ' + patient[1]] = patient
                self.name_list.append(patient[0] + ' ' + patient[1])
