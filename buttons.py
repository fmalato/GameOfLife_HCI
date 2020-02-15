from PyQt5.QtCore import QTimer, QObject
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QPushButton


class StartButton(QPushButton):

    def __init__(self, canvas):
        super().__init__('Start')
        self.timer = QTimer()
        self.canvas = canvas
        self.timer.timeout.connect(self.canvas.updateCells)

    def mousePressEvent(self, e: QMouseEvent):
        self.timer.start(500)
        super().mousePressEvent(e)


class StepButton(QPushButton, QObject):

    def __init__(self, canvas):
        super().__init__('Step')
        self.canvas = canvas

    def mousePressEvent(self, e: QMouseEvent):
        self.clicked.connect(self.canvas.updateCells)
        super().mousePressEvent(e)


class StopButton(QPushButton, QObject):

    def __init__(self, timer):
        super().__init__('Stop')
        self.timer = timer

    def mousePressEvent(self, e: QMouseEvent):
        self.timer.stop()
        super().mousePressEvent(e)


class ClearButton(QPushButton, QObject):

    def __init__(self, canvas):
        super().__init__('Clear')
        self.canvas = canvas

    def mousePressEvent(self, e: QMouseEvent):
        self.clicked.connect(self.canvas.clearAll)
        super().mousePressEvent(e)