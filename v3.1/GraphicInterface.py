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
    QCalendarWidget,
    QButtonGroup,
    QRadioButton,
    QGridLayout,
    QSpinBox,
    QDialog,
    QProgressBar
)

from PyQt5.QtGui import QImage, QPalette, QBrush

from PyQt5.QtCore import Qt, QSize

from functools import partial

from datetime import datetime 

import os
import DBManager as DBM
import References as ref
import DataSaver as DataSaverModule           # Also used to navigate with os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



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

dental_chart_string = ''


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

    def __init__(self, parent = None):
        super(MedicalFormLayout, self).__init__(parent)
        
        
        
        # Title and size of the Main Window and Center it
        self.setWindowTitle("Medical Form")
        #self.center()
        
        # LOGICAL & INTERACTABLE ELEMENTS______________________________________
        # List of options to choose in the Patology field.
        patology_list = ['Caries dental', 
                         'Enfermedad de las encías', 
                         'Cáncer oral', 
                         'Úlceras bucales', 
                         'Dolor de muela', 
                         'Erosión dental',
                         'Sensibilidad dental',
                         'Traumatismos dentales',
                         'Maloclusión',
                         'Tinción dental',
                         'Sarro dental'
                         ]
        
        gender_list = ['Male', 'Female', 'Others']
        
        self.material_list = ["",'Gasas', 'Anestesia', 'Gomas', 'Braquets']
        
        self.dentalString = QLabel("ffffffffffffffffffffffffffffffff")
        
        
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
        self.dental_chart.clicked.connect(self.launchTeethPhoto)
        
        self.MaterialCount = QSpinBox(self)
        self.MaterialList = QComboBox(self)
        self.MaterialList.addItems(self.material_list)
        self.MaterialAddButton = QPushButton("Add")
        self.MaterialAddButton.clicked.connect(self.addButton)
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.MaterialList, 1,1)
        self.grid_layout.addWidget(self.MaterialCount, 1,2)
        self.grid_layout.addWidget(self.MaterialAddButton, 1,3)
        
        
        # The comment section is not mandatory, therefore we dont need to check if is filled up.
        self.Comments = QTextEdit()
        self.save_button = QPushButton("Save Form")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.saveMedicalFormDataDB)
        #self.save_button.clicked.connect(self.saveMedicalFormData)
        self.save_button.clicked.connect(self.close)
        # Go back button
        self.return_button = QPushButton("Go back to Start Menu")
        self.return_button.clicked.connect(self.close)
        
        # LAYOUT ELEMENTS______________________________________________________
        #The fields are declared in the layout, ordered and sentenced to be visible.
        layout = QFormLayout()
        #layout.addRow(' ', self.ErrorMessage)
        
        
        #layout.addRow(self.dentalString)
        
        layout.addRow('PatientID', self.PatientID)
        layout.addRow('Name', self.Name)
        layout.addRow('Surname', self.Surname)
        layout.addRow('Birthday', self.Birthday)
        layout.addRow('Gender', self.Gender)
        layout.addRow('Address', self.Address)
        layout.addRow('Phone', self.Phone)
        layout.addRow('Dental Chart', self.dental_chart)
        layout.addRow('Patology', self.Patology)
        layout.addRow('Comments', self.Comments)
        layout.addRow('Materials', self.grid_layout)
        layout.addRow(self.save_button)
        layout.addRow(self.return_button)
        self.setLayout(layout)


    def launchTeethPhoto(self):
        second_layout = Modal(self)
        


    def checkFilledForm(self):
        # Mandatory information for the Form
        self.save_button.setEnabled(bool(self.Name.text()))
        self.save_button.setEnabled(bool(self.Surname.text()))
        #self.save_button.setEnabled(bool(self.Address.text()))
            
    # Not used    
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
        #print(self.dentalString.text())
        data_base_manager.new_patient(self.PatientID.text(),
                                      str(self.Name.text() + ' ' + self.Surname.text()),
                                      self.Birthday.selectedDate().toString(),
                                      self.Gender.currentText(),
                                      self.Address.text(),
                                      self.Phone.text(),
                                      self.Patology.currentText(),
                                      self.Comments.toPlainText(),
                                      self.dentalString.text(),
                                      self.PatientID.text()
                                      
                                      )
        data_base_manager.close()
    
    def addButton(self):

        data_base_manager_material = DBM.DBManager(ref.filename_sql_material) 
        data_base_manager_material.new_expense(

                                      self.MaterialsList.currentText(),
                                      self.MaterialCount.value()
                                      )

        data_base_manager_material.close()

        self.MaterialCount.setValue(0)
        self.MaterialList.clear()
        self.MaterialList.addItems(self.material_list)
        
        
        
    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())





