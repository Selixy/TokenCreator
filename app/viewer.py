from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QFileDialog, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtSvgWidgets import QSvgWidget  # <- module correct pour SVG widget

RASTER_EXT = {".png", ".jpg", ".jpeg", ".bmp"}
SVG_EXT = {".svg"}

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Viewer minimal")
        self.label = QLabel("Aucune image chargée", alignment=Qt.AlignCenter)
        self.setCentralWidget(self.label)
        self._pix = None

        self.open_image()

    def open_image(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Choisir une image", "", "Images (*.png *.jpg *.jpeg *.bmp *.svg)"
        )
        if not file:
            return

        ext = Path(file).suffix.lower()
        if ext in RASTER_EXT:
            self._show_raster(file)
        elif ext in SVG_EXT:
            self._show_svg(file)
        else:
            self.label.setText("Format non pris en charge")

    def _show_raster(self, path: str):
        pix = QPixmap(path)
        if pix.isNull():
            self.label.setText("Erreur: impossible de charger l'image.")
            return
        self._pix = pix
        self._update_label_pixmap()

    def _show_svg(self, path: str):
        svg = QSvgWidget(path)
        self._pix = None
        self.setCentralWidget(svg)

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self._update_label_pixmap()

    def _update_label_pixmap(self):
        if self.centralWidget() is self.label and self._pix is not None:
            scaled = self._pix.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(scaled)
