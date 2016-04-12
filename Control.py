__author__ = 'Bruckner Michael'
__version__ = 2.7
__date__ = 20160412

from GUI import GUI
import os
import sys
from PySide.QtGui import *
from PySide import *
from TableModel import Table
from Model import Model
from PySide.QtCore import Qt
from Funktionen.EditCommand import EditCommand
from Funktionen.RemoveCommand import RemoveCommand
from Funktionen.InsertCommand import InsertCommand
from Funktionen.DuplicateCommand import DuplicateCommand
from Funktionen.ItemDelegate import ItemDelegate
from sql.SQL import SQL

class Controller(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filename = None
        self.mwindow = QtGui.QMainWindow()
        self.model = Model(self.mwindow)
        self.gui = GUI.Ui_MainWindow()
        self.gui.setupUi(self)
        self.tableView = self.gui.tableView
        self.tablemodel = Table(parent=self, datalist=[], header=[])
        self.role = Qt.DisplayRole
        self.signals()
        self.undoStack = QUndoStack()
        self.gui.tableView.setItemDelegate(ItemDelegate(self.undoStack, self.undoText_redoText))
        self.username = "root"
        self.password = "root"
        self.database = "wahlen"
        self.wahltermin = "2016-04-24"
        try:
            self.db = SQL(self.username, self.password, self.database, self.wahltermin)
        except Exception as e:
            print(e)

    def signals(self):
        self.gui.actionOpen.triggered.connect(self.csvfile)
        self.gui.actionExit.triggered.connect(self.closegui)
        self.gui.actionInsert.triggered.connect(self.insertintable)
        self.gui.actionDelete.triggered.connect(self.removefromtable)
        self.gui.actionDuplicate.triggered.connect(self.duplicatecell)
        self.gui.actionCopy.triggered.connect(self.copycell)
        self.gui.actionCut.triggered.connect(self.cutcell)
        self.gui.actionPaste.triggered.connect(self.pastecell)
        self.gui.actionNew.triggered.connect(self.newfile)
        self.gui.actionSave.triggered.connect(self.savefile)
        self.gui.actionSave_As.triggered.connect(self.saveas)
        self.gui.actionEinlesen.triggered.connect(self.einlesen)
        self.gui.actionAuslesen.triggered.connect(self.auslesen)

    def einlesen(self):
        try:
            liste = self.tablemodel.getList()
            self.db.writeList(liste)
        except Exception as e:
            print(e)

    def auslesen(self):
        try:
            datalist, header = self.db.loadList()
            self.update_table(datalist, header)
        except Exception as e:
            print(e)

    def closegui(self):
        result = QtGui.QMessageBox.question(QtGui.QWidget(),
        'Exit',"Moechten Sie das Programm wirklich beenden?\n Alle ungespeicherten Daten gehen verloren!",
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:
            self.close()
        else:
            pass

    def undoText_redoText(self):
        undo = "Undo"
        redo = "Redo"
        utext = self.undoStack.undoText()
        rtext = self.undoStack.redoText()
        if utext:
            undo += " \"" + utext + "\""
            self.gui.actionUndo.setText(undo)
        if rtext:
            redo += " \"" + rtext + "\""
            self.gui.actionRedo.setText(redo)

    def undo(self):
        self.undoStack.undo()
        self.undoText_redoText()
        self.gui.tableView.reset()

    def redo(self):
        self.undoStack.redo()
        self.undoText_redoText()
        self.gui.tableView.reset()

    def csvfile(self):
        """
        Mit dieser Methode wird das ausgewaehlte CSV-File in die Tabelle importiert
        :return:
        """
        fname = QtGui.QFileDialog.getOpenFileName(self.mwindow, 'Open file...', os.getcwd(), "CSV (*.csv)")[0]
        if len(fname) > 0:
            self.model.currentfile = fname
            datalist, header = self.model.read_csv(fname)
            self.update_table(datalist, header)

    def insertintable(self):
        """
        Erzeugt eine neuen Zeile (unterhalb der aktuellen Zeile)
        :return:
        """
        index, amount = self.get_selctedcell()
        self.undoStack.beginMacro("Add Row")
        self.undoStack.push(InsertCommand(self.tablemodel, index, 1))
        self.undoStack.endMacro()
        self.undoText_redoText()

    def removefromtable(self):
        """
        Entfernt eine asugewaehlte Zeile
        :return:
        """
        index, amount = self.get_selctedcell()
        if index != len(self.tablemodel.getList()):
            self.undoStack.beginMacro("Remove Row/s")
            self.undoStack.push(RemoveCommand(self.tablemodel, index, amount))
            self.undoStack.endMacro()
            self.undoText_redoText()

    def copycell(self):
        """
        Kopiert einzelne Zellen
        :return:
        """
        clipboard = QApplication.clipboard()
        si = self.gui.tableView.selectionModel().selectedIndexes()[0]
        st = str(self.tablemodel.data(si))
        clipboard.setText(st)

    def cutcell(self):
        """
        Schneidet eine Zelle aus
        :return:
        """
        self.copycell()
        index = self.gui.tableView.selectionModel().selectedIndexes()[0]
        command = EditCommand(self.tablemodel, index)
        command.newValue("")
        self.undoStack.beginMacro("Cut")
        self.undoStack.push(command)
        self.undoStack.endMacro()
        self.undoText_redoText()
        self.gui.tableView.reset()

    def pastecell(self):
        clipboard = QApplication.clipboard()
        index = self.gui.tableView.selectionModel().selectedIndexes()[0]
        command = EditCommand(self.tablemodel, index)
        command.newValue(str(clipboard.text()))
        self.undoStack.push(command)
        self.gui.tableView.reset()

    def duplicatecell(self):
        """
        Duplizieren der aktuellen Zeile (inklusive einfuegen unterhalb der aktuellen Zeile)
        Der erste Index einer Zeile muss augewaehlt werden um zu duplizieren, also den Wert
        in der ersten Spalte waehlen.
        """
        index, amount = self.get_selctedcell()
        self.undoStack.beginMacro("Duplicate Row")
        self.undoStack.push(DuplicateCommand(self.tablemodel, index))
        self.undoStack.endMacro()
        self.undoText_redoText()
        self.gui.tableView.reset()

    def get_selctedcell(self):
        si = self.selectedcell()
        if not si:
            return self.tablemodel.rowCount(self), 1
        fsi = si[0]
        si = self.selectedcell()
        row = fsi.row()

        return row, len(si)

    def update_table(self, datlist, header):
        self.tablemodel.set_list(datlist, header)
        self.gui.tableView.reset()
        self.gui.tableView.setModel(self.tablemodel)

    def selectedcell(self):
        si = self.gui.tableView.selectedIndexes()
        return [index for index in si if not index.column()]

    def savefile(self):
        if self.filename is not None:
            self.model.write_csv(self.tablemodel.getList(), self.filename)
        else:
            self.saveas()

    def saveas(self):
        filename = QFileDialog.getSaveFileName(self, caption="Save CSV-File", dir=self.filename, filter="CSV-File (*.csv)")[0]
        if len(filename) > 0:
            self.filename = filename
            self.savefile()

    def newfile(self):
        self.filename = None
        self.tablemodel.set_list([], [])


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    controller = Controller()
    controller.show()
    sys.exit(app.exec_())
