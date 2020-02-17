import numpy as np

from copy import deepcopy

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QLabel


class CanvasModel:

    def __init__(self, squareEdge, pixmapWidth, pixmapHeight):
        # view initializiation
        self.subscribed = []

        # state initialization
        self.squareEdge = squareEdge
        self.pixmapWidth = pixmapWidth
        self.pixmapHeight = pixmapHeight
        self.numRows = int(self.pixmapHeight / self.squareEdge)
        self.numCols = int(self.pixmapWidth / self.squareEdge)
        self.coloredPositions = []
        self.colored = np.zeros((self.numRows, self.numCols))

        # no need to pass the following attributes
        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0
        self.coloredClearState = np.zeros((self.numRows, self.numCols))

    def subscribe(self, s):
        self.subscribed.append(s)

    def notifyDraw(self, create, row, col):
        for s in self.subscribed:
            s.notifyDraw(create, row, col)

    def notifyState(self):
        for s in self.subscribed:
            s.notifyState()

    def minMax(self):
        if self.coloredPositions.__len__() != 0:
            self.minX = min([x[0] for x in self.coloredPositions])
            self.minY = min([x[1] for x in self.coloredPositions])
            self.maxX = max([x[0] for x in self.coloredPositions])
            self.maxY = max([x[1] for x in self.coloredPositions])
        else:
            self.minX = 0
            self.minY = 0
            self.maxX = 0
            self.maxY = 0

    def updatePositions(self, row, col):

        if (row, col) not in self.coloredPositions:
            # now the painter actually draws the rectangle in the desired position
            self.appendPosition(row, col)
            self.notifyDraw(True, row, col)
        else:
            # if the selected position is already colored, by clicking on it we can erase the drawn rectangle
            self.removePosition(row, col)
            self.notifyDraw(False, row, col)

        self.minMax()

    def appendPosition(self, row, col):
        self.coloredPositions.append((row, col))
        self.coloredPositions = list(set(self.coloredPositions))
        self.colored[row][col] = 1
        self.notifyState()
        self.minMax()

    def removePosition(self, row, col):
        self.coloredPositions.remove((row, col))
        self.colored[row][col] = 0
        self.notifyState()
        self.minMax()

    def updateCells(self):
        tmp = []
        tmp_colored = deepcopy(self.colored[self.minX - 1: self.maxX + 2, self.minY - 1: self.maxY + 2])
        # TODO: fix zero valued not enabled error
        itr = np.nditer(tmp_colored, flags=['multi_index'])
        for x in itr:
            if x == 0:
                if itr.multi_index[0] == 0 and itr.multi_index[1] == 0:
                    numNeighs = np.sum(tmp_colored[itr.multi_index[0] : itr.multi_index[0] + 2,
                                                   itr.multi_index[1] : itr.multi_index[1] + 2])
                elif itr.multi_index[0] == 0:
                    numNeighs = np.sum(tmp_colored[itr.multi_index[0] : itr.multi_index[0] + 2,
                                                   itr.multi_index[1] - 1 : itr.multi_index[1] + 2])
                elif itr.multi_index[1] == 0:
                    numNeighs = np.sum(tmp_colored[itr.multi_index[0] - 1 : itr.multi_index[0] + 2,
                                                   itr.multi_index[1] : itr.multi_index[1] + 2])
                else:
                    numNeighs = np.sum(tmp_colored[itr.multi_index[0] - 1 : itr.multi_index[0] + 2,
                                                   itr.multi_index[1] - 1 : itr.multi_index[1] + 2])
                if numNeighs == 3:
                    newPos = (itr.multi_index[0] + self.minX - 1, itr.multi_index[1] + self.minY - 1)
                    tmp.append(newPos)
            else:
                numNeighs = np.sum(tmp_colored[itr.multi_index[0] - 1: itr.multi_index[0] + 2,
                                               itr.multi_index[1] - 1: itr.multi_index[1] + 2]) - 1
                if numNeighs < 2 or numNeighs > 3:
                    newPos = (itr.multi_index[0] + self.minX - 1, itr.multi_index[1] + self.minY - 1)
                    tmp.append(newPos)
        for el in tmp:
            self.updatePositions(el[0], el[1])

    def clearAll(self):
        for p in self.coloredPositions:
            for s in self.subscribed:
                s.notifyDraw(False, p[0], p[1])

        self.coloredPositions = []
        self.colored = deepcopy(self.coloredClearState)
        for s in self.subscribed:
            s.notifyState()


class CanvasView(QLabel):

    def __init__(self, pixmap, controller):
        super().__init__()

        self.controller = controller

        # initial state
        self.numRows = self.controller.getNumRows()
        self.numCols = self.controller.getNumCols()
        self.squareEdge = self.controller.getSquareEdge()

        self.coloredPosition = self.controller.getColoredPositions()
        self.colored = self.controller.getColored()

        # some standard attributes initializations
        self.setStyleSheet("background-color: white;")
        self.setPixmap(pixmap)

        # these attributes are useful for drawing on the canvas
        self.pixmapWidth = self.pixmap().width()
        self.pixmapHeight = self.pixmap().height()

        # also, in order to paint, first you need a painter
        self.painter = QPainter(self.pixmap())
        self.painter.setPen(QPen(Qt.black))
        self.painter.setBrush(QBrush(Qt.green))

    def mousePressEvent(self, ev: QMouseEvent):
        # by getting the attributes and knowing the length of the edge of a grid square, it is possible to
        # compute the row and the column of the selected square with a simple division
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

    def drawRect(self, row, col):
        self.painter.drawRect(col * self.squareEdge, row * self.squareEdge, self.squareEdge, self.squareEdge)
        self.window().update()

    def eraseRect(self, row, col):
        self.painter.eraseRect(col * self.squareEdge + 1, row * self.squareEdge + 1, self.squareEdge - 1,
                               self.squareEdge - 1)
        self.window().update()

    def clearAll(self):
        for p in self.coloredPosition:
            self.eraseRect(p[0], p[1])

        self.window().update()

    def notifyDraw(self, create, row, col):
        if create:
            self.drawRect(row, col)
        else:
            self.eraseRect(row, col)

    def notifyState(self):
        self.coloredPosition = self.controller.getColoredPositions()
        self.colored = self.controller.getColored()


class CanvasController:

    def __init__(self, model):
        self.model = model

    def updatePositions(self, row, col):
        self.model.updatePositions(row, col)

    def getSquareEdge(self):
        return self.model.squareEdge

    def getNumRows(self):
        return self.model.numRows

    def getNumCols(self):
        return self.model.numCols

    def getColoredPositions(self):
        return deepcopy(self.model.coloredPositions)

    def getColored(self):
        return deepcopy(self.model.colored)

    def appendPosition(self, row, col):
        self.model.appendPosition(row, col)

    def removePosition(self, row, col):
        self.model.removePosition(row, col)

    def updateCells(self):
        self.model.updateCells()

    def clearAll(self):
        self.model.clearAll()
