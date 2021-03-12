import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QToolTip, QMessageBox, QLabel)
from PyQt5.QtWidgets import QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QTextEdit, QSpinBox, QListWidget
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class FormWindow(QWidget):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Patient Form")
        
        lstCompany = ['a', 'b', 'c', 'd', 'e']

        
        self.name = QLineEdit()
        self.Surename = QLineEdit()
        self.Birthday = QDateEdit()
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




class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Menu"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        self.pushButton = QPushButton("Medical Form", self)
        self.pushButton.move(275, 200)

        self.pushButton.clicked.connect(self.medicalForm)              # <===
        self.main_window()



    def main_window(self):
        self.label = QLabel("Medical Forms Administrator", self)
        self.label.move(285, 175)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


    def medicalForm(self):                                             # <===
        self.w = FormWindow()
        self.w.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())