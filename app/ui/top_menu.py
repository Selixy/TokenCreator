# ui/top_menu.py
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QWidget, QHBoxLayout, QToolButton, QMenu, QSizePolicy

try:
    from ui.rounded_menu import enable_win11_round_corners
except Exception:
    def enable_win11_round_corners(*args, **kwargs):
        return False


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

        self._connect_rounding(self.fileMenu)

    def _connect_rounding(self, menu: QMenu) -> None:
        menu.aboutToShow.connect(lambda m=menu: enable_win11_round_corners(m, 2))

    def setMenu(self, menu: QMenu | None) -> None:
        if menu is None:
            menu = QMenu(self.fileBtn)
            menu.setObjectName("FileMenu")

        self.fileMenu = menu
        self.fileBtn.setMenu(menu)

        self._connect_rounding(menu)

    def init_file_menu(self, on_new, on_open, on_quit):
        m = self.fileMenu
        m.clear()

        a_new  = QAction("Nouveau", self); a_new.setShortcut(QKeySequence.New)
        a_open = QAction("Ouvrir…", self); a_open.setShortcut(QKeySequence.Open)
        a_quit = QAction("Quitter", self); a_quit.setShortcut(QKeySequence.Quit)

        a_new.triggered.connect(on_new)
        a_open.triggered.connect(on_open)
        a_quit.triggered.connect(on_quit)

        m.addAction(a_new)
        m.addAction(a_open)
        m.addSeparator()
        m.addAction(a_quit)

        return {"new": a_new, "open": a_open, "quit": a_quit}
