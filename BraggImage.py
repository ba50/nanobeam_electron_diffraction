import os.path as path
import numpy as np


class BraggImage:
    def __init__(self, file_path, dtype, shape):
        self.name = path.basename(file_path.split(sep='.')[0])
        self.array = np.zeros(shape, dtype)

    def save(self, file_path):
        save_file = np.memmap(file_path, self.array.dtype, 'w+', 0, self.array.shape)
        save_file[:] = self.array[:]

    def log(self, clip_min=1, clip_max=1e14):
        for i in range(self.array.shape[0]):
            self.array[i, :, :] = np.log(np.clip(self.array[i, :, :], clip_min, clip_max))

    def soble(self):
        self.array = filters.sobel(self.array)

    def canny(self):
        self.array = feature.canny(self.array, sigma=1e-2, low_threshold=0, high_threshold=1e4)

    def wiener(self):
        self.array = signal.wiener(self.array)

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