class Modal(QDialog):
    def __init__(self, parent):
        super(Modal, self).__init__(parent)
        
        self.setFixedSize(1293, 524)


        DataSaverModule.moveToMainDirectory()
        DataSaverModule.moveToDirectory(ref.directory)
        

        oImage = QImage(ref.filename_img)
        sImage = oImage.scaled(QSize(1293,524))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)

        self.saveButton = QPushButton("Save Chart")
        
        self._dictRB = {                                                   # +++                                         
            'rb1': False,
            'rb2': False,
            'rb3': False,
            'rb4': False,
            'rb5': False,
            'rb6': False,
            'rb7': False,
            'rb8': False,
            'rb9': False,
            'rb10': False,
            'rb11': False,
            'rb12': False,
            'rb13': False,
            'rb14': False,
            'rb15': False,
            'rb16': False,
            'rb17': False,
            'rb18': False,
            'rb19': False,
            'rb20': False,
            'rb21': False,
            'rb22': False,
            'rb23': False,
            'rb24': False,
            'rb25': False,
            'rb26': False,
            'rb27': False,
            'rb28': False,
            'rb29': False,
            'rb30': False,
            'rb31': False,
            'rb32': False,
        }


        # Radio buttons
        self.group = QButtonGroup()
        
        self.group.setExclusive(False)
        
        self.b1 = QRadioButton('1')                                       # + 'rb1'  
        self.group.addButton(self.b1)


        self.b2 = QRadioButton('2')                                       # + 'rb2'  
        self.group.addButton(self.b2)


        self.b3 = QRadioButton('3')                                       # +++
        self.group.addButton(self.b3)
        
        self.b4 = QRadioButton('4')                                       # +++
        self.group.addButton(self.b4)
        
        self.b5 = QRadioButton('5')                                       # +++
        self.group.addButton(self.b5)
        
        self.b6 = QRadioButton('6')                                       # +++
        self.group.addButton(self.b6)
        
        self.b7 = QRadioButton('7')                                       # +++
        self.group.addButton(self.b7)
        
        self.b8 = QRadioButton('8')                                       # +++
        self.group.addButton(self.b8)
        
        self.b9 = QRadioButton('9')                                       # +++
        self.group.addButton(self.b9)
        
        self.b10 = QRadioButton('10')                                       # +++
        self.group.addButton(self.b10)
        
        self.b11 = QRadioButton('11')                                       # +++
        self.group.addButton(self.b11)
        
        self.b12 = QRadioButton('12')                                       # +++
        self.group.addButton(self.b12)
        
        self.b13 = QRadioButton('13')                                       # +++
        self.group.addButton(self.b13)
        
        self.b14 = QRadioButton('14')                                       # +++
        self.group.addButton(self.b14)
        
        self.b15 = QRadioButton('15')                                       # +++
        self.group.addButton(self.b15)
        
        self.b16 = QRadioButton('16')                                       # +++
        self.group.addButton(self.b16)
        
        self.b17 = QRadioButton('17')                                       # +++
        self.group.addButton(self.b17)
        
        self.b18 = QRadioButton('18')                                       # +++
        self.group.addButton(self.b18)
        
        self.b19 = QRadioButton('19')                                       # +++
        self.group.addButton(self.b19)
        
        self.b20 = QRadioButton('20')                                       # +++
        self.group.addButton(self.b20)
        
        self.b21 = QRadioButton('21')                                       # +++
        self.group.addButton(self.b21)
        
        self.b22 = QRadioButton('22')                                       # +++
        self.group.addButton(self.b22)
        
        self.b23 = QRadioButton('23')                                       # +++
        self.group.addButton(self.b23)
        
        self.b24 = QRadioButton('24')                                       # +++
        self.group.addButton(self.b24)
        
        self.b25 = QRadioButton('25')                                       # +++
        self.group.addButton(self.b25)
        
        self.b26 = QRadioButton('26')                                       # +++
        self.group.addButton(self.b26)
        
        self.b27 = QRadioButton('27')                                       # +++
        self.group.addButton(self.b27)
        
        self.b28 = QRadioButton('28')                                       # +++
        self.group.addButton(self.b28)
        
        self.b29 = QRadioButton('29')                                       # +++
        self.group.addButton(self.b29)
        
        self.b30 = QRadioButton('30')                                       # +++
        self.group.addButton(self.b30)
        
        self.b31 = QRadioButton('31')                                       # +++
        self.group.addButton(self.b31)
        
        self.b32 = QRadioButton('32')                                       # +++
        self.group.addButton(self.b32)
        
        a = QLabel('Top \n Left' , self )
        b = QLabel('Bottom \n Left' , self )         
        
        # Layout
        layout = QHBoxLayout()
        grid_layout = QGridLayout()
        save_layout = QVBoxLayout()
        
        layout.addLayout(grid_layout)
        layout.addLayout(save_layout)
        
        
        self.setLayout(layout)


        
        grid_layout.addWidget(a, 1,1)
        grid_layout.addWidget(self.b1, 1,2)
        grid_layout.addWidget(self.b2, 1,3)
        grid_layout.addWidget(self.b3, 1,4)
        grid_layout.addWidget(self.b4, 1,5)
        grid_layout.addWidget(self.b5, 1,6)
        grid_layout.addWidget(self.b6, 1,7)
        grid_layout.addWidget(self.b7, 1,8)
        grid_layout.addWidget(self.b8, 1,9)
        grid_layout.addWidget(self.b9, 1,10)
        grid_layout.addWidget(self.b10, 1,11)
        grid_layout.addWidget(self.b11, 1,12)
        grid_layout.addWidget(self.b12, 1,13)
        grid_layout.addWidget(self.b13, 1,14)
        grid_layout.addWidget(self.b14, 1,15)
        grid_layout.addWidget(self.b15, 1,16)
        grid_layout.addWidget(self.b16, 1,17)
        grid_layout.addWidget(b, 2,1,-1,1)
        grid_layout.addWidget(self.b17, 2,2,-1,1)
        grid_layout.addWidget(self.b18, 2,3,-1,1)
        grid_layout.addWidget(self.b19, 2,4,-1,1)
        grid_layout.addWidget(self.b20, 2,5,-1,1)
        grid_layout.addWidget(self.b21, 2,6,-1,1)
        grid_layout.addWidget(self.b22, 2,7,-1,1)
        grid_layout.addWidget(self.b23, 2,8,-1,1)
        grid_layout.addWidget(self.b24, 2,9,-1,1)
        grid_layout.addWidget(self.b25, 2,10,-1,1)
        grid_layout.addWidget(self.b26, 2,11,-1,1)
        grid_layout.addWidget(self.b27, 2,12,-1,1)
        grid_layout.addWidget(self.b28, 2,13,-1,1)
        grid_layout.addWidget(self.b29, 2,14,-1,1)
        grid_layout.addWidget(self.b30, 2,15,-1,1)
        grid_layout.addWidget(self.b31, 2,16,-1,1)
        grid_layout.addWidget(self.b32, 2,17,-1,1)
        grid_layout.addWidget(self.saveButton, 3,9,1,1)
        
        self.group.buttonClicked.connect(self.check_button)                 # +++
        self.saveButton.clicked.connect(partial(self.saveData,parent))
        
        
        
        self.setModal(True)
        self.exec_()
        
    def saveData(self, parent):
        self.accept()
        
        a = ""
        for b in self._dictRB:
            if self._dictRB[b] == False:
                a += 'f'
            else:
                a += 'v'
        #print(a)
        parent.dentalString.setText(a)
        #print(self.teeth_String)
        
    
 
    def check_button(self, radioButton):                                    # +++
        self._dictRB["rb"+radioButton.text()] = not self._dictRB["rb"+radioButton.text()]
        
        #print("clickеd button -> `{} - {}`".format(radioButton.text(), radioButton.isChecked()))        








