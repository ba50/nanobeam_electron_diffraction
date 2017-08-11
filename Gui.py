import os.path as path
import numpy as np
import copy

import gui_template
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
from scipy import misc

from BinResolution import BinResolution

from BraggImage import BraggImage
import Dm3Reader3_1
from Centering import Centering
from VirtualImagePlot import VirtualImagePlot

# Testing
from FindCircle import FindCircle


class Gui(QtWidgets.QMainWindow, gui_template.Ui_MainWindow):
    def __init__(self, core):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.core = core
        self.curr_image = None
        self.curr_series = None
        self.vi_plot = None
        self.find_circle = None

        # Add pyqtgraph to window
        self.image_view = pg.ImageView()
        self.image_layout.addWidget(self.image_view)

        # Set timer for update function
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_move_roi)
        self.timer.start(100)

        # Slider for current show image
        self.slider_image_id.valueChanged.connect(self.value_change)
        self.curr_index = self.slider_image_id.value()

        # Load and Save
        self.actionOpen.triggered.connect(self.open_files)
        self.actionSave.triggered.connect(self.save_files)

        # Tools
        self.actionCenter_series.triggered.connect(self.center_series)
        self.actionVirtual_image.triggered.connect(self.virtual_image_start)
        self.actionFind_circles.triggered.connect(self.find_circle_start)

        # Filters
        self.actionLog.triggered.connect(self.log_filter)
        self.actionSobel.triggered.connect(self.sobel_filter)
        self.actionCanny.triggered.connect(self.canny_filter)

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
        if self.curr_series:
            file_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
            self.curr_series.save(file_path[0])
        else:
            self.statusBar().showMessage('No files')

    def value_change(self):
        self.curr_index = self.slider_image_id.value()
        self.curr_image_name.setPlainText(str(self.curr_index))
        self.curr_image = self.curr_series.array[self.curr_index, :, :]
        self.update_image()

    def load_template(self):
        if self.curr_series:
            image = self.image_view.roi.getArrayRegion(self.curr_image, self.image_view.getImageItem())
            self.core.template = image

            image = misc.imresize(image, (100, 100))
            image = np.flip(image, 0)
            image = misc.imrotate(image, -90)

            misc.imsave('template.png', image)
            self.label_template.setPixmap(QtGui.QPixmap('template.png'))
        else:
            self.statusBar().showMessage('No files')

    def center_series(self):
        if self.curr_series:
            self.load_template()
            self.statusBar().showMessage("Centering...")
            Centering().move(self.core.original,
                             self.core.template,
                             self.image_view)
            self.update_image()
            self.statusBar().showMessage("Ready")
        else:
            self.statusBar().showMessage('No files')

    def virtual_image_start(self):
        if self.curr_series:
            self.vi_plot = VirtualImagePlot(self.curr_series, self.image_view)
        else:
            self.statusBar().showMessage('No files')

    def find_circle_start(self):
        self.load_template()
        self.find_circle = FindCircle()

    def log_filter(self):
        if self.curr_series:
            self.statusBar().showMessage("Log...")
            self.core.original.log()
            self.update_image()
            self.statusBar().showMessage("Ready")
        else:
            self.statusBar().showMessage('No files')

    def sobel_filter(self):
        if self.curr_series:
            self.statusBar().showMessage("Soble...")
            self.core.original.soble()
            self.update_image()
            self.statusBar().showMessage("Ready")
        else:
            self.statusBar().showMessage('No files')

    def canny_filter(self):
        if self.curr_series:
            self.statusBar().showMessage("Canny...")
            self.core.original.canny()
            self.update_image()
            self.statusBar().showMessage("Ready")
        else:
            self.statusBar().showMessage('No files')

    def update_image(self):
        self.image_view.setImage(self.curr_image)

    def update_move_roi(self):
        if self.move_roi.checkState():
            move_speed = [0.0, 0.0]

            if self.image_view.roi.pos()[0] + self.image_view.roi.size()[0]\
                    > self.image_view.getView().viewRange()[0][1]:
                move_speed[0] = 1

            if self.image_view.roi.pos()[1] + self.image_view.roi.size()[1]\
                    > self.image_view.getView().viewRange()[1][1]:
                move_speed[1] = 1

            self.image_view.getView().translateBy(x=move_speed[0], y=move_speed[1])
