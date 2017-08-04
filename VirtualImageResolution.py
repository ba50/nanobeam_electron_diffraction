from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import virtual_image_resolution_template


class VirtualImageResolution(QDialog, virtual_image_resolution_template.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.width = 20
        self.height = 20

        self.lineEdit_width.setText(str(self.width))
        self.lineEdit_height.setText(str(self.height))

        self.buttonBox_set_resolution.accepted.connect(self.set_resolution)

        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def set_resolution(self):
        self.width = int(self.lineEdit_width.text())
        self.height = int(self.lineEdit_height.text())
