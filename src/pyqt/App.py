import sys

from PyQt5.QtWidgets import *

from src.pyqt.AppScreen import AppScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = AppScreen()
    view.show()

    sys.exit(app.exec_())
