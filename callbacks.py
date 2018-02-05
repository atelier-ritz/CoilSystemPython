from PyQt5 import uic
from PyQt5.QtCore import QFile, QRegExp
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMenu, QMessageBox
from fieldManager import FieldManager
from s826 import S826
#=========================================================
# UI config
#=========================================================
qtCreatorFile = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
field = FieldManager(S826())
#=========================================================
# a class that handles the signal and callbacks of the GUI
#=========================================================
class GUI(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.connectUi()

    def connectUi(self):
        #================================================
        # General Control Tab
        #================================================
        # link to functions
        self.dsb_x.valueChanged.connect(self.on_dsb_x)
        self.dsb_y.valueChanged.connect(self.on_dsb_y)
        self.dsb_z.valueChanged.connect(self.on_dsb_z)
        self.btn_clearCurrent.clicked.connect(self.on_btn_clearCurrent)
        # link slider to doubleSpinBox
        self.dsb_x.valueChanged.connect(lambda value: self.hsld_x.setValue(int(value*100)))
        self.dsb_y.valueChanged.connect(lambda value: self.hsld_y.setValue(int(value*100)))
        self.dsb_z.valueChanged.connect(lambda value: self.hsld_z.setValue(int(value*100)))
        self.hsld_x.valueChanged.connect(lambda value: self.dsb_x.setValue(float(value/100)))
        self.hsld_y.valueChanged.connect(lambda value: self.dsb_y.setValue(float(value/100)))
        self.hsld_z.valueChanged.connect(lambda value: self.dsb_z.setValue(float(value/100)))
        #================================================
        # Vision Tab
        #================================================

    def on_dsb_x(self,val):
        val = self.dsb_x.value()
        # field.setX(val)

    def on_dsb_y(self,val):
        val = self.dsb_y.value()
        # field.setY(val)

    def on_dsb_z(self,val):
        val = self.dsb_z.value()
        # field.setZ(val)

    def on_btn_clearCurrent(self):
        self.dsb_x.setValue(0)
        self.dsb_y.setValue(0)
        self.dsb_z.setValue(0)
        # field.setXYZ(0,0,0)
