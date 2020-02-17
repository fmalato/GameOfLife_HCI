from PyQt5.QtWidgets import QLabel, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from canvas import CanvasModel, CanvasView, CanvasController
from buttons import StartButton, StepButton, StopButton, ClearButton, KnownPatternsBox
from slider import FPSSlider


class MainWindow(QMainWindow):

    def __init__(self, squareEdge, numRows, numCols):
        super().__init__()

        # window
        self.squareEdge = squareEdge
        self.numRows = numRows
        self.numCols = numCols

        # background widget
        widget = QWidget()
        self.setCentralWidget(widget)
        self.setWindowTitle("Conway's Game of Life")

        # canvas
        pixmap = QPixmap(self.squareEdge * self.numCols + 1, self.squareEdge * self.numRows + 1)
        pixmap.fill(Qt.white)
        canvasModel = CanvasModel(self.squareEdge, pixmap.width(), pixmap.height())
        canvasController = CanvasController(canvasModel)
        canvas = CanvasView(pixmap, canvasController)
        canvasModel.subscribe(canvas)
        canvas.setFixedSize(self.numCols * self.squareEdge + 1, self.numRows * self.squareEdge + 1)

        # buttons initialization and layout definition (as a list of widgets)
        buttons = []
        start = StartButton(canvasController)
        buttons.append(start)
        buttons.append(StopButton(start.timer))
        buttons.append(StepButton(canvasController))
        buttons.append(ClearButton(canvasController))
        buttons.append(KnownPatternsBox(canvasController))
        buttonLayout = QVBoxLayout()
        for b in buttons:
            b.setFixedSize(100, 50)
            buttonLayout.addWidget(b)

        """Layout has been defined as multiple layouts containing each other, in order to avoid chaotic situations.
           We could summarize like this: a container contains other container, each of which contains a specific object.
           This way, I was able to handle the overall layout just like a divs cascade."""

        # two simple boxes: a label and an horizontal slider, aligned horizontally
        sliderLayout = QHBoxLayout()
        fpsLabel = QLabel('FPS:')
        fpsLabel.setFixedWidth(30)
        minLabel = QLabel('1')
        minLabel.setFixedWidth(10)
        sliderLayout.addWidget(fpsLabel)
        sliderLayout.addWidget(minLabel)
        sliderLayout.addWidget(FPSSlider(start))
        sliderLayout.addWidget(QLabel('20'))

        # canvas is defined as an horizontal layout formed by two containers, containing the Canvas object and a
        # bunch of buttons respectively
        canvasLayout = QHBoxLayout()
        canvasLayout.addWidget(canvas)
        canvasLayout.addLayout(buttonLayout)

        # this is the highest-level layout, that contains both the canvas and the slider in a vertical fashion
        layout = QVBoxLayout()
        layout.addLayout(sliderLayout)
        layout.addLayout(canvasLayout)
        widget.setLayout(layout)

        # finally, the canvas can draw the grid
        canvas.drawGrid()
