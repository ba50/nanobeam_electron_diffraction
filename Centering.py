import copy

from skimage import filters
import numpy as np
from scipy import signal

from BraggImage import BraggImage


class Centering:
    @staticmethod
    def move(images_in, template, min_x, max_x, min_y, max_y):
        images = copy.deepcopy(images_in)
        images_log = [image.log() for image in images_in]
        template = template.log()

        max_disk_soble =\
            [BraggImage(image.name, filters.sobel(image.array[min_x:max_x, min_y:max_y]))
             for image in images_log]

        cross =\
            [BraggImage(face.name, signal.correlate2d(face.array, template.array, mode='same'))
             for face in max_disk_soble]

        cross_0 = signal.correlate2d(template.array, template.array, mode='same')
        i_0, j_0 = np.unravel_index(cross_0.argmax(), cross_0.shape)

        for index, data in enumerate(cross):
            i, j = np.unravel_index(data.array.argmax(), data.array.shape)
            images[index].move(j-j_0, i_0-i)

        return images




