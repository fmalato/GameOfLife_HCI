from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPainter, QPen, QBrush, QPalette
from PyQt5.QtWidgets import QLabel, QScrollArea


class CanvasView(QLabel):

    def __init__(self, pixmap, model):
        super().__init__()

        self.model = model
        self.controller = None

        # initial state, inconsistent if there's no controller
        self.numRows = 0
        self.numCols = 0
        self.squareEdge = 0

        # oldPos doesn't require the colored pixels map, since it's just a graphical effect but doesn't affect the
        # next generation at all
        self.oldPos = []
        self.coloredPosition = []
        self.colored = []

        self.history = False

        # some standard attributes initializations
        self.setStyleSheet("background-color: white;")
        self.setPixmap(pixmap)

        # these attributes are useful for drawing on the canvas
        self.pixmapWidth = self.pixmap().width()
        self.pixmapHeight = self.pixmap().height()

        # also, in order to paint, first you need a painter. It has two brushes to paint two different types of
        # squares (new and old)
        self.painter = QPainter(self.pixmap())
        self.painter.setPen(QPen(Qt.black))
        self.brush = QBrush(Qt.green)
        self.oldBrush = QBrush(Qt.red)
        self.painter.setBrush(self.brush)

    # when self.history switches from True to False, you need to get the latest oldPos and erase all its squares.
    # Then, since there could be some intersections, you also need to get the latest position and redraw it.
    def setHistory(self):
        self.history = not self.history
        if not self.history:
            self.oldPos = self.controller.getOldPos()
            for el in self.oldPos:
                self.eraseRect(el[0], el[1])
            self.coloredPosition = self.controller.getColoredPositions()
            for el in self.coloredPosition:
                self.drawRect(el[0], el[1], True)

    """
        This has to be called right after the View object is instantiated. It works like a "subscribe()" method:
        a Controller subscribes to its View in order to get the user's inputs. To be a proper "subscribe()"
        method the View should have a list of controllers but, since this app just requires one, I thought it
        wouldn't have been necessary to mess up things.
    """
    def addController(self, controller):
        self.controller = controller

        self.numRows = self.controller.getNumRows()
        self.numCols = self.controller.getNumCols()
        self.squareEdge = self.controller.getSquareEdge()

        self.oldPos = self.controller.getOldPos()
        self.coloredPosition = self.controller.getColoredPositions()
        self.colored = self.controller.getColored()

    def mousePressEvent(self, ev: QMouseEvent):
        # updatePosition() is one of the major function of the model class. It is used to update the grid state,
        # then it notifies the changes to the view which draws the rectangle.
        if self.controller is not None:
            self.controller.updatePositions(int(ev.pos().y() / self.squareEdge), int(ev.pos().x() / self.squareEdge))

        # to make the colored square appear, we need to update the window
        self.window().update()

    def drawGrid(self):
        # if I know the grid square's edge length and the desired number of rows and columns, it is easy to
        # draw a grid just by drawing lines between the right couple of points
        x = 0
        y = 0
        for i in range(self.numRows + 1):
            self.painter.drawLine(0, y, self.squareEdge * self.numCols, y)
            y += self.squareEdge
        for j in range(self.numCols + 1):
            self.painter.drawLine(x, 0, x, self.squareEdge * self.numRows)
            x += self.squareEdge

    def drawRect(self, row, col, isNew):
        if isNew:
            self.painter.setBrush(self.brush)
        else:
            self.painter.setBrush(self.oldBrush)
        self.painter.drawRect(col * self.squareEdge, row * self.squareEdge, self.squareEdge, self.squareEdge)
        self.window().update()

    def eraseRect(self, row, col):
        self.painter.eraseRect(col * self.squareEdge + 1, row * self.squareEdge + 1, self.squareEdge - 1,
                               self.squareEdge - 1)
        self.window().update()

    def clearAll(self):
        for op in self.oldPos:
            self.eraseRect(op[0], op[1])
        for p in self.coloredPosition:
            self.eraseRect(p[0], p[1])

        self.window().update()







