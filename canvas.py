from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPainter, QPen, QBrush, QPalette
from PyQt5.QtWidgets import QLabel, QScrollArea


class CanvasView(QLabel):

    def __init__(self, pixmap, model):
        super().__init__()

        self.model = model
        self.controller = None

        self.history = False

        # some standard attributes initializations
        self.setStyleSheet("background-color: white;")
        self.setPixmap(pixmap)

        # these attributes are useful for drawing on the canvas
        self.pixmapWidth = self.model.pixmapWidth
        self.pixmapHeight = self.model.pixmapHeight

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
            for el in self.model.oldPos:
                self.eraseRect(el[0], el[1])
            for el in self.model.coloredPositions:
                self.drawRect(el[0], el[1], True)

    """
        This has to be called right after the View object is instantiated. It works like a "subscribe()" method:
        a Controller subscribes to its View in order to get the user's inputs. To be a proper "subscribe()"
        method the View should have a list of controllers but, since this app just requires one, I thought it
        wouldn't have been necessary to mess up things.
    """
    def addController(self, controller):
        self.controller = controller

    def mousePressEvent(self, ev: QMouseEvent):
        # updatePosition() is one of the major function of the model class. It is used to update the grid state,
        # then it notifies the changes to the view which draws the rectangle.
        if self.controller is not None:
            self.controller.updatePositions(int(ev.pos().y() / self.model.squareEdge),
                                            int(ev.pos().x() / self.model.squareEdge))

        # to make the colored square appear, we need to update the window
        self.window().update()

    def drawGrid(self):
        # if I know the grid square's edge length and the desired number of rows and columns, it is easy to
        # draw a grid just by drawing lines between the right couple of points
        x = 0
        y = 0
        for i in range(self.model.numRows + 1):
            self.painter.drawLine(0, y, self.model.squareEdge * self.model.numCols, y)
            y += self.model.squareEdge
        for j in range(self.model.numCols + 1):
            self.painter.drawLine(x, 0, x, self.model.squareEdge * self.model.numRows)
            x += self.model.squareEdge

    def drawRect(self, row, col, isNew):
        if isNew:
            self.painter.setBrush(self.brush)
        else:
            self.painter.setBrush(self.oldBrush)
        self.painter.drawRect(col * self.model.squareEdge, row * self.model.squareEdge, self.model.squareEdge,
                              self.model.squareEdge)
        self.window().update()

    def eraseRect(self, row, col):
        self.painter.eraseRect(col * self.model.squareEdge + 1, row * self.model.squareEdge + 1,
                               self.model.squareEdge - 1, self.model.squareEdge - 1)
        self.window().update()

    def clearAll(self):
        for op in self.model.oldPos:
            self.eraseRect(op[0], op[1])
        for p in self.model.coloredPositions:
            self.eraseRect(p[0], p[1])

        self.window().update()







