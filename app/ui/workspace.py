from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class Workspace(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("WorkspaceRoot")
        self.setAttribute(Qt.WA_StyledBackground, True) 




