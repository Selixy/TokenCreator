from __future__ import annotations
from pathlib import Path
import numpy as np
import cv2

if False:
    from ui.workspace import Workspace


class ImageBuffer:
    def __init__(self, workspace: "Workspace") -> None:
        self._workspace = workspace
        self._buffer: np.ndarray | None = None

    def load_image(self, path: str | Path) -> None:

        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(path)

        img = cv2.imread(str(p), cv2.IMREAD_UNCHANGED)
        if img is None:
            raise IOError(f"Impossible de lire l'image: {path}")

        self._buffer = self._to_rgba(img)
        self._workspace.show_from_buffer(self._buffer)

    @staticmethod
    def _to_rgba(img: np.ndarray) -> np.ndarray:
        """ OpenCV ndarray -> ndarray RGBA8 (H, W, 4) """
        if img.ndim == 2:
            # Niveaux de gris -> RGB
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
        elif img.shape[2] == 3:
            # BGR -> RGBA
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        elif img.shape[2] == 4:
            # BGRA -> RGBA
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        else:
            raise ValueError(f"Format d'image non supporté: shape={img.shape}")

        return img.astype(np.uint8, copy=False)
