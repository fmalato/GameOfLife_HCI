import json

from PyQt5.QtCore import QTimer, QObject
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QPushButton, QComboBox


class StartButton(QPushButton):

    def __init__(self, canvas):
        super().__init__('Start')
        self.timer = QTimer()
        self.canvas = canvas
        self.timer.timeout.connect(self.canvas.updateCells)
        self.fps = 1

    def mousePressEvent(self, e: QMouseEvent):
        self.timer.start(1000 * (1 / self.fps))
        super().mousePressEvent(e)

    def setFps(self, value):
        self.fps = value


class StepButton(QPushButton, QObject):

    def __init__(self, canvasController):
        super().__init__('Step')
        self.canvasController = canvasController
        self.clicked.connect(self.canvasController.updateCells)

    def mousePressEvent(self, e: QMouseEvent):
        super().mousePressEvent(e)


class StopButton(QPushButton, QObject):

    def __init__(self, timer):
        super().__init__('Stop')
        self.timer = timer

    def mousePressEvent(self, e: QMouseEvent):
        self.timer.stop()
        super().mousePressEvent(e)


class ClearButton(QPushButton, QObject):

    def __init__(self, canvasController):
        super().__init__('Clear')
        self.canvasController = canvasController

    def mousePressEvent(self, e: QMouseEvent):
        self.clicked.connect(self.canvasController.clearAll)
        super().mousePressEvent(e)

class KnownPatternsBox(QComboBox, QObject):

    def __init__(self, canvasController):
        super().__init__()
        self.patterns = []
        # EXTRA TASK: LOADING OF INITIAL STATE
        with open('patterns.json', 'r') as f:
            self.jsonData = json.load(f)
            self.patternsNames = list(self.jsonData.keys())
        for el in self.patternsNames:
            self.addItem(el)
        self.canvasController = canvasController
        self.activated.connect(self.drawPattern)

    def drawPattern(self):
        index = self.currentIndex()
        self.patterns = self.jsonData[self.patternsNames[index]]["pattern"]
        posX = self.jsonData[self.patternsNames[index]]["position"][0]
        posY = self.jsonData[self.patternsNames[index]]["position"][1]
        shapeX = self.jsonData[self.patternsNames[index]]["shape"][0]
        shapeY = self.jsonData[self.patternsNames[index]]["shape"][1]
        self.canvasController.clearAll()
        if self.canvasController.getNumCols() >= shapeX + posX and self.canvasController.getNumRows() >= shapeY + posY:
            for r in range(self.patterns.__len__()):
                for c in range(self.patterns[r].__len__()):
                    if self.patterns[r][c] == 1:
                        self.canvasController.updatePositions(r + posX, c + posY)
        else:
            print('Cannot draw pattern: the grid is too small.')



