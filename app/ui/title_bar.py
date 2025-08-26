from PySide6.QtCore import Qt, QEvent, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QSizePolicy, QStyle, QSpacerItem, QMenu, QToolButton
)
from ui.top_menu import TopMenu


class TitleBar(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("TitleBar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(32)

        self.iconSource: QIcon | QPixmap | str | None = None
        self.filteredWindow: QWidget | None = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(11, 9, 0, 0)
        layout.setSpacing(5)

        # Icône
        self.icon_lbl = QLabel(self)
        self.icon_lbl.setObjectName("TitleBarIcon")
        self.icon_lbl.setAlignment(Qt.AlignCenter)
        self.icon_lbl.setScaledContents(False)
        self.icon_lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.syncIconLabelSize()

        # Top menu
        self.topMenu = TopMenu(self)

        # Spacer
        layout.addWidget(self.icon_lbl)
        layout.addWidget(self.topMenu)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Sync icône fenêtre
        self.installWindowFilter()

    # ---------- Vestiges ----------
    @property
    def fileMenu(self) -> QMenu:
        return self.topMenu.fileMenu

    @fileMenu.setter
    def fileMenu(self, menu: QMenu | None) -> None:
        self.topMenu.setMenu(menu)

    # ----------------- Icône -----------------
    def styleIconSize(self) -> int:
        px = self.style().pixelMetric(QStyle.PM_SmallIconSize, None, self)
        if px <= 0:
            px = max(16, int(self.height() * 0.6))
        return px

    def syncIconLabelSize(self) -> None:
        s = self.styleIconSize()
        self.icon_lbl.setFixedSize(s, s)

    def renderIcon(self) -> None:
        target: QSize = self.icon_lbl.size()
        if target.isEmpty():
            self.icon_lbl.clear()
            return

        src = self.iconSource
        pm: QPixmap | None = None
        if isinstance(src, QIcon):
            pm = src.pixmap(target)
        elif isinstance(src, QPixmap):
            pm = src.scaled(target, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        elif isinstance(src, str) and src:
            p = QPixmap(src)
            if not p.isNull():
                pm = p.scaled(target, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        if pm is None or pm.isNull():
            self.icon_lbl.clear()
        else:
            self.icon_lbl.setPixmap(pm)

    def setIcon(self, icon: QIcon | QPixmap | str | None) -> None:
        """Fixer une icône explicite pour la barre (remplace l’icône de fenêtre)."""
        self.iconSource = icon
        self.renderIcon()

    def updateIconFromWindow(self) -> None:
        """Si aucune icône explicite, utiliser l’icône de la fenêtre."""
        if self.iconSource is not None:
            return
        win = self.window()
        win_icon = win.windowIcon() if win else QIcon()
        if not win_icon.isNull():
            self.iconSource = win_icon
            self.renderIcon()
        else:
            self.icon_lbl.clear()

    # ----------------- Sync avec la fenêtre -----------------
    def installWindowFilter(self) -> None:
        win = self.window()
        if self.filteredWindow is win:
            return
        if self.filteredWindow is not None:
            self.filteredWindow.removeEventFilter(self)
        self.filteredWindow = win
        if win is not None:
            win.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.filteredWindow and event.type() == QEvent.WindowIconChange:
            self.iconSource = None
            self.updateIconFromWindow()
        return super().eventFilter(obj, event)

    def changeEvent(self, e):
        if e.type() in (QEvent.ParentChange, QEvent.ParentAboutToChange):
            self.installWindowFilter()
        return super().changeEvent(e)

    def showEvent(self, e):
        self.updateIconFromWindow()
        return super().showEvent(e)

    # ----------------- Resize handling -----------------
    def resizeEvent(self, e) -> None:
        prev = self.icon_lbl.size()
        self.syncIconLabelSize()
        if self.icon_lbl.size() != prev:
            self.renderIcon()
        super().resizeEvent(e)
