# app/__main__.py
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.mainwindow import MainWindow
from ui.apply_theme import apply_theme
from ui.menu.setup import setup_menus

def resolve_icon() -> str | None:
    candidates = []
    if getattr(sys, "frozen", False):
        meipass = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        candidates += [meipass / "icons" / "app.ico", Path(sys.executable).parent / "icons" / "app.ico"]
    here = Path(__file__).resolve().parent
    candidates += [here.parent / "icons" / "app.ico", here / "icons" / "app.ico"]
    for p in candidates:
        if p.exists():
            return str(p)
    return None

def main():
    app = QApplication(sys.argv)
    apply_theme(app, "dark")

    ico = resolve_icon()
    if ico:
        app.setWindowIcon(QIcon(ico))

    w = MainWindow()
    if ico:
        w.setWindowIcon(QIcon(ico))

    setup_menus(w)

    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
