from PyQt5.QtWidgets import QApplication


class GameOfLife(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

    def exec_(self):
        super().exec_()