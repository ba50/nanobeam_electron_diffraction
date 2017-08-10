from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import virtual_image_resolution_template


class VirtualImageResolution(QDialog, virtual_image_resolution_template.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.shape = 20, 20
        self.threads = 1

        self.lineEdit_width.setText(str(self.shape[0]))
        self.lineEdit_height.setText(str(self.shape[1]))
        self.lineEdit_threads.setText(str(self.threads))

        self.buttonBox_set_resolution.accepted.connect(self.set_resolution)

        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def set_resolution(self):
        self.shape = int(self.lineEdit_width.text()), int(self.lineEdit_height.text())
        self.threads = int(self.lineEdit_threads.text())
