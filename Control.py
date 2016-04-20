__author__ = 'Bruckner Michael'
__version__ = 2.7
__date__ = 20160412

from GUI import GUI
import os
import sys
from orderedset.OrderedSet import OrderedSet
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
from Results import ResultsController

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
        self.db = SQL(self.username, self.password, self.database, self.wahltermin)

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
        self.gui.actionHochrechnung.triggered.connect(self.hochrechnung)
        self.gui.actionUndo.triggered.connect(self.undo)
        self.gui.actionRedo.triggered.connect(self.redo)

    def einlesen(self):
        """
        Ruft die Funktion writeList auf mittels welcher in die Datenbank geschrieben werden kann.
        :return:
        """
        try:
            liste = self.tablemodel.getList()
            self.db.writeList(liste)
        except Exception as e:
            print(e)

        QtGui.QMessageBox.information(self, "Einlesen", "Das Einlesen in die Datenbank hat geklappt! :D")

    def auslesen(self):
        """
        Ruft die Funktion loadlist auf mittels welcher die Daten aus der Datenbakn ausgelesen werden.
        :return:
        """
        try:
            datalist, header = self.db.loadList()
            self.update_table(datalist, header)
        except Exception as e:
            print(e)

        QtGui.QMessageBox.information(self, "Auslesen", "Das Auselen aus der Datenbank hat geklappt! :D")

    def hochrechnung(self):
        """
        Es wird die Funktion results aufgerufen und eine neues Fenster geöffnet, in welchem die
        Hochrechnung angezeigt wird.
        :return:
        """
        datalist, header = self.db.results()
        rechnung = ResultsController(datalist, header, title="Hochrechnung in %")
        rechnung.show()

    def closegui(self):
        """
        Die Funktion wird aufgerufen, wenn das Programm geschlossen werden soll.
        Es wird vor dem Schliessen abgefrag, ob man wirklich beenden will.
        :return:
        """
        result = QtGui.QMessageBox.question(QtGui.QWidget(),
        'Exit',"Moechten Sie das Programm wirklich beenden?\n Alle ungespeicherten Daten gehen verloren!",
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:
            QtGui.QMessageBox.information(self, "Bye Bye", "Bis zum nächsten Mal! :D")
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
        if self.tablemodel.getHeader() == [] and self.tablemodel.getList() == []:
            fname = QtGui.QFileDialog.getOpenFileName(self.mwindow, 'Open file...', os.getcwd(), "CSV (*.csv)")[0]
            if len(fname) > 0:
                self.model.currentfile = fname
                datalist, header = self.model.read_csv(fname)
                self.update_table(datalist, header)
        else:
            result = QtGui.QMessageBox.question(QtGui.QWidget(),
            'Open',"Moechten Sie wirklich eine neues File öffnen?\n Alle ungespeicherten Daten gehen verloren!",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if result == QtGui.QMessageBox.Yes:
                fname = QtGui.QFileDialog.getOpenFileName(self.mwindow, 'Open file...', os.getcwd(), "CSV (*.csv)")[0]
                if len(fname) > 0:
                    self.model.currentfile = fname
                    datalist, header = self.model.read_csv(fname)
                    self.update_table(datalist, header)
            else:
                pass


    def insertintable(self):
        """
        Erzeugt eine neuen Zeile (oberhalb der aktuellen Zeile)
        :return:
        """
        index, amount = self.get_selectedcell()
        self.undoStack.beginMacro("Add Row")
        self.undoStack.push(InsertCommand(self.tablemodel, index, 1))
        self.undoStack.endMacro()
        self.undoText_redoText()

    def removefromtable(self):
        """
        Entfernt eine asugewaehlte Zeile
        :return:
        """
        index, amount = self.get_selectedcell()
        if index != len(self.tablemodel.getList()):
            self.undoStack.beginMacro("Remove Row/s")
            self.undoStack.push(RemoveCommand(self.tablemodel, index, amount))
            self.undoStack.endMacro()
            self.undoText_redoText()

    def copycell(self):
        """
        Kopiert einzelne Zelle
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
        """
        Kopiert Wert in eine ausgewaehlte Zelle
        :return:
        """
        clipboard = QApplication.clipboard()
        index = self.gui.tableView.selectionModel().selectedIndexes()[0]
        command = EditCommand(self.tablemodel, index)
        command.newValue(str(clipboard.text()))
        self.undoStack.push(command)
        self.gui.tableView.reset()

    def duplicatecell(self):
        """
        Duplizieren der aktuellen Zeile (inklusive einfuegen unterhalb der aktuellen Zeile)
        Der erste Index einer Zeile muss ausgewaehlt werden um zu duplizieren, also den Wert
        in der ersten Spalte waehlen.
        """
        index, amount = self.get_selectedcell()
        self.undoStack.beginMacro("Duplicate Row")
        self.undoStack.push(DuplicateCommand(self.tablemodel, index))
        self.undoStack.endMacro()
        self.undoText_redoText()
        self.gui.tableView.reset()

    def update_table(self, datlist, header):
        """
        Erzeugt eine neue Tabelle mit den Listen datalist und header
        :param datlist: es wird die neue datalist uebergeben
        :param header:  es wird der neue header uebergeben
        :return:
        """
        self.tablemodel.set_list(datlist, header)
        self.gui.tableView.reset()
        self.gui.tableView.setModel(self.tablemodel)

    def selectedcell(self):
        si = self.gui.tableView.selectedIndexes()
        return [index for index in si if not index.column()]

    def get_selectedcell(self):
        si = self.selectedcell()
        if not si:
            return self.tablemodel.rowCount(self), 1
        fsi = si[0]
        si = self.selectedcell()
        row = fsi.row()

        return row, len(si)

    def savefile(self):
        """
        Speichert das File unter dem Namen unter welchem es geoeffnet wurde.
        Hat das File noch keinen Namen wird die Methode saveas aufgerufen.
        :return:
        """
        if self.filename is not None:
            self.model.write_csv(self.tablemodel.getList(), self.filename)
        else:
            self.saveas()
        QtGui.QMessageBox.information(self, "Speichern", "Das File wurde gespeichert! :D")

    def saveas(self):
        """
        Fuehrt die Methode savefile aus um Files zu speichern.
        Es wird beim Aufruf ein Fenster erzeugt, indem der User den Filenamen
        festlegt und den Speicherort auswaehlt.
        :return:
        """
        filename = QFileDialog.getSaveFileName(self, caption="Save CSV-File", dir=self.filename, filter="CSV-File (*.csv)")[0]
        if len(filename) > 0:
            self.filename = filename
            self.savefile()

    def newfile(self):
        """
        Erzeugt eine neue Tabelle.
        :return:
        """
        self.filename = None
        result = QtGui.QMessageBox.question(QtGui.QWidget(),
        'Open',"Moechten Sie wirklich eine neue Tabelle erstellen?\n Alle ungespeicherten Daten gehen verloren!",
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:
            #header = ['WK','SPR', 'BZ', 'WBER', 'ABG', 'UNG','ANDAS','FPOE','FREIE','GFW','GRUE','M','NEOS','OEVP','SLP','SPOE','WIFF','WWW',]
            self.tablemodel.set_list([], self.tablemodel.getHeader())
        else:
            pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    controller = Controller()
    controller.show()
    sys.exit(app.exec_())
