from PySide6.QtGui import QAction, QKeySequence, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from qframelesswindow import FramelessMainWindow
from ui.title_bar import TitleBar

class MainWindow(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        
        btn = self.titleBar.closeBtn
        btn.setObjectName("CloseButton")
        btn.style().unpolish(btn)
        btn.style().polish(btn)
        btn.update()

        self.titlebar = TitleBar(self)
        self.setWindowTitle("TokenMaker")
        self.resize(900, 600)
        self._init_menu()



    def _init_menu(self):
        m_file = self.titlebar.fileMenu

        a_new = QAction("Nouveau", self); a_new.setShortcut(QKeySequence.New)
        a_new.triggered.connect(lambda: self._log("Nouveau")); m_file.addAction(a_new)

        a_open = QAction("Ouvrir…", self); a_open.setShortcut(QKeySequence.Open)
        a_open.triggered.connect(lambda: self._log("Ouvrir")); m_file.addAction(a_open)

        m_file.addSeparator()

        a_quit = QAction("Quitter", self); a_quit.setShortcut(QKeySequence.Quit)
        a_quit.triggered.connect(self.close); m_file.addAction(a_quit)

