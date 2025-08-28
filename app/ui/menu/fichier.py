# menu/fichier.py
from __future__ import annotations
from typing import Callable, Dict
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMenu

# API minimale : on peuple le menu "Fichier" et on renvoie les actions.
def populate_fichier_menu(
    menu: QMenu,
    on_new: Callable[[], None],
    on_open: Callable[[], None],
    on_quit: Callable[[], None],
) -> Dict[str, QAction]:
    menu.clear()

    a_new = QAction("Nouveau", menu)
    a_new.setShortcut(QKeySequence.New)
    a_new.triggered.connect(on_new)
    menu.addAction(a_new)

    a_open = QAction("Ouvrir…", menu)
    a_open.setShortcut(QKeySequence.Open)
    a_open.triggered.connect(on_open)
    menu.addAction(a_open)

    menu.addSeparator()

    a_quit = QAction("Quitter", menu)
    a_quit.setShortcut(QKeySequence.Quit)
    a_quit.triggered.connect(on_quit)
    menu.addAction(a_quit)

    return {
        "new": a_new,
        "open": a_open,
        "quit": a_quit,
    }
