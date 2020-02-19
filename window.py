from PyQt5.QtWidgets import QLabel, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from canvas import CanvasView
from MVC import Controller, Model
from buttons import KnownPatternsBox

from utils import createButtonsForGUI, generateLabelsForGUI


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

        # since the Canvas object is the core of the GUI, its definition is a bit messy
        pixmap = QPixmap(self.squareEdge * self.numCols + 1, self.squareEdge * self.numRows + 1)
        pixmap.fill(Qt.white)
        # model of the MVC
        model = Model(self.squareEdge, pixmap.width(), pixmap.height())
        # views of the MVC, getting the model as argument
        canvas = CanvasView(pixmap, model)
        knownPatternBox = KnownPatternsBox(model)
        # controller of the MVC
        controller = Controller(model, canvas, knownPatternBox)
        canvas.addController(controller)
        knownPatternBox.addController(controller)
        # an useful canvas property
        canvas.setFixedSize(self.numCols * self.squareEdge + 1, self.numRows * self.squareEdge + 1)

        # buttons initialization and layout definition (as a list of widgets)
        fpsSlider, buttons = createButtonsForGUI(canvas, knownPatternBox, controller)
        buttonLayout = QVBoxLayout()
        for b in buttons:
            b.setFixedSize(100, 50)
            buttonLayout.addWidget(b)

        """
            Layout has been defined as multiple layouts containing each other, in order to avoid chaotic situations.
            We could summarize like this: a container contains other containers, each of which contains a specific 
            object. This way I was able to handle the overall layout just like a divs cascade.
        """

        # two simple boxes: three labels and an FPSSlider, all aligned horizontally
        fpsLabel, minLabel = generateLabelsForGUI()
        # assembling the label layout
        sliderLayout = QHBoxLayout()
        sliderLayout.addWidget(fpsLabel)
        sliderLayout.addWidget(minLabel)
        sliderLayout.addWidget(fpsSlider)
        sliderLayout.addWidget(QLabel('60'))

        # canvasLayout is defined as an horizontal layout formed by two containers, containing the Canvas object on the
        # left and the buttonLayout with all of its buttons on the right.
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
