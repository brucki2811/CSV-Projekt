author__ = 'Bruckner Michael'
__version__ = 1.0
__date__ = 20160411

from PySide.QtGui import *

class InsertCommand(QUndoCommand):
    def __init__(self, model, index, amount):
        QUndoCommand.__init__(self)
        self.__model = model
        self.__index = index
        self.__amount = amount

    def redo(self):
        self.__model.insertRows(self.__index, self.__amount)

    def undo(self):
        self.__model.removeRows(self.__index, self.__amount)
