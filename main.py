import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtGui import QPainter, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt

if __name__ == '__main__':

    app = QApplication(sys.argv)

    squareEdge = 15
    numCols = 30
    numRows = 20

    widg = QLabel()
    widg.setFixedSize(numCols * squareEdge + 1, numRows * squareEdge + 1)
    window = QMainWindow()
    widget = QWidget()

    window.setCentralWidget(widget)
    layout = QVBoxLayout()
    sliderLayout = QHBoxLayout()
    canvasLayout = QHBoxLayout()
    buttonLayout = QVBoxLayout()
    canvasLayout.addWidget(widg)
    sliderLayout.addWidget(QLabel('FPS'))
    sliderLayout.addWidget(QSlider(Qt.Horizontal))
    layout.addLayout(sliderLayout)
    layout.addLayout(canvasLayout)
    labels = ['Start', 'Stop', 'Pause', 'Clear']
    buttons = [QPushButton(label) for label in labels]
    for b in buttons:
        buttonLayout.addWidget(b)
    canvasLayout.addLayout(buttonLayout)
    window.setWindowTitle("Conway's Game of Life")
    pixmap = QPixmap(squareEdge * numCols + 1, squareEdge * numRows + 1)
    pixmap.fill(Qt.white)
    widg.setPixmap(pixmap)
    widg.setStyleSheet('background-color: white;')
    painter = QPainter(widg.pixmap())
    painter.setPen(QPen(Qt.black))
    painter.setBrush(QBrush(Qt.black))
    x = 0
    y = 0
    for i in range(numRows + 1):
        painter.drawLine(0, y, squareEdge * numCols, y)
        y += squareEdge
    for j in range(numCols + 1):
        painter.drawLine(x, 0, x, squareEdge * numRows)
        x += squareEdge
    widget.setLayout(layout)

    window.show()
    app.exec_()
