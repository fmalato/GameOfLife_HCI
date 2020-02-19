import json
import numpy as np

from copy import deepcopy
from abc import ABCMeta, abstractmethod

from PyQt5.QtWidgets import QMessageBox

"""
    The Model of the MVC implementation is used to retain the useful data (it should be linked to a DB or something
    like that, but since there are a few data I didn't want to overkill it) and to dispatch them to the various 
    views via the Controller. Also, I've decided to send the updated data as return value of the model methods (where
    possible), since it is faster than using specific function calls like getters and setters and this way you still
    don't access directly the stored data, therefore not violating the MVC principle.
"""


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
        self.jsonData = []
        self.patternsNames = []

        # no need to pass the following attributes
        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0

    """ 
        This method provides a way to compute the smallest grid that contains dots of interest: since a dead cell
        can become alive iff there are alive cells in its neighborhood, there's no point in computing values for
        dead cells that are not close to living cells. Hence, by updating the (x, y) positions of both the 
        closest and the farthest cell wrt to the top-left corner, you can find a sub grid with all the interesting 
        cells and also save quite a lot of computations (even if it's not the minimum number).
    """

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
        results = []

        # necessary to avoid a numpy bug
        if len(tmp_colored) != 0:
            itr = np.nditer(tmp_colored, flags=['multi_index'])
        else:
            return results
        for x in itr:
            indexX = itr.multi_index[0]
            indexY = itr.multi_index[1]
            if x == 0:
                # handling the corner cases
                if indexX == 0 and indexY == 0:
                    numNeighs = np.sum(tmp_colored[indexX: indexX + 2, indexY: indexY + 2])
                elif indexX == 0:
                    numNeighs = np.sum(tmp_colored[indexX: indexX + 2, indexY - 1: indexY + 2])
                elif indexY == 0:
                    numNeighs = np.sum(tmp_colored[indexX - 1: indexX + 2, indexY: indexY + 2])
                else:
                    numNeighs = np.sum(tmp_colored[indexX - 1: indexX + 2, indexY - 1: indexY + 2])
                # applying the game rules
                if numNeighs == 3:
                    tmp.append((indexX + self.minX - 1, indexY + self.minY - 1))
            # if the current element of the grid is a 1, it can't be a corner square, so there's no need to handle
            # the cases
            else:
                numNeighs = np.sum(tmp_colored[indexX - 1: indexX + 2, indexY - 1: indexY + 2]) - 1
                if numNeighs < 2 or numNeighs > 3:
                    tmp.append((indexX + self.minX - 1, indexY + self.minY - 1))
        for el in tmp:
            results.append([self.updatePositions(el[0], el[1]), el[0], el[1]])
        return results

    def clearAll(self):

        cp = deepcopy(self.coloredPositions)
        c = deepcopy(self.colored)

        self.coloredPositions = []
        self.colored = np.zeros((self.numRows, self.numCols))

        return cp, c

    def loadPattern(self, index):
        pattern = self.jsonData[self.patternsNames[index]]["pattern"]
        posX = self.jsonData[self.patternsNames[index]]["position"][0]
        posY = self.jsonData[self.patternsNames[index]]["position"][1]
        shapeX = self.jsonData[self.patternsNames[index]]["shape"][0]
        shapeY = self.jsonData[self.patternsNames[index]]["shape"][1]
        self.clearAll()
        if self.numCols >= shapeX + posX and self.numCols >= shapeY + posY:
            for r in range(pattern.__len__()):
                for c in range(pattern[r].__len__()):
                    if pattern[r][c] == 1:
                        self.appendPosition(r + posX, c + posY)
        else:
            self.showErrorPopup()

        return deepcopy(self.coloredPositions)

    def loadPatternNames(self):
        with open('patterns.json', 'r') as f:
            self.jsonData = json.load(f)
            self.patternsNames = list(self.jsonData.keys())
            return deepcopy(self.patternsNames)

    def showErrorPopup(self):
        msg = QMessageBox()
        msg.setWindowTitle('Error')
        msg.setText('Cannot draw pattern: the grid is too small.')
        msg.exec_()


"""
    I've been thinking a lot about whether to make a controller for all the MainWindow or just for some of the
    widgets. Finally I've decided that since the MVC is mostly about separating view from data, the exchange of a
    single signal between two components wasn't worth the effort of calling the controller: for example, setting the
    FPS of the FPSSlider is not a vital information for the view nor the model, since it affects only a timer which
    is declared into the StartButton.
    So I've come up to the conclusion that I needed different strategies for different objects:
    - If a widget needs to access important data (such as the Canvas or the KnownPatternBox), they have to be a
      View in the MVC paradigm;
    - Else if a widget has to emit signals to the Model, it must have a controller attribute, so that it could
      propagate its signals correctly (for example, the StartButton doesn't need data but tells the Model to start
      following the game rules);
    - Finally, if a widget doesn't need important data and emits signals to another widget that is not part of the
      MVC, there's no need to bother the Controller at all. This is the case of the StartButton and the FPSSlider
      described above.
"""


class Controller:

    # in the MVC paradigm, a Controller is aware of both the controller and the view.
    def __init__(self, model, canvasView, patternBoxView):
        self.model = model
        self.canvasView = canvasView
        self.patternBoxView = patternBoxView

    def updatePositions(self, row, col):
        create = self.model.updatePositions(row, col)
        if create:
            self.canvasView.drawRect(row, col)
        else:
            self.canvasView.eraseRect(row, col)

    # A bunch of getters I couldn't avoid...
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

    def getPatternsNames(self):
        return self.model.loadPatternNames()

    def updateCells(self):
        results = self.model.updateCells()
        for el in results:
            if el[0]:
                self.canvasView.drawRect(el[1], el[2])
            else:
                self.canvasView.eraseRect(el[1], el[2])

    def clearAll(self):
        cp, c = self.model.clearAll()
        self.canvasView.coloredPosition = cp
        self.canvasView.colored = c
        self.canvasView.clearAll()
        self.canvasView.coloredPosition = self.getColoredPositions()
        self.canvasView.colored = self.getColored()

    def loadPattern(self, index):
        self.clearAll()
        positions = self.model.loadPattern(index)
        for p in positions:
            self.canvasView.drawRect(p[0], p[1])
