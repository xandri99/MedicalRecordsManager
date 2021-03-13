from PyQt5.QtWidgets import QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QTextEdit, QMessageBox, QSpinBox
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import os

import textwrap
from datetime import datetime




class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    error = pyqtSignal(str)
    file_saved_as = pyqtSignal(str)


class Generator(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.

    :param data: The data to add to the PDF for generating.
    """

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            
         
            today = datetime.today() 
            file = open("C:/Users/Ramon Roca Oliver/.ipython/projects/Fichita.txt", "a")
            #file.write(os.linesep)
            file.write("-")

            # Prepared by
            file.write(self.data['Name']+",")
            file.write(self.data['Surname']+",")
            file.write(self.data['Birthday']+",")
            file.write(today.strftime('%F')+",") #today's date
            file.write(self.data['Address']+",")
            file.write(self.data['Patology']+",")
            file.write(self.data['n_errors']+",")
            file.write(self.data['Comments'])
                       
        except Exception as e:
            self.signals.error.emit(str(e))
            return

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Patient Form")
        self.threadpool = QThreadPool()
        
        lstCompany = ['a', 'b', 'c', 'd', 'e']
        
        self.Name = QLineEdit()
        self.Surname = QLineEdit()
        self.Address = QLineEdit()
        self.Patology = QComboBox(self)
        self.Patology.addItems(lstCompany)
        self.Birthday = QDateEdit()
        self.vendor = QLineEdit()
        self.n_errors = QSpinBox()
        self.n_errors.setRange(0, 1000)
        self.comments = QTextEdit()

        self.generate_btn = QPushButton("Save")
        self.generate_btn.pressed.connect(self.generate)

        layout = QFormLayout()
        layout.addRow("Name", self.Name)
        layout.addRow("Surename", self.Surname)
        layout.addRow("Birthday", self.Birthday)
        layout.addRow("Address", self.Address)
        layout.addRow("Patology", self.Patology)
        layout.addRow("No. of Errors", self.n_errors)

        layout.addRow("Comments", self.comments)
        layout.addRow(self.generate_btn)

        self.setLayout(layout)
        
    def getComboValue(self):
        print((self.comboBox.currentText(), self.comboBox.currentIndex()))
        
    def generate(self):
        self.generate_btn.setDisabled(True)
        data = {
            'Name': self.Name.text(),
            'Surname': self.Surname.text(),
            'Address': self.Address.text(),
            'Patology': str(self.Patology.currentData()),
            'Birthday': self.Birthday.text(),
            'n_errors': str(self.n_errors.value()),
            'Comments': self.comments.toPlainText()
        }
        g = Generator(data)
        g.signals.file_saved_as.connect(self.generated)
        g.signals.error.connect(print)  # Print errors to console.
        self.threadpool.start(g)

    def generated(self, outfile):
        self.generate_btn.setDisabled(False)
        try:
            os.startfile(outfile)
        except Exception:
            # If startfile not available, show dialog.
            QMessageBox.information(self, "Finished", "PDF has been generated")


app = QApplication([])
w = Window()
w.show()
app.exec_()