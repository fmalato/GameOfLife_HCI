import sys

from PyQt5.QtWidgets import QApplication

from window import MainWindow


if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow(10, 40, 50)
    window.show()
    app.exec_()
