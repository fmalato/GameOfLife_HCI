from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent


class FPSSlider(QSlider):

    def __init__(self, startButton):
        super().__init__(Qt.Horizontal)
        self.setMinimum(1)
        self.setMaximum(30)
        self.setFixedWidth(400)
        self.startButton = startButton

    def mouseReleaseEvent(self, ev: QMouseEvent):
        self.valueChanged(self.value())
        super().mouseReleaseEvent(ev)

    def valueChanged(self, value: int):
        self.startButton.setFps(value)
