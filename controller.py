from copy import deepcopy
import numpy as np


class Model:

    def __init__(self, squareEdge, pixmapWidth, pixmapHeight):

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
            self.minMax()
            return True
        else:
            # if the selected position is already colored, by clicking on it we can erase the drawn rectangle
            self.removePosition(row, col)
            self.minMax()
            return False

    def appendPosition(self, row, col):
        self.coloredPositions.append((row, col))
        self.coloredPositions = list(set(self.coloredPositions))
        self.colored[row, col] = 1
        self.minMax()

    def removePosition(self, row, col):
        self.coloredPositions.remove((row, col))
        self.colored[row, col] = 0
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
                    tmp.append((itr.multi_index[0] + self.minX - 1, itr.multi_index[1] + self.minY - 1))
            else:
                numNeighs = np.sum(tmp_colored[itr.multi_index[0] - 1: itr.multi_index[0] + 2,
                                               itr.multi_index[1] - 1: itr.multi_index[1] + 2]) - 1
                if numNeighs < 2 or numNeighs > 3:
                    tmp.append((itr.multi_index[0] + self.minX - 1, itr.multi_index[1] + self.minY - 1))
        results = []
        for el in tmp:
            results.append([self.updatePositions(el[0], el[1]), el[0], el[1]])
        return results

    def clearAll(self):

        cp = deepcopy(self.coloredPositions)
        c = deepcopy(self.colored)

        self.coloredPositions = []
        self.colored = np.zeros((self.numRows, self.numCols))

        return cp, c


class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def updatePositions(self, row, col):
        create = self.model.updatePositions(row, col)
        if create:
            self.view.drawRect(row, col)
        else:
            self.view.eraseRect(row, col)

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

    def updateCells(self):
        results = self.model.updateCells()
        for el in results:
            if el[0]:
                self.view.drawRect(el[1], el[2])
            else:
                self.view.eraseRect(el[1], el[2])

    def clearAll(self):
        cp, c = self.model.clearAll()
        self.view.clearAll()
        self.view.coloredPosition = cp
        self.view.colored = c
