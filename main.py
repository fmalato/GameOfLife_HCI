import sys

from app import GameOfLife
from window import MainWindow


if __name__ == '__main__':

    app = GameOfLife(sys.argv)

    window = MainWindow(10, 60, 80)
    window.show()
    app.exec_()
