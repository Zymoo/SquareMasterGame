import sys

from PySide2.QtWidgets import QApplication

from src.qt.AppScreen import AppScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = AppScreen()
    view.show()

    sys.exit(app.exec_())
