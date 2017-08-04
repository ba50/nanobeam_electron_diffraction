import os.path as path
import numpy as np
import copy
from threading import Thread

import gui_template
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
from scipy import misc

from BinReader import BinReader
from VirtualImageResolution import VirtualImageResolution
from BraggImage import BraggImage
import Dm3Reader3_1
from Centering import Centering
from BinResolution import BinResolution
from Plot import Plot

# Testing
import multiprocessing

class Gui(QtWidgets.QMainWindow, gui_template.Ui_MainWindow):
    def __init__(self, core):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.core = core
        self.curr_image = None
        self.curr_series = None

        # Add pyqtgraph to window
        self.image_view = pg.ImageView()
        self.image_layout.addWidget(self.image_view)

        # Set timer for update function
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_)
        self.timer.start(500)

        # Slider for current show image
        self.slider_image_id.valueChanged.connect(self.value_change)
        self.curr_index = self.slider_image_id.value()

        self.actionOpen.triggered.connect(self.browse_folder)
        # Tools
        self.actionCenter_series.triggered.connect(self.center_series)
        self.actionVirtual_image.triggered.connect(self.virtual_image_start)

        # Filters
        self.actionLog.triggered.connect(self.log_filter)
        self.actionSobel.triggered.connect(self.sobel_filter)
        self.actionCanny.triggered.connect(self.canny_filter)

        # Virtual image threading
        self.plot = None
        self.virtual_image_on = False
        self.thread_pool = [Thread(target=self.virtual_image) for i in range(0, multiprocessing.cpu_count()-1)]
        for thread in self.thread_pool:
            thread.daemon = True

        self.statusBar().showMessage("Ready")

    def browse_folder(self):
        files_path = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Files')

        self.statusBar().showMessage("Loading files...")

        bin_resolution = BinResolution()
        if path.basename(files_path[0][0]).split(sep='.')[1] == 'dm3':
            self.core.original = BraggImage(files_path[0][0],
                                            bin_resolution.dtype,
                                            (len(files_path[0]),
                                             bin_resolution.width,
                                             bin_resolution.height))
            if self.core.original.load:
                self.core.original.load = False
                for index, file in enumerate(files_path[0]):
                    self.core.original.arrays[index, :, :] = Dm3Reader3_1.ReadDm3File(file)

        elif path.basename(files_path[0][0]).split(sep='.')[1] == 'bin':
            self.core.original = BraggImage(files_path[0][0],
                                            bin_resolution.dtype,
                                            (len(files_path[0]),
                                             bin_resolution.width,
                                             bin_resolution.height))
            if self.core.original.load:
                self.core.original.load = False
                for index, file in enumerate(files_path[0]):
                    self.core.original.arrays[index, :, :] = \
                        BinReader.read_bin_file(file,
                                                bin_resolution.dtype,
                                                bin_resolution.offset,
                                                (bin_resolution.width, bin_resolution.height))
        else:
            self.statusBar().showMessage("Not supported file type.")

        self.statusBar().showMessage("Read")

        self.curr_series = self.core.original

        self.curr_image = self.curr_series.arrays[self.curr_index, :, :]
        self.image_view.setImage(self.curr_image)
        self.curr_image_name.setPlainText(str(self.curr_index))
        self.slider_image_id.setMaximum(self.curr_series.arrays.shape[0]-1)

    def value_change(self):
        self.curr_index = self.slider_image_id.value()
        self.curr_image = self.curr_series.arrays[self.curr_index, :, :]
        self.image_view.setImage(self.curr_image)
        self.curr_image_name.setPlainText(str(self.curr_index))

    def load_template(self):
        image = self.image_view.roi.getArrayRegion(self.curr_image, self.image_view.getImageItem())
        self.core.template = image

        image = misc.imresize(image, (100, 100))
        image = np.flip(image, 0)
        image = misc.imrotate(image, -90)

        misc.imsave('template.png', image)
        self.label_template.setPixmap(QtGui.QPixmap('template.png'))

    def center_series(self):
        self.load_template()
        self.statusBar().showMessage("Centering...")
        self.core.center = Centering().move(self.core.original,
                                            self.core.template,
                                            self.image_view)
        self.statusBar().showMessage("Ready")

    def virtual_image_start(self):
        virtual_image_resolution = VirtualImageResolution()
        self.core.virtual_image = np.zeros((virtual_image_resolution.width, virtual_image_resolution.height))
        self.virtual_image_on = not self.virtual_image_on
        if self.virtual_image_on:
            self.plot = Plot()
            for thread in self.thread_pool:
                if not thread.is_alive():
                    thread.start()

    # In another thread
    def virtual_image(self):
        while 1:
                for i in range(self.core.virtual_image.shape[0]):
                    for j in range(self.core.virtual_image.shape[1]):
                        self.core.virtual_image[i, j] =\
                            np.mean(
                                self.image_view.roi.getArrayRegion(
                                    self.curr_series.arrays[i*self.core.virtual_image.shape[0]+j, :, :],
                                    self.image_view.getImageItem()))

    def log_filter(self):
        _translate = QtCore.QCoreApplication.translate
        self.core.log = copy.deepcopy(self.curr_series)
        for image in self.core.log:
            image.log(1e1, 1e14)
        self.image_view.setImage(self.core.log[0].array)
        self.image_series.addItem("")
        self.image_series.setItemText(len(self.image_series)-1, _translate("MainWindow", "Log"))

    def sobel_filter(self):
        self.curr_image.soble()
        self.image_view.setImage(self.curr_image.array)

    def canny_filter(self):
        self.curr_image.canny()
        self.image_view.setImage(self.curr_image.array)

    def wiener_filter(self):
        self.curr_image.wiener()
        self.image_view.setImage(self.curr_image.array)

    def update_(self):
        if self.virtual_image_on:
            self.plot.update(self.core.virtual_image)

        if self.move_roi.checkState():
            move_speed = [0.0, 0.0]

            if self.image_view.roi.pos()[0] + self.image_view.roi.size()[0]\
                    > self.image_view.getView().viewRange()[0][1]:
                move_speed[0] = 1

            if self.image_view.roi.pos()[1] + self.image_view.roi.size()[1]\
                    > self.image_view.getView().viewRange()[1][1]:
                move_speed[1] = 1

            self.image_view.getView().translateBy(x=move_speed[0], y=move_speed[1])
