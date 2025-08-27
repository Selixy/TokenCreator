from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qframelesswindow import FramelessMainWindow
from ui.top_bar import TopBar
from ui.workspace import Workspace


class MainWindow(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TokenMaker")

        # bouton natif
        btn = self.titleBar.closeBtn
        btn.setObjectName("CloseButton")
        btn.style().unpolish(btn)
        btn.style().polish(btn)
        btn.update()

        self.topBar = TopBar(self.titleBar)
        self._place_topbar()
        self.titleBar.installEventFilter(self)

        # workspace central, on soustrais la bare de titre
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 32, 0, 0)
        layout.setSpacing(0)

        self.workspace = Workspace(container)
        layout.addWidget(self.workspace)

        self.setCentralWidget(container)

        self.titleBar.raise_()

        self.resize(900, 600)
        self._init_menu()

    def _place_topbar(self):
        tb = self.titleBar
        try:
            right_limit = tb.minBtn.x()
        except Exception:
            right_limit = tb.width()
        w = max(0, right_limit - 8)
        self.topBar.setGeometry(0, 0, w, tb.height())

        if hasattr(self, "setHitTestVisible"):
            self.setHitTestVisible(self.topBar, True)
        elif hasattr(self, "addIgnoreWidget"):
            self.addIgnoreWidget(self.topBar)

    def eventFilter(self, obj, ev):
        if obj is self.titleBar and ev.type() in (QEvent.Resize, QEvent.Show):
            self._place_topbar()
        return super().eventFilter(obj, ev)

    def _init_menu(self):
        m_file = self.topBar.fileMenu

        a_new = QAction("Nouveau", self)
        a_new.setShortcut(QKeySequence.New)
        a_new.triggered.connect(lambda: self._log("Nouveau"))
        m_file.addAction(a_new)

        a_open = QAction("Ouvrir…", self)
        a_open.setShortcut(QKeySequence.Open)
        a_open.triggered.connect(lambda: self._log("Ouvrir"))
        m_file.addAction(a_open)

        m_file.addSeparator()

        a_quit = QAction("Quitter", self)
        a_quit.setShortcut(QKeySequence.Quit)
        a_quit.triggered.connect(self.close)
        m_file.addAction(a_quit)

    def _log(self, msg):
        print(msg)
