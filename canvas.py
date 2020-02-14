from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QLabel


class Canvas(QLabel):

    def __init__(self, pixmap, squareEdge):
        super().__init__()

        # some standard attributes initializations
        self.setStyleSheet("background-color: white;")
        self.setPixmap(pixmap)

        # these attributes are useful for drawing on the canvas
        self.squareEdge = squareEdge
        self.pixmapWidth = self.pixmap().width()
        self.pixmapHeight = self.pixmap().height()

        # also, in order to paint, first you need a painter
        self.painter = QPainter(self.pixmap())
        self.painter.setPen(QPen(Qt.black))
        self.painter.setBrush(QBrush(Qt.green))

        # an attribute to have memory of all the colored positions
        self.coloredPositions = []
        # 2D Array to determine the next generation
        self.colored = [[0 for x in range((int)(self.pixmapWidth / self.squareEdge))]
                        for y in range((int)(self.pixmapHeight / self.squareEdge))]

    def mousePressEvent(self, ev: QMouseEvent):
        # by getting the attributes and knowing the length of the edge of a grid square, it is possible to
        # compute the row and the column of the selected square with a simple division
        clickPosition = ev.pos()
        clickPosX = clickPosition.x()
        clickPosY = clickPosition.y()
        col = (int)(clickPosX / self.squareEdge)
        row = (int)(clickPosY / self.squareEdge)

        if (row, col) not in self.coloredPositions:
            # now the painter actually draws the rectangle in the desired position
            self.drawRect(row, col)
        else:
            # if the selected position is already colored, by clicking on it we can erase the drawn rectangle
            self.eraseRect(row, col)

        # to make the colored square appear, we need to update the window
        self.window().update()

    def drawGrid(self, numRows, numCols):
        # if I know the grid square's edge length and the desired number of rows and columns, it is easy to
        # draw a grid just by drawing lines between the right couple of points
        x = 0
        y = 0
        for i in range(numRows + 1):
            self.painter.drawLine(0, y, self.squareEdge * numCols, y)
            y += self.squareEdge
        for j in range(numCols + 1):
            self.painter.drawLine(x, 0, x, self.squareEdge * numRows)
            x += self.squareEdge

    def drawRect(self, row, col):
        self.coloredPositions.append((row, col))
        self.colored[row][col] = 1
        self.painter.drawRect(col * self.squareEdge, row * self.squareEdge, self.squareEdge, self.squareEdge)

    def eraseRect(self, row, col):
        self.coloredPositions.remove((row, col))
        self.colored[row][col] = 0
        self.painter.eraseRect(col * self.squareEdge + 1, row * self.squareEdge + 1, self.squareEdge - 1,
                               self.squareEdge - 1)

    def clearAll(self):
        for p in self.coloredPositions:
            self.painter.eraseRect(p[1] * self.squareEdge + 1, p[0] * self.squareEdge + 1, self.squareEdge - 1,
                                   self.squareEdge - 1)
            self.colored[p[0]][p[1]] = 0
        self.coloredPositions = []

