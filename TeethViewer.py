import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.Qt import *
from functools import partial
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush

import References as ref
import DataSaver as DataSaverModule           # Also used to navigate with os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()


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
        b = QLabel('Bot \n Left' , self )         
        
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
        grid_layout.addWidget(b, 2,1)
        grid_layout.addWidget(self.b17, 2,2)
        grid_layout.addWidget(self.b18, 2,3)
        grid_layout.addWidget(self.b19, 2,4)
        grid_layout.addWidget(self.b20, 2,5)
        grid_layout.addWidget(self.b21, 2,6)
        grid_layout.addWidget(self.b22, 2,7)
        grid_layout.addWidget(self.b23, 2,8)
        grid_layout.addWidget(self.b24, 2,9)
        grid_layout.addWidget(self.b25, 2,10)
        grid_layout.addWidget(self.b26, 2,11)
        grid_layout.addWidget(self.b27, 2,12)
        grid_layout.addWidget(self.b28, 2,13)
        grid_layout.addWidget(self.b29, 2,14)
        grid_layout.addWidget(self.b30, 2,15)
        grid_layout.addWidget(self.b31, 2,16)
        grid_layout.addWidget(self.b32, 2,17)
        layout.addWidget(self.saveButton)
        
        self.group.buttonClicked.connect(self.check_button)                 # +++
        self.saveButton.clicked.connect(self.saveData)
        self.saveButton.clicked.connect(self.close)
      
    def saveData(self):
        a = ""
        for b in self._dictRB:
            if self._dictRB[b] == False:
                a += 'f'
            else:
                a += 't'
                   
        return a     
                
    
 
    def check_button(self, radioButton):                                    # +++
        self._dictRB["rb"+radioButton.text()] = not self._dictRB["rb"+radioButton.text()]
        
        print("clickеd button -> `{} - {}`".format(radioButton.text(), radioButton.isChecked()))        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setFixedSize(1293, 524)
    #window.fixed_aspect_ratio = 16
    window.show()
    app.exec_()