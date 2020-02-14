from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QMouseEvent


class ClearButton(QPushButton):

    def __init__(self, label, canvas):
        super().__init__(label)
        self.canvas = canvas

    def mousePressEvent(self, e: QMouseEvent):
        self.canvas.clearAll()
        self.window().update()