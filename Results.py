from PySide import QtGui

from PySide.QtGui import QDialog, QVBoxLayout

from TableModel import Table


class ResultsController(QDialog):

    def __init__(self, data, header, title, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        tablemodel = Table(datalist=[], header=[], parent=self)
        tablemodel.set_list(data, header)

        self.gui = QtGui.QTableView(self)
        self.gui.setModel(tablemodel)
        self.gui.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.gui.resizeColumnsToContents()
        layout.addWidget(self.view)

        self.setWindowTitle(title)
        self.resize(850,120)
        self.setModal(True)
        self.exec_()