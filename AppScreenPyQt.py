from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QProgressBar, QPushButton, \
    QSizePolicy, QButtonGroup, QHBoxLayout, QLabel, QWidget, QMainWindow, QAction, QMessageBox, QDialog, \
    QDialogButtonBox

from AppModel import AppModel
from Commons import *


class AppScreenQ(QMainWindow):
    def __init__(self):
        super(AppScreenQ, self).__init__()
        self.setWindowTitle("Mistrz szachownicy QT")

        self.timeCounter = TIME_LIMIT
        self.gameFlag = False
        self.bar = None
        self.engine = AppModel()

        self.mainLayout = QVBoxLayout()
        self.setMinimumSize(800, 800)
        self._menuSetUp()
        self._boardSetUp()
        self._progressSetUp()
        self._controlSetUp()
        self._statsSetUp()

        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)
        self.show()

    def _menuSetUp(self):
        fileMenu = self.menuBar().addMenu("&Menu")
        newAct = QAction('Opis', self)
        newAct.triggered.connect(self._overviewDisplay)
        fileMenu.addAction(newAct)

    def _overviewDisplay(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Opis gry!")
        overviewLayout = QHBoxLayout()
        overview = QLabel(OVERVIEW_TEXT)
        overview.setWordWrap(True)
        overviewLayout.addWidget(overview)
        dlg.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        dlg.setLayout(overviewLayout)
        dlg.show()

    def _statsSetUp(self):
        style = """ 
        border: 2px solid gray;
        border-radius: 10px;
        padding: 8px;
        selection-background-color: darkgray;"""
        self.stats = QHBoxLayout()

        self.scoreStatic = QLabel("Aktualny wynik:")
        self.scoreStatic.setMinimumHeight(40)
        self.scoreStatic.setMaximumHeight(40)
        self.scoreStatic.setStyleSheet(style)
        self.scoreStatic.setAlignment(QtCore.Qt.AlignCenter)

        self.score = QLabel("0")
        self.score.setMinimumHeight(40)
        self.score.setMaximumHeight(40)
        self.score.setStyleSheet(style)
        self.score.setAlignment(QtCore.Qt.AlignCenter)

        self.coordStatic = QLabel("Znajdź:")
        self.coordStatic.setMinimumHeight(40)
        self.coordStatic.setMaximumHeight(40)
        self.coordStatic.setStyleSheet(style)
        self.coordStatic.setAlignment(QtCore.Qt.AlignCenter)

        self.coord = QLabel("")
        self.coord.setMinimumHeight(40)
        self.coord.setMaximumHeight(40)
        self.coord.setStyleSheet(style)
        self.coord.setAlignment(QtCore.Qt.AlignCenter)

        self.stats.addWidget(self.scoreStatic)
        self.stats.addWidget(self.score)
        self.stats.addWidget(self.coordStatic)
        self.stats.addWidget(self.coord)
        self.mainLayout.addLayout(self.stats)

    def _controlSetUp(self):
        style = """ 
        border-style: solid;
        border-color: gray;
        border-width: 2px;
        border-radius: 10px;"""

        self.menu = QHBoxLayout()

        self.startButton = QPushButton('Start', self)
        self.startButton.setStyleSheet(style)
        self.startButton.setMinimumHeight(40)
        self.startButton.clicked.connect(self._onButtonStart)

        self.stopButton = QPushButton('Stop', self)
        self.stopButton.setStyleSheet(style)
        self.stopButton.setMinimumHeight(40)
        self.stopButton.clicked.connect(self._onButtonStop)
        self.stopButton.setEnabled(False)

        self.menu.addWidget(self.startButton)
        self.menu.addWidget(self.stopButton)

        self.mainLayout.addLayout(self.menu)

    def _progressSetUp(self):
        self.progress = QProgressBar(self)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("border: 2px solid grey;"
                                    "border-radius: 5px;"
                                    "text-align: center;"
                                    )
        self.mainLayout.addWidget(self.progress)
        self.progress.setMaximum(TIME_LIMIT)

    def _boardSetUp(self):
        frameWidget = QWidget()
        frameLayout = QHBoxLayout()
        frameLayout.addStretch()
        frameWidget.setFixedSize(560, 560)
        frameLayout.addWidget(frameWidget)
        frameLayout.addStretch()
        self.mainLayout.addLayout(frameLayout)
        squareLayout = QGridLayout(frameWidget)
        squareLayout.setSpacing(0)
        self.squares = QButtonGroup()
        for i in range(8 * 8):
            newButton = QPushButton()
            policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            newButton.setSizePolicy(policy)
            x = getX(i)
            y = getY(i)
            if (x + y) % 2 == 0:
                newButton.setStyleSheet("background-color: linen")
            else:
                newButton.setStyleSheet("background-color: sienna")
            self.squares.addButton(newButton, i)
            squareLayout.addWidget(newButton, x, y)
        self.squares.setExclusive(True)
        self.squares.buttonPressed.connect(self._onSquareClick)
        self.squares.buttonReleased.connect(self._onSquareRelease)
        self.mainLayout.addLayout(squareLayout)

    def _onButtonStart(self):
        if self.gameFlag:
            return
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.gameFlag = True

        self.timeCounter = TIME_LIMIT
        self.bar = QTimer()
        self.bar.timeout.connect(self._onClockChanged)
        self.bar.start(TIME_INTERVAL)

        self.engine.counterReset()
        self.engine.getNextPosition()
        self.coord.setText(self.engine.getCurrentNotation())
        self.score.setText("0")

    def _onButtonStop(self):
        if not self.gameFlag:
            return
        self.bar.stop()
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.gameFlag = False

    def _onClockChanged(self):
        if (self.timeCounter == 0) or (self.gameFlag is False):
            self.startButton.setEnabled(True)
            self.stopButton.setEnabled(False)
            self.gameFlag = False
        self.timeCounter -= 1
        self.progress.setValue(self.timeCounter)

    def _onSquareClick(self, btn):
        if not self.gameFlag:
            return
        i = self.squares.id(btn)
        x = getX(i)
        y = getY(i)

        if self.engine.getCurrentPosition() == (x, y):
            btn.setStyleSheet("background-color: green")
            self.engine.counterAdd()
            self.engine.getNextPosition()
            self.coord.setText(self.engine.getCurrentNotation())
            self.score.setText(str(self.engine.getCounter()))
            return
        btn.setStyleSheet("background-color: red")

    def _onSquareRelease(self, btn):
        i = self.squares.id(btn)
        x = getX(i)
        y = getY(i)
        if (x + y) % 2 == 0:
            btn.setStyleSheet("background-color: linen")
        else:
            btn.setStyleSheet("background-color: sienna")
