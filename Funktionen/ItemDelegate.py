__author__ = 'Bruckner Michael'
__version__ = 1.0
__date__ = 20160411

from PySide.QtGui import QStyledItemDelegate, QLineEdit
from Funktionen.EditCommand import EditCommand

class ItemDelegate(QStyledItemDelegate):
    def __init__(self, undoStack, undoRedoText):
        super().__init__()
        self.undoStack = undoStack
        self.edit = None
        self.undoRedoText = undoRedoText

    def setModelData(self, editor, model, index):
        newValue = editor.text()
        self.edit.newValue(newValue)
        self.undoStack.beginMacro("Edit Cell")
        self.undoStack.push(self.edit)
        self.undoStack.endMacro()
        self.undoRedoText()

    def editorEvent(self, event, model, option, index):
        self.edit = EditCommand(model, index)

    def createEditor(self, parent, option, index):
        return QLineEdit(parent)
