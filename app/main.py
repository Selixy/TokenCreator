import sys
from PySide6.QtWidgets import QApplication
from viewer import ImageViewer

def main():
    app = QApplication(sys.argv)
    w = ImageViewer()
    w.resize(800, 600)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()