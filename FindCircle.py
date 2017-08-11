from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import find_circle_template
import cv2
import numpy as np


class FindCircle(QDialog, find_circle_template.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.plot = None

        self.min_dist = 20
        self.param1 = 1
        self.param2 = 15
        self.min_radius = 5
        self.max_radius = 15

        self.lineEdit_minDist.setText(str(self.min_dist))
        self.lineEdit_param1.setText(str(self.param1))
        self.lineEdit_param2.setText(str(self.param2))
        self.lineEdit_minRadius.setText(str(self.min_radius))
        self.lineEdit_maxRadius.setText(str(self.max_radius))

        self.buttonBox_set_resolution.accepted.connect(self.set_resolution)

        self.setWindowModality(Qt.WindowModal)
        self.exec_()

    def set_resolution(self):
        self.min_dist = int(self.lineEdit_minDist.text())
        self.param1 = int(self.lineEdit_param1.text())
        self.param2 = int(self.lineEdit_param2.text())
        self.min_radius = int(self.lineEdit_minRadius.text())
        self.max_radius = int(self.lineEdit_maxRadius.text())

        self.find_circle()

    def find_circle(self):
        img = cv2.imread('template.png', 0)
        cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        circles = cv2.HoughCircles(img,
                                   cv2.HOUGH_GRADIENT,
                                   1,
                                   self.min_dist,
                                   param1=self.param1,
                                   param2=self.param2,
                                   minRadius=self.min_radius,
                                   maxRadius=self.max_radius)

        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

        self.plot = cv2.imshow('detected circles', cimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
