import sys
import os
import glob

from scipy import signal

import Dm3Reader3_1
from BraggImage import BraggImage
from Centering import Centering
from Plot import Plot

import numpy as np
from skimage.transform import hough_circle, hough_circle_peaks

from PyQt5 import QtWidgets
from Gui import Gui


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = Gui()
    form.show()
    app.exec_()

"""
path = os.path.join('D:', 'Bartek_dane', 'rudzinski')
files = glob.glob(os.path.join(path, '*.dm3'))

print("Loading data... ", end='')
original = [BraggImage(file, Dm3Reader3_1.ReadDm3File(file)) for file in files[:1]]
print("Ok")

template = BraggImage(original[34].name, original[34].array[119:151, 119:159])
center = Centering.move(original, template, 119, 151, 119, 159)

center_log = [image.log() for image in center]
soble = [image.soble() for image in center_log]

print("Cross... ", end='')
cross = [BraggImage(image.name, signal.correlate2d(image.array, soble[0].array, mode='same')) for image in soble[:7]]
print("Ok")

# Detect two radii
hough_radii = np.arange(2, 10, .5)
hough_res = [hough_circle(image.array, hough_radii) for image in cross]

for index, i in enumerate(hough_res):
    accums, cx, cy, radii = hough_circle_peaks(i, hough_radii, total_num_peaks=25)

    for center_y, center_x, radius in zip(cy, cx, radii):
         cross[index].disks.append((center_x, center_y, radius))
         center_log[index].disks.append((center_x, center_y, radius))

Plot(cross)
Plot(center_log)
"""
