__author__ = 'Bruckner Michael'
__version__ = 1.0
__date__ = 20160221

import sys
from PySide import QtCore, QtGui
import GUI

class Main(QtGui.QMainWindow,GUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gui = GUI.Ui_MainWindow()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = GUI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

