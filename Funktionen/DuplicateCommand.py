__author__ = 'Bruckner Michael'
__version__ = 1.0
__date__ = 20160411

from PySide.QtGui import *

class DuplicateCommand(QUndoCommand):

    def __init__(self, model, index):
        QUndoCommand.__init__(self)
        self.__model = model
        self.__index = index

    def redo(self):
        self.__model.duplicateRow(self.__index)

    def undo(self):
        self.__model.removeRows(self.__index, 1)