from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QToolButton, QMenu, QSizePolicy
from ui.rounded_menu import enable_win11_round_corners

class TopMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TopMenu")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.fileBtn = QToolButton(self)
        self.fileBtn.setObjectName("FileBtn")
        self.fileBtn.setText("Fichier")
        self.fileBtn.setAutoRaise(True)
        self.fileBtn.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.fileBtn.setPopupMode(QToolButton.InstantPopup)
        self.fileBtn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addWidget(self.fileBtn)

        self.fileMenu = QMenu(self.fileBtn)
        self.fileMenu.setObjectName("FileMenu")
        self.fileBtn.setMenu(self.fileMenu)

        self.fileMenu.aboutToShow.connect(lambda: enable_win11_round_corners(self.fileMenu, 2))

    # API minimale
    def setMenu(self, menu: QMenu | None) -> None:
        if menu is None:
            menu = QMenu(self.fileBtn)
            menu.setObjectName("FileMenu")
        self.fileMenu = menu
        self.fileBtn.setMenu(menu)

    def addFileAction(self, *args, **kwargs):
        return self.fileMenu.addAction(*args, **kwargs)

    def setFileButtonText(self, text: str) -> None:
        self.fileBtn.setText(text)
