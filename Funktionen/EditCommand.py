__author__ = 'Bruckner Michael'
__version__ = 1.0
__date__ = 20160411

from PySide.QtGui import *

class EditCommand(QUndoCommand):
    def __init__(self, model, index):
        QUndoCommand.__init__(self)
        self.__newValue = None
        self.__model = model
        self.__index = index
        self.__oldValue = None

    def redo(self):
        self.__oldValue = self.__model.data(self.__index)
        self.__model.setData(self.__index, self.__newValue)

    def undo(self):
        self.__newValue = self.__model.data(self.__index)
        self.__model.setData(self.__index, self.__oldValue)

    def setText(self, *args, **kwargs):
        super().setText(*args, **kwargs)

    def newValue(self, newValue):
        self.__newValue = newValue
