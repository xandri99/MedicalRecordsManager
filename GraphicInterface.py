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
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QDesktopWidget,
    QScrollArea,
    QSpacerItem,
    QSizePolicy,
    QCompleter,
    QCalendarWidget
)
from PyQt5.QtCore import Qt
from datetime import datetime 

import TeethViewer as FotoLaunch
import DBManager as DBM
import References as ref
import DataSaver as DataSaverModule           # Also used to navigate with os




title_style = """<span style=\"
                           font-family: times, Times New Roman, times-roman, georgia, serif;
                           color: #0018FF;
                           margin: 0;
                           padding: 0px 0px 6px 0px;
                           font-size: 25px;
                           line-height: 44px;
                           letter-spacing: -2px;
                           font-weight: bold;">"""
                           
button_style = """<span style=\"
                           font-family: times, Times New Roman, times-roman, georgia, serif;
                           color: #111;
                           margin: 0;
                           padding: 0px 0px 6px 0px;
                           font-size: 15px;
                           line-height: 44px;
                           letter-spacing: -2px;">"""

closing_style = """</span>"""

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
        intro_text = title_style + "Welcome to MR-Manager." + closing_style
                       
        self.label = QLabel(intro_text)
        layout.addWidget(self.label)
        
        # Button to launch the Medical Form Layout
        self.medical_forms_button = QPushButton("Add New Patient", self) 
        layout.addWidget(self.medical_forms_button)
        self.medical_forms_button.clicked.connect(self.hide)
        
        # Button to search for an old patient
        self.searching_engine_button = QPushButton("Search an Old Patient", self) 
        layout.addWidget(self.searching_engine_button)
        self.searching_engine_button.clicked.connect(self.hide)
        
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
        gender_list = ['Male', 'Female', 'Others']
        #self.ErrorMessage = QLabel(self)
        self.PatientID = QLineEdit()
        idP = str(datetime.now())
        self.PatientID.setText(idP)
        self.PatientID.setReadOnly(True)
        
        self.Name = QLineEdit()
        self.Name.textChanged.connect(self.checkFilledForm)
        self.Surname = QLineEdit()
        self.Surname.textChanged.connect(self.checkFilledForm)
        self.Birthday = QCalendarWidget()
        self.Gender = QComboBox(self)
        self.Gender.addItems(gender_list)
        self.Address = QLineEdit()
        self.Address.textChanged.connect(self.checkFilledForm)
        self.Phone = QLineEdit()

        # To acces the selected item, we have the following methods:    self.Patology.currentText()
        #                                                               self.Patology.currentIndex()
        self.Patology = QComboBox(self)
        self.Patology.addItems(patology_list)
        
        
        self.dental_chart = QPushButton("Dental Chart")
        self.dental_chart.clicked.connect(self.launchFoto)
        
        
        # The comment section is not mandatory, therefore we dont need to check if is filled up.
        self.Comments = QTextEdit()
        self.save_button = QPushButton("Save Form")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.saveMedicalFormDataDB)
        self.save_button.clicked.connect(self.close)
        # Go back button
        self.return_button = QPushButton("Go back to Start Menu")
        self.return_button.clicked.connect(self.close)
        
        # LAYOUT ELEMENTS______________________________________________________
        #The fields are declared in the layout, ordered and sentenced to be visible.
        layout = QFormLayout()
        #layout.addRow(' ', self.ErrorMessage)
        layout.addRow('PatientID', self.PatientID)
        layout.addRow('Name', self.Name)
        layout.addRow('Surname', self.Surname)
        layout.addRow('Birthday', self.Birthday)
        layout.addRow('Gender', self.Gender)
        layout.addRow('Address', self.Address)
        layout.addRow('Phone', self.Phone)
        layout.addRow('Patology', self.Patology)
        layout.addRow('Dental Chart', self.dental_chart)
        layout.addRow('Comments', self.Comments)
        layout.addRow(self.save_button)
        layout.addRow(self.return_button)
        self.setLayout(layout)


    def launchFoto(self):
        self.wL = FotoLaunch.MainWindow()
        self.wL.setFixedSize(1293, 524)
        self.wL.show()


    def checkFilledForm(self):
        # Mandatory information for the Form
        self.save_button.setEnabled(bool(self.Name.text()))
        self.save_button.setEnabled(bool(self.Surname.text()))
        #self.save_button.setEnabled(bool(self.Address.text()))
            
        
    def saveMedicalFormData(self):
        
        # The data is organized in a Dictionary and sent to be saved.
        # Calculate age using the birth date and store.
        

        data = {
            #'HistoryID' : self.HistoryID.text(),
            'Name': self.Name.text(),
            'Surname': self.Surname.text(),
            'Birthday': self.Birthday.selectedDate().toString(),
            'Address': self.Address.text(),
            'Patology': self.Patology.currentText(),
            'Comments': self.Comments.toPlainText()
        }
        
        data_saver_module = DataSaverModule.SaveMedicalFormData(data)
        data_saver_module.saveAsDataFrame()


    def saveMedicalFormDataDB(self):  
        # To open the database in the directory specified in References.py
        DataSaverModule.moveToMainDirectory()
        DataSaverModule.moveToDirectory(ref.directory)
        
        data_base_manager = DBM.DBManager(ref.filename_sql) 
        
        data_base_manager.new_patient(self.PatientID.text(),
                                      str(self.Name.text() + ' ' + self.Surname.text()),
                                      self.Birthday.selectedDate().toString(),
                                      self.Gender.currentText(),
                                      self.Address.text(),
                                      self.Phone.text(),
                                      self.Patology.currentText(),
                                      self.Comments.toPlainText()
                                      )
        data_base_manager.close()
    
    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())



