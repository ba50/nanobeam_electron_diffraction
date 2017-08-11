from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import bin_resolution_template

import numpy as np


class BinResolution(QDialog, bin_resolution_template.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.shape = 1, 512, 512
        self.offset = 0
        self.dtype = np.int16

        self.lineEdit_z.setText(str(self.shape[0]))
        self.lineEdit_width.setText(str(self.shape[1]))
        self.lineEdit_height.setText(str(self.shape[2]))
        self.lineEdit_offset.setText(str(self.offset))

        self.buttonBox_set_resolution.accepted.connect(self.set_resolution)

        self.comboBox_type.activated[str].connect(self.change_type)

        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def set_resolution(self):
        self.shape = int(self.lineEdit_z.text()), int(self.lineEdit_width.text()), int(self.lineEdit_height.text())
        self.offset = int(self.lineEdit_offset.text())

    def change_type(self, text):
        if text == 'int16':
            self.dtype = np.int16
        if text == 'int32':
            self.dtype = np.int32
        elif text == 'float32':
            self.dtype = np.float32
