import os.path as path
import numpy as np
import multiprocessing
from skimage import filters
from skimage import feature
from sklearn import preprocessing

# Testing
import matplotlib.pyplot as plt


class BraggImage:
    def __init__(self, file_path, dtype, shape):
        self.name = path.basename(file_path.split(sep='.')[0])
        self.array = np.zeros(shape, dtype)

    def save(self, file_path):
        save_file = np.memmap(file_path, self.array.dtype, 'w+', 0, self.array.shape)
        save_file[:] = self.array[:]

    @staticmethod
    def log_(image):
        return np.log(image)

    @staticmethod
    def soble_(image):
        return preprocessing.normalize(filters.sobel(image))

    # Not tested problem with low_, high_ parameters
    @staticmethod
    def canny_(image):
        return feature.canny(image, sigma=1e-2, low_threshold=0, high_threshold=1e4)

    def log(self, clip_min=1, clip_max=1e14):
        images = [np.clip(self.array[i, :, :], clip_min, clip_max) for i in range(self.array.shape[0])]

        with multiprocessing.Pool(multiprocessing.cpu_count()-1) as p:
            images_ = p.map(self.log_, images)
        
        for i in range(self.array.shape[0]):
            self.array[i, :, :] = images_[i]

    # Displaying image problem
    def soble(self):
        images = [self.array[i, :, :] for i in range(self.array.shape[0])]

        with multiprocessing.Pool(multiprocessing.cpu_count()-1) as p:
            images_ = p.map(self.soble_, images)

        images_ = np.clip(images_, 0, 1e14)

        plt.imshow(images_[0])
        plt.show()

        for i in range(self.array.shape[0]):
            self.array[i, :, :] = images_[i]

    # Not working
    def canny(self):
        images = [self.array[i, :, :] for i in range(self.array.shape[0])]

        with multiprocessing.Pool(multiprocessing.cpu_count()-1) as p:
            images_ = p.map(self.canny_, images)

        for i in range(self.array.shape[0]):
            self.array[i, :, :] = images_[i]

    def move(self, index, dx, dy):
        tmp = self.array[index, :, :]
        if dx > 0:
            tmp = self.array[index, :, dx:self.array.shape[1]]
            tmp = np.c_[tmp, np.zeros((self.array.shape[1], dx))]
        elif dx < 0:
            tmp = self.array[index, :, 0:self.array.shape[2] + dx]
            tmp = np.c_[np.zeros((self.array.shape[1], abs(dx))), tmp]

        if dy > 0:
            tmp = self.array[index, 0:self.array.shape[1] - dy, :]
            tmp = np.r_[np.zeros((dy, self.array.shape[2])), tmp]
        elif dy < 0:
            tmp = self.array[index, abs(dy):self.array.shape[2], :]
            tmp = np.r_[tmp, np.zeros((abs(dy), self.array.shape[2]))]

        self.array[index, :, :] = tmp

