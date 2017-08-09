import os.path as path
import numpy as np
from multiprocessing import Process

import gui_template
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
from scipy import misc

from VirtualImageResolution import VirtualImageResolution
from BinResolution import BinResolution

from BraggImage import BraggImage
import Dm3Reader3_1
from Centering import Centering
from Plot import Plot

# Testing
import copy


# In another thread
def virtual_image(virtual_image_, curr_series, image_view):
    while 1:
            for i in range(virtual_image_.shape[0]):
                for j in range(virtual_image_.shape[1]):
                    virtual_image[i, j] =\
                        np.mean(image_view.roi.getArrayRegion(curr_series[i*virtual_image_.shape[0]+j, :, :],
                                                              image_view.getImageItem()))


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

        self.actionOpen.triggered.connect(self.open_files)
        self.actionSave.triggered.connect(self.save_files)

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
        self.process_pool = None

        self.statusBar().showMessage("Ready")

    def open_files(self):
        files_path = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file")
        files_path = files_path[0]
        self.statusBar().showMessage("Loading files...")

        files_type = path.basename(files_path[0]).split(sep='.')[1]

        if files_type == 'dm3':
            tmp = Dm3Reader3_1.ReadDm3File(files_path[0])

            self.core.original = BraggImage(files_path[0],
                                            tmp.dtype,
                                            [len(files_path), tmp.shape[0], tmp.shape[1]])

            for index, file in enumerate(files_path):
                self.core.original.array[index, :, :] = Dm3Reader3_1.ReadDm3File(file)

        elif files_type == 'bin':
            bin_resolution = BinResolution()
            self.core.original = BraggImage(files_path[0],
                                            bin_resolution.dtype,
                                            [len(files_path),
                                             bin_resolution.shape[1],
                                             bin_resolution.shape[2]])

            for index, file in enumerate(files_path):
                self.core.original.array[index, :, :] = copy.deepcopy(np.memmap(file,
                                                                                bin_resolution.dtype,
                                                                                'r',
                                                                                bin_resolution.offset,
                                                                                (bin_resolution.shape[1], bin_resolution.shape[2])))
        elif files_type == 'raw':
            bin_resolution = BinResolution()
            self.core.original = BraggImage(files_path[0], bin_resolution.dtype, bin_resolution.shape)

            self.core.original.array = copy.deepcopy(np.memmap(files_path[0],
                                                               bin_resolution.dtype,
                                                               'r+',
                                                               bin_resolution.offset,
                                                               bin_resolution.shape))
        else:
            self.statusBar().showMessage("Not supported file type.")

        self.curr_series = self.core.original
        self.curr_image = self.curr_series.array[self.curr_index, :, :]
        self.image_view.setImage(self.curr_image)
        self.curr_image_name.setPlainText(str(self.curr_index))
        self.slider_image_id.setMaximum(self.curr_series.array.shape[0] - 1)

        self.statusBar().showMessage("Read")

    def save_files(self):
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
        self.curr_series.save(file_path[0])

    def value_change(self):
        self.curr_index = self.slider_image_id.value()
        self.curr_image = self.curr_series.array[self.curr_index, :, :]
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
        Centering().move(self.core.original,
                         self.core.template,
                         self.image_view)
        self.statusBar().showMessage("Ready")

    def virtual_image_start(self):
        p = Process(target=virtual_image, args=(self.core.virtual_image, self.curr_series.array, self.image_view))
        p.daemon = True
        p.start()

    def log_filter(self):
        self.core.original.log(1e1, 1e14)
        self.image_view.setImage(self.core.original.arrays[0, :, :])
        self.curr_index = 0

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