class SearchingEngineLayout(QMainWindow):

    def __init__(self):
        super().__init__()

        self.controls = QWidget()  # Controls container widget.
        self.controlsLayout = QVBoxLayout()   # Controls container layout.
        #self.center()
        
        # List of names, widgets are stored in a dictionary by these keys.
        ################## MAYBE WE COULD USE THE FINGERPRINT AS A PATIENT ID ################
        DataSaverModule.moveToMainDirectory()
        DataSaverModule.moveToDirectory(ref.directory)
        
        self.database = DBM.DBManager(ref.filename_sql)
        widget_names = self.database.get_all_db_names()
        self.database.close()
        
        
        
        self.widgets = []

        # Iterate the names, creating a new search result for each

        for name in widget_names:
            item = SearchResult(name)
            self.controlsLayout.addWidget(item)
            self.widgets.append(item)

        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controlsLayout.addItem(spacer)
        self.controls.setLayout(self.controlsLayout)

        # Scroll Area Properties.
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.controls)

        # Search bar.
        mess = button_style + "Enter the name of the patient you want to search for:" + closing_style
        self.label = QLabel(mess)
        self.searchbar = QLineEdit()
        self.searchbar.textChanged.connect(self.updateDisplay)

        # Completer.
        self.completer = QCompleter(widget_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)
        
        # Close button.
        self.return_button = QPushButton("Go back to Start Menu")
        self.return_button.clicked.connect(self.close)

        # Add the items to VBoxLayout (applied to container widget)
        # which encompasses the whole window.
        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.label)
        containerLayout.addWidget(self.searchbar)
        containerLayout.addWidget(self.scroll)
        containerLayout.addWidget(self.return_button)

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        #self.setGeometry(600, 100, 800, 600)
        self.setWindowTitle('Control Panel')

    def updateDisplay(self, text):

        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())




class SearchResult(QWidget):

    def __init__(self, name):
        super(SearchResult, self).__init__()
        self.name = name
        self.is_on = False

        self.content = QLabel(self.name)
        self.show_more_btn = QPushButton("Read Full Record")
        self.edit_patient_btn = QPushButton("Edit Patient Record")
        self.edit_patient_btn.setStyleSheet("background-color: #0086FF; color: #fff;")

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.content)
        self.hbox.addWidget(self.show_more_btn)
        self.hbox.addWidget(self.edit_patient_btn)

        self.show_more_btn.clicked.connect(self.readFullRecord)
        self.edit_patient_btn.clicked.connect(self.editPatientRecord)

        self.setLayout(self.hbox)


    def show(self):
        #Show this widget, and all child widgets.
        for w in [self, self.content, self.show_more_btn, self.edit_patient_btn]:
            w.setVisible(True)

    def hide(self):
        # Hide this widget, and all child widgets.
        for w in [self, self.content, self.show_more_btn, self.edit_patient_btn]:
            w.setVisible(False)

    def editPatientRecord(self):
        print("Still not implemented.\nThe implementation depends on how the database is structured and how you decide to organize the saving of files. ")

    def readFullRecord(self):
        self.is_on = not self.is_on
        self.updateButtonState()

    def updateButtonState(self):

        if self.is_on == True:
            self.show_more_btn.setStyleSheet("background-color: #4CAF50; color: #fff;")
            
            # Open the database, search record by name and print info
            DataSaverModule.moveToMainDirectory()
            DataSaverModule.moveToDirectory(ref.directory)
            self.database = DBM.DBManager(ref.filename_sql)
            self.patient_data = self.database.search_patient_by_name(self.name)
            self.database.close()
            
            self.content.setText(self.getFormatedPacientRecord(self.patient_data))
            
            
        else:
            self.show_more_btn.setStyleSheet("background-color: none; color: none;")
            self.content.setText(self.name)


    
    def getFormatedPacientRecord(self, patient_data):
        self.patient = patient_data
        formated_record = ("Patient ID: \t" + self.patient[0][0] + "\n" + 
                            "Full Name: \t" +  self.patient[0][1] + "\n" + 
                            "Birthday: \t\t" + self.patient[0][2] + "\n" + 
                            "Gender: \t\t" + self.patient[0][3] + "\n" +
                            "Address: \t\t" + self.patient[0][4] + "\n" + 
                            "Phone: \t\t" + self.patient[0][5] + "\n" + 
                            "Patology: \t" + self.patient[0][6] + "\n" + 
                            "Comments: \t" + self.patient[0][7] + "\n"
                            )
        return formated_record



