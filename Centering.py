import copy

from skimage import filters
import numpy as np
from scipy import signal
import multiprocessing

from BraggImage import BraggImage


class Centering:
    def __init__(self):
        self.template = None

    def correlation2d(self, face):
        return signal.correlate2d(face.array, self.template.array, mode='same')

    def move(self, images_in, template, template_range):
        self.template = template
        images_out = copy.deepcopy(images_in)

        max_disk_soble = \
            [BraggImage(image.name, filters.sobel(image.array[template_range[0]:template_range[1],
                                                  template_range[2]:template_range[3]]))
             for image in images_in]

        with multiprocessing.Pool(multiprocessing.cpu_count()-1) as p:
            cross = p.map(self.correlation2d, max_disk_soble)

        cross_0 = signal.correlate2d(template.array, template.array, mode='same')
        i_0, j_0 = np.unravel_index(cross_0.argmax(), cross_0.shape)

        for index, data in enumerate(cross):
            i, j = np.unravel_index(data.argmax(), data.shape)
            images_out[index].move(j-j_0, i_0-i)

        return images_out

