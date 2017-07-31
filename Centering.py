import copy

from skimage import filters
import numpy as np
from scipy import signal

from BraggImage import BraggImage


class Centering:
    @staticmethod
    def move(images_in, template, template_range):
        images_out = copy.deepcopy(images_in)

        max_disk_soble = \
            [BraggImage(image.name, filters.sobel(image.array[template_range[0]:template_range[1],
                                                  template_range[2]:template_range[3]]))
             for image in images_in]

        cross =\
            [BraggImage(face.name, signal.correlate2d(face.array, template.array, mode='same'))
             for face in max_disk_soble]

        cross_0 = signal.correlate2d(template.array, template.array, mode='same')
        i_0, j_0 = np.unravel_index(cross_0.argmax(), cross_0.shape)

        for index, data in enumerate(cross):
            i, j = np.unravel_index(data.array.argmax(), data.array.shape)
            images_out[index].move(j-j_0, i_0-i)

        return images_out




