import sys
from callbacks import GUI
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    window.move(1050, 0) # position of the main GUI
    sys.exit(app.exec_())
