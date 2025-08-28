from __future__ import annotations
import weakref
import numpy as np

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap

from logic.image_buffer import ImageBuffer
from logic.queue_manager import QueueManager


class Workspace(QWidget):
    _current_ref: weakref.ReferenceType["Workspace"] | None = None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("WorkspaceRoot")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._label = QLabel(self)
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._label.setText("Aucune image")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._label)

        self._qimage: QImage | None = None

        # Enfants : créés ICI (exigence)
        self.image_buffer = ImageBuffer(workspace=self)
        self.queue_manager = QueueManager(image_buffer=self.image_buffer)

        # Enregistre cette instance comme “courante”
        Workspace._current_ref = weakref.ref(self)

    @classmethod
    def current(cls) -> "Workspace | None":
        return cls._current_ref() if cls._current_ref else None

    # ---------- API publique ----------
    def show_from_buffer(self, buffer: np.ndarray) -> None:
        if not isinstance(buffer, np.ndarray):
            raise TypeError("buffer doit être un np.ndarray")
        if buffer.dtype != np.uint8:
            raise TypeError("buffer doit être de type uint8")
        if buffer.ndim != 3 or buffer.shape[2] != 4:
            raise ValueError("buffer doit avoir la forme (H, W, 4) en RGBA")

        buffer = np.ascontiguousarray(buffer)
        h, w, _ = buffer.shape

        img = QImage(buffer.data, w, h, 4 * w, QImage.Format.Format_RGBA8888)
        self._qimage = img.copy()
        self._update_scaled_pixmap()

    # ---------- Implémentation ----------
    def _update_scaled_pixmap(self) -> None:
        if self._qimage is None or self.width() <= 0 or self.height() <= 0:
            return
        scaled = self._qimage.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._label.setPixmap(QPixmap.fromImage(scaled))

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._update_scaled_pixmap()
