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
    QCompleter
)
from PyQt5.QtCore import Qt


import DataSaver as DataSaverModule
import SearchingEngine as SearchingEngineModule


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
        self.save_button.clicked.connect(self.close)
        
        
        
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



class SearchingEngineLayout(QMainWindow):

    def __init__(self):
        super().__init__()

        self.controls = QWidget()  # Controls container widget.
        self.controlsLayout = QVBoxLayout()   # Controls container layout.

        # List of names, widgets are stored in a dictionary by these keys.
        database = SearchingEngineModule.ReadDatabase()
        database.readtxtDataBase()
        widget_names = database.name_list
        
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

        # Adding Completer.
        self.completer = QCompleter(widget_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)

        # Add the items to VBoxLayout (applied to container widget)
        # which encompasses the whole window.
        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.label)
        containerLayout.addWidget(self.searchbar)
        containerLayout.addWidget(self.scroll)

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
        print("Still not implemented.")

    def readFullRecord(self):
        self.is_on = not self.is_on
        self.updateButtonState()

    def updateButtonState(self):

        if self.is_on == True:
            self.show_more_btn.setStyleSheet("background-color: #4CAF50; color: #fff;")
        else:
            self.show_more_btn.setStyleSheet("background-color: none; color: none;")


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



if __name__ == "__main__":
    
    """
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
    """    

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

