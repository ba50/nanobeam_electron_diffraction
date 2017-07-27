import numpy as np

from PyQt5 import QtWidgets, QtCore, QtGui
import gui_template
import pyqtgraph as pg
from scipy import misc

from BraggImage import BraggImage
import Dm3Reader3_1
from Centering import Centering


class Gui(QtWidgets.QMainWindow, gui_template.Ui_MainWindow):
    def __init__(self, core):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.core = core
        self.image_view = pg.ImageView()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_)
        self.timer.start(10)

        self.image_layout.addWidget(self.image_view)

        self.slider_image_id.valueChanged.connect(self.value_change)
        self.curr_index = self.slider_image_id.value()

        self.actionOpen.triggered.connect(self.browse_folder)
        self.actionLoad_template.triggered.connect(self.load_template)
        self.actionCenter_series.triggered.connect(self.center_series)

    def browse_folder(self):
        files_path = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Folder')

        self.statusBar().showMessage("Loading files...")
        self.core.original = [BraggImage(file, Dm3Reader3_1.ReadDm3File(file)) for file in files_path[0]]
        self.statusBar().showMessage("Ok")

        self.image_view.setImage(self.core.original[0].array)
        self.curr_image_name.setPlainText(self.core.original[0].name)
        self.slider_image_id.setMaximum(len(self.core.original)-1)

    def value_change(self):
        self.curr_index = self.slider_image_id.value()
        self.image_view.setImage(self.core.original[self.curr_index].array)
        self.curr_image_name.setPlainText(self.core.original[self.curr_index].name)

    def load_template(self):
        self.core.template_range = [np.ceil(self.image_view.roi.pos()[0]).astype("int"),
                                    np.ceil(self.image_view.roi.pos()[0]+self.image_view.roi.size()[0]).astype("int"),
                                    np.ceil(self.image_view.roi.pos()[1]).astype("int"),
                                    np.ceil(self.image_view.roi.pos()[1]+self.image_view.roi.size()[1]).astype("int")]

        self.core.template = BraggImage(self.core.original[self.curr_index].name,
                                        self.core.original[self.curr_index].array[
                                        self.core.template_range[0]:self.core.template_range[1],
                                        self.core.template_range[2]:self.core.template_range[3]])

        misc.imsave('template.png', misc.imresize(misc.toimage(self.core.template.array), (100, 100)))
        self.label_template.setPixmap(QtGui.QPixmap('template.png'))

    def center_series(self):
        self.core.center = Centering.move(self.core.original, self.core.template, self.core.template_range)

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