class SearchEngineController():
    
    def updateDataBaseLecture():
        #database = SearchingEngineModule.ReadDatabase()
        #database.readtxtDataBase()
        print('updated')



class StatisticsLayout(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Statistics Section")
        #self.center()
    
        self.return_button = QPushButton("Close window")
        self.return_button.clicked.connect(self.close)

        layout = QFormLayout()
        self.label = QLabel("Not yet.")
        layout.addWidget(self.label)
        layout.addRow(self.return_button)
        self.setLayout(layout)
    
    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())
        
class ServerSynchronizationLayout(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Server Synchronization Section")
        #self.center()
    
        self.return_button = QPushButton("Close window")
        self.return_button.clicked.connect(self.close)

        layout = QFormLayout()
        self.label = QLabel("Not yet.")
        layout.addWidget(self.label)
        layout.addRow(self.return_button)
        self.setLayout(layout)


    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())




class LayoutManager():
    def __init__(self):
        app = QApplication(sys.argv)
        self.w1 = StartMenuLayout()
        
        self.w1.medical_forms_button.clicked.connect(self.launchMedicalFormLayout)
        self.w1.searching_engine_button.clicked.connect(self.launchSearchingEngineLayout)
        self.w1.statistics_button.clicked.connect(self.launchStatisticsLayout)
        self.w1.server_synchronization_button.clicked.connect(self.launchStatisticsLayout)
        
        self.w1.show()
        sys.exit(app.exec_())
    
    
    def launchMedicalFormLayout(self):

        self.w2 = MedicalFormLayout()
        self.w2.show()
        self.w2.save_button.clicked.connect(self.w1.show)
        self.w2.return_button.clicked.connect(self.w1.show)
        
    
    
    def launchSearchingEngineLayout(self):
        
        self.w3 = SearchingEngineLayout()
        self.w3.show()
        self.w3.return_button.clicked.connect(self.w1.show)
    
    
    def launchStatisticsLayout(self):
        
        self.w4 = StatisticsLayout()
        self.w4.show()
        self.w4.return_button.clicked.connect(self.w1.show)
    
    
    def launchStatisticsLayout(self):
        
        self.w4 = ServerSynchronizationLayout()
        self.w4.show()
        self.w4.return_button.clicked.connect(self.w1.show)
        


if __name__ == "__main__":
    app = LayoutManager()




# Working but w/ updatable layouts. Static interface.
"""
if __name__ == "__main__":
    
    
    El motivo de que tanto la pestaña para introducir un nuevo paciente como el buscador
    no se actualicen al cerrar la pestaña, sino que esten con los mismos datos desde el 
    inicio puede ser por como esta escrito el main. Todas las layouts estan cargadas en 
    sus respectivos threads desde el principio, y lo unico que se hace es hide and show.
    Quizas habria que ir invocandolas desde las distintas clases y abrirlas desde 0???
    
    Problemas:
        1. El buscador se abre con los datos que habia al momento de ejecutar el codigo. 
           Si en esta misma ejecucion se ha añadido pacientes, no aparecen.
        2. Cuando vas a añadir un segundo paciente, los datos del introducido primero estan
        ahi.
            --> Solucion pocha: Hacer que se borren todos los QLineEdit por codigo y skrr xd.


    app = QApplication(sys.argv)
    
    w1 = StartMenuLayout()
    w2 = MedicalFormLayout()
    w5 = SearchingEngineLayout()
    w3 = StatisticsLayout()
    w4 = ServerSynchronizationLayout()
    
    # Map of hierarchical relationships between layouts
    w1.medical_forms_button.clicked.connect(w2.show)
    w1.searching_engine_button.clicked.connect(w5.show)
    w1.statistics_button.clicked.connect(w3.show)
    w1.server_synchronization_button.clicked.connect(w4.show)
    
    w2.save_button.clicked.connect(w1.show)
    #w5.
    w3.return_button.clicked.connect(w1.show)
    w4.return_button.clicked.connect(w1.show)
    
    w1.show()
    sys.exit(app.exec_())
"""
