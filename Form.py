from PyQt5.QtWidgets import QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QTextEdit, QSpinBox, QListWidget
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton

class FormWindow(QWidget):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Patient Form")
        
        lstCompany = ['a', 'b', 'c', 'd', 'e']

        
        self.name = QLineEdit()
        self.Surename = QLineEdit()
        self.Birthday = QLineEdit()
        self.customer = QLineEdit()
        self.Address = QLineEdit()
        self.Patology = QComboBox(self)
        self.Patology.addItems(lstCompany)
        self.comments = QTextEdit()

        self.generate_btn = QPushButton("Save")

        layout = QFormLayout()
        layout.addRow("Name", self.name)
        layout.addRow("Surename", self.Surename)
        layout.addRow("Birthday", self.Birthday)
        layout.addRow("Address", self.Address)
        layout.addRow("Patology", self.Patology)
        # Añadir las imagenes de los dientes.

        layout.addRow("Comments", self.comments)
        layout.addRow(self.generate_btn)

        self.setLayout(layout)


        
    def getComboValue(self):
        print((self.comboBox.currentText(), self.comboBox.currentIndex()))

app = QApplication([])
w = FormWindow()
w.show()
app.exec()






#https://www.learnpyqt.com/examples/python-pdf-report-generator/

#https://realpython.com/python-pyqt-layout/

#https://pythones.net/lista-de-widgets-pyqt-5-explicacion-de-cada-uno/