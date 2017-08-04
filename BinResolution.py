from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import bin_resolution_tamplate

import numpy as np


class BinResolution(QDialog, bin_resolution_tamplate.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.width = 512
        self.height = 512
        self.offset = 10
        self.dtype = np.int32

        self.lineEdit_width.setText(str(self.width))
        self.lineEdit_height.setText(str(self.height))
        self.lineEdit_offset.setText(str(self.offset))

        self.buttonBox_set_resolution.accepted.connect(self.set_resolution)

        self.comboBox_type.activated[str].connect(self.change_type)

        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def set_resolution(self):
        self.width = int(self.lineEdit_width.text())
        self.height = int(self.lineEdit_height.text())
        self.offset = int(self.lineEdit_offset.text())

    def change_type(self, text):
        if text == 'int32':
            self.type = np.int32
        elif text == 'float32':
            self.type = np.float32
