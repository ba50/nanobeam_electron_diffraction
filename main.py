import numpy as np
from scipy import signal
from skimage import filters
import os
import glob

from Plot import Plot
import Dm3Reader3_1
from Image import Image

files = glob.glob(os.path.join('D:', 'Bartek_dane', 'rudzinski', '*.dm3'))

original = [Image(file, Dm3Reader3_1.ReadDm3File(file)) for file in files[34:100]]
original_log = [Image(image.name, image.log()) for image in original]
max_disk = [Image(image.name, image.array[119:151, 119:159]) for image in original_log]
soble = [Image(image.name, filters.sobel(image.array)) for image in max_disk]
cross =\
    [Image(template.name, signal.correlate2d(soble[0].array, template.array, mode='same')) for template in soble]

to_center = []
i_0, j_0 = np.unravel_index(cross[0].array.argmax(), cross[0].array.shape)
for index, data in enumerate(cross):
    i_cross, j_cross = np.unravel_index(data.array.argmax(), data.array.shape)
    cross[index].array[i_cross, j_cross] = -1
    i, j = (i_0-i_cross)+i_0, (j_0-j_cross)+j_0
    max_disk[index].array[i, j] = -1
    original[index].array[119+i, 119+j] = -1
    to_center.append((i-i_0, j-j_0))

Plot(original)
for index, data in enumerate(to_center):
    print(data[0], data[1])
    original[index].move_center(data[1], -data[0])

Plot(original)
