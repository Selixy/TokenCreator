from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qframelesswindow import FramelessMainWindow
from ui.top_bar import TopBar
from ui.workspace import Workspace
from functools import partial
from logic.fichier import action_nouveau, action_ouvrir, action_quitter

class MainWindow(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TokenMaker")

        # bouton natif (facultatif: style)
        btn = self.titleBar.closeBtn
        btn.setObjectName("CloseButton")
        btn.style().unpolish(btn); btn.style().polish(btn); btn.update()

        # superposer la TopBar dans la barre native
        self.topBar = TopBar(self.titleBar)
        self._place_topbar()
        self.titleBar.installEventFilter(self)

        # central: marge haute = 32 (barre native)
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 32, 0, 0)
        layout.setSpacing(0)

        self.workspace = Workspace(container)
        layout.addWidget(self.workspace)
        self.setCentralWidget(container)

        self.titleBar.raise_()
        self.resize(900, 600)


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
