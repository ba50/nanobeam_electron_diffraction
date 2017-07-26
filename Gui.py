import numpy as np

from PyQt5 import QtWidgets, QtCore, QtGui
import gui_template
import pyqtgraph as pg
from scipy import misc

from BraggImage import BraggImage
import Dm3Reader3_1


class Gui(QtWidgets.QMainWindow, gui_template.Ui_MainWindow):
    def __init__(self, core):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.browse_folder)
        self.image_view = pg.ImageView()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

        self.image_layout.addWidget(self.image_view)

        self.core = core

        self.horizontalSlider.valueChanged.connect(self.value_change)
        self.curr_index = self.horizontalSlider.value()

        self.actionLoad_template.triggered.connect(self.load_template)

    def browse_folder(self):
        files_path = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Folder')

        self.statusBar().showMessage("Loading files...")
        self.core.original = [BraggImage(file, Dm3Reader3_1.ReadDm3File(file)) for file in files_path[0]]
        self.statusBar().showMessage("Ok")

        self.image_view.setImage(self.core.original[0].array)
        self.textBrowser.setPlainText(self.core.original[0].name)
        self.horizontalSlider.setMaximum(len(self.core.original)-1)

    def value_change(self):
        self.curr_index = self.horizontalSlider.value()
        self.image_view.setImage(self.core.original[self.curr_index].array)
        self.textBrowser.setPlainText(self.core.original[self.curr_index].name)

    def load_template(self):
        xmin = np.ceil(self.image_view.roi.pos()[0]).astype("int")
        xmax = np.ceil(self.image_view.roi.pos()[0]+self.image_view.roi.size()[0]).astype("int")
        ymin = np.ceil(self.image_view.roi.pos()[1]).astype("int")
        ymax = np.ceil(self.image_view.roi.pos()[1]+self.image_view.roi.size()[1]).astype("int")
        template = np.copy(self.core.original[self.curr_index].array[xmin:xmax][ymin:ymax])
        misc.imsave('template.png', template)
        self.label.setPixmap(QtGui.QPixmap('template.png'))

    def update(self):
        move_speed = [0.0, 0.0]

        if self.move.checkState():
            if self.image_view.roi.pos()[0] + self.image_view.roi.size()[0]\
                    > self.image_view.getView().viewRange()[0][1]:
                move_speed[0] = .1

            if self.image_view.roi.pos()[1] + self.image_view.roi.size()[1]\
                    > self.image_view.getView().viewRange()[1][1]:
                move_speed[1] = .1

        self.image_view.getView().translateBy(x=move_speed[0], y=move_speed[1])
