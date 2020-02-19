from PyQt5.QtCore import QTimer, QObject
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QPushButton, QComboBox, QCheckBox


class StartButton(QPushButton):

    def __init__(self, controller):
        super().__init__('Start')
        self.timer = QTimer()
        self.controller = controller
        self.timer.timeout.connect(self.controller.updateCells)
        self.fps = 1

    def mousePressEvent(self, e: QMouseEvent):
        self.timer.start(1000 * (1 / self.fps))
        super().mousePressEvent(e)

    def setFps(self, value):
        self.fps = value
        if self.timer.isActive():
            self.timer.stop()
            self.timer.start(1000 * (1 / self.fps))


class StepButton(QPushButton, QObject):

    def __init__(self, controller):
        super().__init__('Step')
        self.controller = controller
        self.clicked.connect(self.controller.updateCells)

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

    def __init__(self, controller):
        super().__init__('Clear')
        self.controller = controller
        self.clicked.connect(self.controller.clearAll)


class KnownPatternsBox(QComboBox, QObject):

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.controller = None

        self.activated.connect(self.loadPattern)

    """
        Just like the canvas, drawing a pattern requires to access some data (in this case, from a file). So, it was
        necessary to make the KnownPatternsBox a view of the MVC and, because of that, I provided the same method as
        the Canvas class.
    """
    def addController(self, controller):
        self.controller = controller
        patternsNames = self.controller.getPatternsNames()
        for el in patternsNames:
            self.addItem(el)

    def loadPattern(self):
        if self.controller is not None:
            self.controller.loadPattern(self.currentIndex())


class HistoryCheckBox(QCheckBox):

    def __init__(self, canvas):
        super().__init__('Cells history')
        self.canvas = canvas
        self.stateChanged.connect(self.canvas.setHistory)


