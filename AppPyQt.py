import sys

from PyQt5.QtWidgets import *

from AppScreenPyQt import AppScreenQ

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = AppScreenQ()
    view.show()

    sys.exit(app.exec_())
