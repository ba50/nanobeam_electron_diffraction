from PyQt5 import QtWidgets, QtCore, QtGui
import gui_template
import pyqtgraph as pg

from BraggImage import BraggImage
import Dm3Reader3_1


class Gui(QtWidgets.QMainWindow, gui_template.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.select_folder.clicked.connect(self.browse_folder)
        self.image_view = pg.ImageView()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

        self.image_layout.addWidget(self.image_view)


    def browse_folder(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a folder")
        image = BraggImage(file_path[0], Dm3Reader3_1.ReadDm3File(file_path[0]))
        self.image_view.setImage(image.array)

    def update(self):
        #print(self.image_view.roi.pos() + self.image_view.roi.getHandles()[0].pos())
        #print(self.image_view.getView().viewRect())
        move_speed = [0.0, 0.0]

        if self.image_view.roi.pos()[0] + self.image_view.roi.getHandles()[0].pos()[0] > self.image_view.getView().viewRect().width() - 127:
            move_speed[0] = .1

        if self.image_view.roi.pos()[1] + self.image_view.roi.getHandles()[0].pos()[1] > self.image_view.getView().viewRect().height():
            move_speed[1] = .1
        self.image_view.getView().translateBy(x=move_speed[0], y=move_speed[1])
