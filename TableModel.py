author__ = 'Bruckner Michael'
__version__ = 2.0
__date__ = 20160410
__author__ = 'Bruckner Michael'
__version__ = 1.5
__date__ = 20160412

from PySide.QtCore import QAbstractTableModel, Qt, SIGNAL, QModelIndex

class Table(QAbstractTableModel):
    def __init__(self, parent, datalist, header):
        super().__init__()
        self.list = []
        self.header = []
        self.set_list(datalist, header)

    def set_list(self, datalist, header):
        self.emit(SIGNAL("layoutToBeChanged()"))
        self.list = datalist
        self.header = header
        self.emit(SIGNAL("layoutChanged()"))

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.list[index.row()][self.header[index.column()]]

    def rowCount(self, parent):
        return len(self.list)

    def columnCount(self, parent):
        return len(self.header)

    def getList(self):
        return self.list

    def getHeader(self):
        return self.header

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def flags(self, *args, **kwargs):
        return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setData(self, *args):
        self.list[args[0].row()][self.header[args[0].column()]] = args[1]
        # self.emit(SIGNAL("dataChanged()"))
        return True

    def insertRow(self, row, rows, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row + rows - 1)
        for tmp in range(rows):
            self.daten.insert(row, {key: "" for key in self.header})
        self.endInsertRows()
        return True

    def duplicateRow(self, rindex, parent=QModelIndex()):
        self.beginInsertRows(parent, rindex, 1)
        row = self.list[rindex].copy()
        self.list.insert(rindex+1, {key: "" for key in self.header})
        self.list[rindex+1] = row
        self.endInsertRows()

    def removeRows(self, row, rows, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + rows - 1)
        del self.list[row:row + rows]
        self.endRemoveRows()
        return True
