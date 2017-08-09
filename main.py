import sys

from PyQt5 import QtWidgets
from Gui import Gui
from Core import Core


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    core = Core()
    form = Gui(core)
    form.show()
    app.exec_()
