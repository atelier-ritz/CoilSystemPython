# from s826 import S826
# from fieldManager import FieldManager
import sys
from callbacks import GUI
from PyQt5 import QtCore, QtGui, QtWidgets,  uic
from PyQt5.QtGui import QPixmap

if __name__ == "__main__":
    # field = FieldManager(S826())
    # field.setXYZ(0,0,0)
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
