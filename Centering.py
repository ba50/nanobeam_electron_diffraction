from skimage import filters
import numpy as np
from scipy import signal
import multiprocessing


class Centering:
    def __init__(self):
        self.template = None

    def correlation2d(self, face):
        return signal.correlate2d(filters.sobel(face), filters.sobel(self.template), mode='same')

    def move(self, images_in, template, image_view):
        self.template = template

        faces = [image_view.roi.getArrayRegion(images_in.arrays[i, :, :], image_view.getImageItem())
                 for i in range(images_in.arrays.shape[0])]

        with multiprocessing.Pool(multiprocessing.cpu_count()-1) as p:
            cross = p.map(self.correlation2d, faces)

        cross_0 = signal.correlate2d(template, template, mode='same')
        i_0, j_0 = np.unravel_index(cross_0.argmax(), cross_0.shape)

        for index, data in enumerate(cross):
            i, j = np.unravel_index(data.argmax(), data.shape)
            images_in.move(index, j-j_0, i_0-i)
