from threading import Thread
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import virtual_image_plot_template

import pyqtgraph as pg

from VirtualImageResolution import VirtualImageResolution


class VirtualImagePlot(QDialog, virtual_image_plot_template.Ui_Dialog_virtual_image_plot):
    def __init__(self, curr_series, image_view):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.image_view = image_view
        self.image_view_ = pg.ImageView()
        self.image_layout.addWidget(self.image_view_)
        self.pushButton_update_plot.clicked.connect(self.start_update_plot)

        self.vi_resolution = VirtualImageResolution()
        self.do_update = False

        self.curr_series = curr_series
        self.virtual_image = np.zeros(self.vi_resolution.shape)

        self.thread_pool = None

        self.setWindowModality(Qt.WindowModal)
        self.exec_()

    def start_update_plot(self):
        self.thread_pool = [Thread(target=self.update_plot) for i in range(self.vi_resolution.threads)]
        for thread in self.thread_pool:
            thread.daemon = True
            thread.start()

        self.do_update = True

    def update_plot(self):
        while self.do_update:
            for i in range(self.virtual_image.shape[0]):
                for j in range(self.virtual_image.shape[1]):
                    self.virtual_image[i, j] =\
                        np.mean(self.image_view.roi.getArrayRegion(self.curr_series.array[j*self.virtual_image.shape[0]+i, :, :], self.image_view.getImageItem()))
            self.image_view_.setImage(self.virtual_image)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.do_update = False
