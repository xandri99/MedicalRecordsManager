import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QTextEdit,
    QApplication,
    QFormLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QDesktopWidget
)

import DataSaver as DataSaverModule


class StartMenuLayout(QMainWindow):
    def __init__(self):
        super().__init__()
       
        # Title and size of the Main Window
        self.setWindowTitle("Medical Records Manager")
        self.resize(370, 200)
        #self.center()
        
        
        # Create a QVBoxLayout instance
        layout = QVBoxLayout()
        
        # Text in the Layout
        # We'll use this to explain the buttons and functions.
        self.label = QLabel("Texto explicando algo")
        layout.addWidget(self.label)
        
        # Button to launch the Medical Form Layout
        self.medical_forms_button = QPushButton("Medical Form", self) 
        layout.addWidget(self.medical_forms_button)
        self.medical_forms_button.clicked.connect(self.hide)
        
        # Button to launch the Statistics Layout
        self.statistics_button = QPushButton("Statistics", self) 
        layout.addWidget(self.statistics_button)
        self.statistics_button.clicked.connect(self.hide)
        
        # Button to launch the Server Synchronization Layout
        self.server_synchronization_button = QPushButton("Server Synchronization", self) 
        layout.addWidget(self.server_synchronization_button)
        self.server_synchronization_button.clicked.connect(self.hide)
        
        
        # Prevents buttons from separating vertically when enlarging tab
        layout.addStretch()
        
        # Sets the layout as a widget so it's visible.
        self.w1 = QWidget()
        self.w1.setLayout(layout)
        self.setCentralWidget(self.w1)

    
    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

class MedicalFormLayout(QWidget):

    def __init__(self):
        super().__init__()
        
        # Title and size of the Main Window and Center it
        self.setWindowTitle("Medical Form")
        #self.center()
        
        # LOGICAL & INTERACTABLE ELEMENTS______________________________________
        # List of options to choose in the Patology field.
        patology_list = ['a', 'b', 'c', 'd', 'e']
        #self.ErrorMessage = QLabel(self)
        self.Name = QLineEdit()
        self.Name.textChanged.connect(self.checkFilledForm)
        self.Surname = QLineEdit()
        self.Surname.textChanged.connect(self.checkFilledForm)
        self.Birthday = QDateEdit()
        self.Address = QLineEdit()
        self.Address.textChanged.connect(self.checkFilledForm)
        
        # To acces the selected item, we have the following methods:    self.Patology.currentText()
        #                                                               self.Patology.currentIndex()
        self.Patology = QComboBox(self)
        self.Patology.addItems(patology_list)
        
        # The comment section is not mandatory, therefore we dont need to check if is filled up.
        self.Comments = QTextEdit()
        self.save_button = QPushButton("Save Form")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.saveMedicalFormData)
        self.save_button.clicked.connect(self.hide)
        
        
        
        # LAYOUT ELEMENTS______________________________________________________
        #The fields are declared in the layout, ordered and sentenced to be visible.
        layout = QFormLayout()
        #layout.addRow(' ', self.ErrorMessage)
        layout.addRow('Name', self.Name)
        layout.addRow('Surname', self.Surname)
        layout.addRow('Birthday', self.Birthday)
        layout.addRow('Address', self.Address)
        layout.addRow('Patology', self.Patology)
        layout.addRow('Comments', self.Comments)
        layout.addRow(self.save_button)
        self.setLayout(layout)


    def checkFilledForm(self):
        self.save_button.setEnabled(bool(self.Name.text()))
        self.save_button.setEnabled(bool(self.Surname.text()))
        self.save_button.setEnabled(bool(self.Address.text()))
            
        
    def saveMedicalFormData(self):
        
        # The data is organized in a Dictionary and sent to be saved.
        data = {
            'Name': self.Name.text(),
            'Surname': self.Surname.text(),
            'Birthday': self.Birthday.text(),
            'Address': self.Address.text(),
            'Patology': self.Patology.currentText(),
            'Comments': self.Comments.toPlainText()
        }
        
        data_saver_module = DataSaverModule.SaveMedicalFormData(data)
        data_saver_module.saveAsDataFrame()

    
    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())



class StatisticsLayout(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Statistics Section")
    
        self.return_button = QPushButton("Close window")
        self.return_button.clicked.connect(self.close)

        layout = QFormLayout()
        self.label = QLabel("Not yet.")
        layout.addWidget(self.label)
        layout.addRow(self.return_button)
        self.setLayout(layout)
        
class ServerSynchronizationLayout(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Server Synchronization Section")
    
        self.return_button = QPushButton("Close window")
        self.return_button.clicked.connect(self.close)

        layout = QFormLayout()
        self.label = QLabel("Not yet.")
        layout.addWidget(self.label)
        layout.addRow(self.return_button)
        self.setLayout(layout)



if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    w1 = StartMenuLayout()
    w2 = MedicalFormLayout()
    w3 = StatisticsLayout()
    w4 = ServerSynchronizationLayout()
    
    # Map of hierarchical relationships between layouts
    w1.medical_forms_button.clicked.connect(w2.show)
    w1.statistics_button.clicked.connect(w3.show)
    w1.server_synchronization_button.clicked.connect(w4.show)
    
    w2.save_button.clicked.connect(w1.show)
    w3.return_button.clicked.connect(w1.show)
    w4.return_button.clicked.connect(w1.show)
    
    w1.show()
    sys.exit(app.exec_())

