import os.path as path
import numpy as np

from PyQt5 import QtWidgets, QtCore, QtGui
import gui_template
import pyqtgraph as pg
from scipy import misc

from BinReader import BinReader
from BraggImage import BraggImage
import Dm3Reader3_1
from Centering import Centering
from BinResolution import BinResolution

import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import copy


class Gui(QtWidgets.QMainWindow, gui_template.Ui_MainWindow):
    def __init__(self, core):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.core = core
        self.curr_series = None
        self.bin_resolution = None

        self.image_view = pg.ImageView()

        self.statusBar().showMessage("Loading files...")
        files_path = ['CCD Spectrum image_001.bin']
        self.core.original =\
            [BraggImage(file, BinReader.read_bin_file(file, np.int32, 10, (512, 512))) for file in files_path]
        self.statusBar().showMessage("Ready")

        self.curr_series = self.core.original

        self.image_view.setImage(self.curr_series[0].array)
        self.curr_image_name.setPlainText(self.curr_series[0].name)
        self.slider_image_id.setMaximum(len(self.curr_series)-1)

        self.curr_image = self.curr_series[0]

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_)
        self.timer.start(10)

        self.image_layout.addWidget(self.image_view)

        self.slider_image_id.valueChanged.connect(self.value_change)
        self.curr_index = self.slider_image_id.value()

        self.actionOpen.triggered.connect(self.browse_folder)
        if self.curr_image:
            self.actionLoad_template.triggered.connect(self.load_template)
            self.actionCenter_series.triggered.connect(self.center_series)
            self.actionTesting.triggered.connect(self.testing)
            self.actionVirtual_image.triggered.connect(self.virtual_image)

            self.actionLog.triggered.connect(self.log_filter)
            self.actionSobel.triggered.connect(self.sobel_filter)
            self.actionCanny.triggered.connect(self.canny_filter)

            self.actionWiener.triggered.connect(self.wiener_filter)

            self.actionTesting_2.triggered.connect(self.testing_2)
        else:
            self.statusBar().showMessage("No image.")

        self.image_series.activated[str].connect(self.change_series)

        self.statusBar().showMessage("Ready")

    def browse_folder(self):
        files_path = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Folder')

        self.statusBar().showMessage("Loading files...")

        self.core.original = []
        if path.basename(files_path[0][0]).split(sep='.')[1] == 'dm3':
            for file in files_path[0]:
                self.core.original.append(BraggImage(file, Dm3Reader3_1.ReadDm3File(file)))
        elif path.basename(files_path[0][0]).split(sep='.')[1] == 'bin':
            self.bin_resolution = BinResolution()
            for file in files_path[0]:
                self.core.original.append(BraggImage(file,
                                                     BinReader.read_bin_file(file,
                                                                             self.bin_resolution.type,
                                                                             self.bin_resolution.offset,
                                                                             (self.bin_resolution.width,
                                                                              self.bin_resolution.height)
                                                                             )
                                                     )
                                          )
        else:
            self.statusBar().showMessage("Not supported file type.")

        self.statusBar().showMessage("Read")

        self.curr_series = self.core.original

        self.curr_image = self.curr_series[self.curr_index]
        self.image_view.setImage(self.curr_image.array)
        self.curr_image_name.setPlainText(self.curr_image.name)
        self.slider_image_id.setMaximum(len(self.curr_series)-1)

    def value_change(self):
        self.curr_index = self.slider_image_id.value()
        self.curr_image = self.curr_series[self.curr_index]
        self.image_view.setImage(self.curr_image.array)
        self.curr_image_name.setPlainText(self.curr_image.name)

    def load_template(self):
        self.core.template_range = [np.ceil(self.image_view.roi.pos()[0]).astype("int"),
                                    np.ceil(self.image_view.roi.pos()[0]+self.image_view.roi.size()[0]).astype("int"),
                                    np.ceil(self.image_view.roi.pos()[1]).astype("int"),
                                    np.ceil(self.image_view.roi.pos()[1]+self.image_view.roi.size()[1]).astype("int")]

        self.core.template = BraggImage(self.curr_image.name,
                                        self.curr_image.array[
                                        self.core.template_range[0]:self.core.template_range[1],
                                        self.core.template_range[2]:self.core.template_range[3]])

        misc.imsave('template.png', misc.imresize(misc.toimage(self.core.template.array), (100, 100)))
        self.label_template.setPixmap(QtGui.QPixmap('template.png'))

    def center_series(self):
        _translate = QtCore.QCoreApplication.translate
        self.statusBar().showMessage("Centering...")
        if self.core.template:
            self.core.center = Centering().move(self.core.original, self.core.template, self.core.template_range)
            self.statusBar().showMessage("Ready")
            self.image_series.addItem("")
            self.image_series.setItemText(len(self.image_series)-1, _translate("MainWindow", "Centred"))
        else:
            self.statusBar().showMessage("Empty template.")

    def virtual_image(self):
        self.core.virtual_image = []
        for image in self.curr_series:
            self.core.virtual_image.append(np.mean(image.array[self.core.template_range[0]:self.core.template_range[1],
                                                   self.core.template_range[2]:self.core.template_range[3]]))
        self.core.virtual_image = np.array(self.core.virtual_image)
        self.core.virtual_image = self.core.virtual_image.reshape(20, 20)

        plt.figure()
        plt.imshow(self.core.virtual_image, cmap='gray')
        plt.show()

    def testing(self):
        # Load picture and detect edges
        image = self.curr_image.array
        plt.imshow(image)
        #image = img_as_ubyte(data.coins()[160:230, 70:270])
        edges = canny(image, sigma=1, low_threshold=0, high_threshold=1e10)

        # Detect two radii
        hough_radii = np.arange(20, 35, 2)
        hough_res = hough_circle(edges, hough_radii)

        # Select the most prominent 5 circles
        accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                                   total_num_peaks=3)

        # Draw them
        fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
        image = color.gray2rgb(image)
        for center_y, center_x, radius in zip(cy, cx, radii):
            circy, circx = circle_perimeter(center_y, center_x, radius)
            image[circy, circx] = (220, 20, 20)

        ax.imshow(image, cmap=plt.cm.gray)
        plt.show()

    def change_series(self, text):
        if text == 'Original':
            self.curr_series = self.core.original
        elif text == 'Centred':
            self.curr_series = self.core.center
        elif text == 'Log':
            self.curr_series = self.core.log

        self.curr_image = self.curr_series[self.curr_index]
        self.image_view.setImage(self.curr_image.array)

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

    def testing_2(self):

        data = self.curr_image.array
        total = data.sum()
        X, Y = np.indices(data.shape)
        x = (X*data).sum()/total
        y = (Y*data).sum()/total
        col = data[:, int(y)]
        width_x = np.sqrt(np.abs((np.arange(col.size)-y)**2*col).sum()/col.sum())
        row = data[int(x), :]
        width_y = np.sqrt(np.abs((np.arange(row.size)-x)**2*row).sum()/row.sum())

        self.core.background = gaussian_filter(self.curr_image.array, [width_x, width_y])

        plt.figure()
        plt.imshow(self.core.background, cmap='gray')
        plt.show()

        self.curr_image = BraggImage(self.curr_image.name, np.clip(self.curr_image.array - self.core.background, 0, 1e14))
        self.image_view.setImage(self.curr_image.array)

        """
        image = np.gradient(self.curr_image.array)
        plt.figure()
        plt.imshow(image[0], cmap='gray')
        plt.figure()
        plt.imshow(image[1], cmap='gray')
        plt.show(block=False)
        """

    def update_(self):
        if self.move_roi.checkState():
            move_speed = [0.0, 0.0]

            if self.image_view.roi.pos()[0] + self.image_view.roi.size()[0]\
                    > self.image_view.getView().viewRange()[0][1]:
                move_speed[0] = .1

            if self.image_view.roi.pos()[1] + self.image_view.roi.size()[1]\
                    > self.image_view.getView().viewRange()[1][1]:
                move_speed[1] = .1

            self.image_view.getView().translateBy(x=move_speed[0], y=move_speed[1])
