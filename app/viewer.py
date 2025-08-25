from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QFileDialog, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtSvgWidgets import QSvgWidget

RASTER_EXT = {".png", ".jpg", ".jpeg", ".bmp"}
SVG_EXT = {".svg"}

class ImageViewer(QMainWindow):
    """
    Fenêtre principale minimale.
    Hérite de QMainWindow, définit juste un titre et une taille.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageViewer — Fenêtre vide")
        self.resize(800, 600)
