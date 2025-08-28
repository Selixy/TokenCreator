from __future__ import annotations
from pathlib import Path
from typing import Iterable, List
from PySide6.QtWidgets import QApplication, QFileDialog

from ui.workspace import Workspace


_VALID_EXT = {
    ".png",
    ".jpg", ".jpeg",
    ".bmp",
    ".tif", ".tiff",
    ".webp",
    ".pbm", ".pgm", ".ppm",
    ".hdr"
}


def _looks_supported(path: Path) -> bool:
    return path.suffix.lower() in _VALID_EXT


def _validate_paths(paths: Iterable[str]) -> List[Path]:
    out: List[Path] = []
    for s in paths:
        p = Path(s)
        if not p.exists() or not p.is_file():
            continue
        if not _looks_supported(p):
            continue
        out.append(p)
    return out


def _open_images_dialog(parent) -> List[Path]:
    start = str(Path.home())
    filt = (
        "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp *.ppm *.pgm *.pbm *.hdr);;"
        "PNG (*.png);;"
        "JPEG (*.jpg *.jpeg);;"
        "Bitmap (*.bmp);;"
        "TIFF (*.tif *.tiff);;"
        "WebP (*.webp);;"
        "PNM (*.pbm *.pgm *.ppm);;"
        "HDR (*.hdr);;"
        "Tous les fichiers (*)"
    )
    files, _ = QFileDialog.getOpenFileNames(parent, "Sélectionner des images", start, filt)
    return _validate_paths(files)


def action_nouveau(window) -> None:
    ws = Workspace.current()
    if ws is None:
        raise RuntimeError("Aucune instance Workspace active.")
    paths = _open_images_dialog(window)
    ws.queue_manager.set_paths(paths)
    print(ws.queue_manager.get_all())


def action_ouvrir(window) -> None:
    action_nouveau(window)


def action_quitter() -> None:
    app = QApplication.instance()
    if app is not None:
        app.quit()
