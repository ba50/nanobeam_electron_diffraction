import numpy as np

from PyQt5 import QtWidgets, QtCore, QtGui
import gui_template
import pyqtgraph as pg
from scipy import misc

from BraggImage import BraggImage
import Dm3Reader3_1
from Centering import Centering

import matplotlib.pyplot as plt
from scipy.ndimage.filters  import gaussian_filter


class Gui(QtWidgets.QMainWindow, gui_template.Ui_MainWindow):
    def __init__(self, core):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.core = core
        self.curr_series = None

        self.image_view = pg.ImageView()

        self.statusBar().showMessage("Loading files...")
        files_path = ['dd020.dm3']
        self.core.original = [BraggImage(file, Dm3Reader3_1.ReadDm3File(file)) for file in files_path]
        self.statusBar().showMessage("Ok")

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
            self.actionLog.triggered.connect(self.log_filter)
            self.actionSobel.triggered.connect(self.sobel_filter)
            self.actionCanny.triggered.connect(self.canny_filter)
            self.actionWiener.triggered.connect(self.wiener_filter)

            self.actionTesting_2.triggered.connect(self.testing_2)
        else:
            self.statusBar().showMessage("No image.")

        self.image_series.activated[str].connect(self.change_series)

    def browse_folder(self):
        files_path = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Folder')

        self.statusBar().showMessage("Loading files...")
        self.core.original = [BraggImage(file, Dm3Reader3_1.ReadDm3File(file)) for file in files_path[0]]
        self.statusBar().showMessage("Ok")

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
        self.core.center = Centering.move(self.core.original, self.core.template, self.core.template_range)

    def testing(self):
        plt.figure()
        plt.plot(range(0, 256), self.curr_image.array[:, 128])
        plt.show(block=False)

    def change_series(self, text):
        if text == 'Original':
            if self.core.original:
                self.curr_series = self.core.original
                self.image_view.setImage(self.curr_series[self.curr_index].array)
            else:
                self.statusBar().showMessage("Original series is empty.")
        elif text == 'Centred':
            if self.core.center:
                self.curr_series = self.core.center
                self.image_view.setImage(self.curr_series[self.curr_index].array)
            else:
                self.statusBar().showMessage("Centred series is empty.")

    def log_filter(self):
        self.curr_image.log(1e1, 1e14)
        self.image_view.setImage(self.curr_image.array)

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
