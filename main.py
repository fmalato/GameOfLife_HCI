import sys

from app import GameOfLife
from window import MainWindow


if __name__ == '__main__':

    app = GameOfLife(sys.argv)

    window = MainWindow(10, 40, 50)
    window.show()
    app.exec_()