class SearchingEngineLayout(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Searching Engine")
        self.resize(1150, 750)

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
        
        # obtain Human Teeth Overview
        names_list = ["upper right 3rd molar", "upper right 2nd molar", "upper right 1st molar", "upper right 2nd bicuspid", "upper right 1st bicuspid", 
                 "upper right cuspid", "upper right latheral incisor", "upper right central incisor", "upper left central incisor", "upper left lateral incisor",
                 "upper left cuspid", "upper left 1st bicuspid", "upper left 2nd bicuspid", "upper left 1st molar",  "upper left 2nd molar", "upper left 3rd molar",
                 
                 "lower right 3rd molar", "lower right 2nd molar", "lower right 1st molar", "lower right 2nd bicuspid", "lower right 1st bicuspid", 
                 "lower right cuspid", "lower right latheral incisor", "lower right central incisor", "lower left central incisor", "lower left lateral incisor",
                 "lower left cuspid", "lower left 1st bicuspid", "lower left 2nd bicuspid", "lower left 1st molar",  "lower left 2nd molar", "lower left 3rd molar",
                 ]
        afected_teeth = ""
        for (char, name) in zip(self.patient[0][8], names_list):
            if char == 'v':
                if len(afected_teeth) == 0:
                    afected_teeth = name
                else:
                    afected_teeth = afected_teeth + '\n\t\t\t\t' + name
                
        
        formated_record = ("Patient ID: \t\t" + self.patient[0][0] + "\n" + 
                            "Full Name: \t\t" +  self.patient[0][1] + "\n" + 
                            "Birthday: \t\t\t" + self.patient[0][2] + "\n" + 
                            "Gender: \t\t\t" + self.patient[0][3] + "\n" +
                            "Address: \t\t\t" + self.patient[0][4] + "\n" + 
                            "Phone: \t\t\t" + self.patient[0][5] + "\n" +  
                            "Patology: \t\t" + self.patient[0][6] + "\n" + 
                            "Affected teeth: \t" + afected_teeth + "\n" + 
                            "Comments: \t\t" + self.patient[0][7] + "\n"
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
        self.resize(1600, 800)

        chart = Canvas(self)
        
        
        
class ServerSynchronizationLayout(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Server")
        #self.center()
    
        self.progress_bar = QProgressBar()
        
        self.return_button = QPushButton("Go Back")
        self.return_button.clicked.connect(self.close)
        
        self.server_push = QPushButton("Server Push")
        self.server_push.clicked.connect(self.serverPush)
        
        self.server_pull = QPushButton("Server Pull")
        self.server_pull.clicked.connect(self.serverPull)
        
        layout = QGridLayout()

        
        layout.addWidget(self.server_push,1,1)
        layout.addWidget(self.server_pull,2,1)
        layout.addWidget(self.return_button,3,1)
        self.setLayout(layout)
        self.resize(200, 100)   
        
        
    def serverPush(self):
        DataSaverModule.moveToMainDirectory()
        DataSaverModule.moveToDirectory(ref.directory)
        
        file = open(r"DBPushClient.py") 
        exec(file.read()) 
        file.close()
        os.chdir("..")
        
    def serverPull(self):
        DataSaverModule.moveToMainDirectory()
        DataSaverModule.moveToDirectory(ref.directory)
        
        file = open(r"DBPullClient.py") 
        exec(file.read()) 
        file.close()
        os.chdir("..")
        
        
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
        self.w1.server_synchronization_button.clicked.connect(self.launchServerSynchronizationLayout)
        
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
    
    
    def launchServerSynchronizationLayout(self):
        
        self.w5 = ServerSynchronizationLayout()
        self.w5.show()
        self.w5.return_button.clicked.connect(self.w1.show)
        


if __name__ == "__main__":
    app = LayoutManager()


class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        super().__init__(fig)
        self.setParent(parent)

        """ 
        Matplotlib Script
        """
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)
        
        self.ax.plot(t, s)

        self.ax.set(xlabel='time (s)', ylabel='voltage (mV)',
               title='About as simple as it gets, folks')
        self.ax.grid()


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
