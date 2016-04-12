from PySide.QtGui import *

class RemoveCommand(QUndoCommand):
    def __init__(self, model, index, amount):
        QUndoCommand.__init__(self)
        self.__model = model
        self.__index = index
        self.__amount = amount
        self.__oldList = None
        self.__oldHeader = None

    def redo(self):
        self.__oldHeader = list(self.__model.getHeader())
        self.__oldList = list(self.__model.getList())
        self.__model.removeRows(self.__index, self.__amount)

    def undo(self):
        self.__model.set_list(self.__oldList, self.__oldHeader)
