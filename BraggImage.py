import os.path as path
import os


import numpy as np


class BraggImage:
    def __init__(self, file_path, dtype, shape):
        self.name = path.basename(file_path.split(sep='.')[0])
        self.load = False
        if path.isfile(self.name):
            self.arrays = np.memmap(self.name, dtype=dtype, mode='r+', shape=shape)
        else:
            self.arrays = np.memmap(self.name, dtype=dtype, mode='w+', shape=shape)
            self.load = True

    def log(self, clip_min=1, clip_max=1e14):
        for i in range(self.arrays.shape[0]):
            self.arrays[i, :, :] = np.log(np.clip(self.arrays[i, :, :], clip_min, clip_max))

    def soble(self):
        self.array = filters.sobel(self.array)

    def canny(self):
        self.array = feature.canny(self.array, sigma=1e-2, low_threshold=0, high_threshold=1e4)

    def wiener(self):
        self.array = signal.wiener(self.array)

    def move(self, index, dx, dy):
        tmp = self.arrays[index, :, :]
        if dx > 0:
            tmp = self.arrays[index, :, dx:self.arrays.shape[1]]
            tmp = np.c_[tmp, np.zeros((self.arrays.shape[1], dx))]
        elif dx < 0:
            tmp = self.arrays[index, :, 0:self.arrays.shape[2]+dx]
            tmp = np.c_[np.zeros((self.arrays.shape[1], abs(dx))), tmp]

        if dy > 0:
            tmp = self.arrays[index, 0:self.arrays.shape[1]-dy, :]
            tmp = np.r_[np.zeros((dy, self.arrays.shape[2])), tmp]
        elif dy < 0:
            tmp = self.arrays[index, abs(dy):self.arrays.shape[2], :]
            tmp = np.r_[tmp, np.zeros((abs(dy), self.arrays.shape[2]))]

        self.arrays[index, :, :] = tmp

