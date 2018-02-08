import sys
from callbacks import GUI
from PyQt5 import QtCore, QtGui, QtWidgets,  uic
from PyQt5.QtGui import QPixmap

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
