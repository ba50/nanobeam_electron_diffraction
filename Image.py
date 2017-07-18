import numpy as np
from skimage import io
import os.path as path


class Image:
    def __init__(self, file_name, array, log=False):
        self.name = path.basename(file_name)
        self.array = array

        if log:
            self.array = np.log(self.array)

    def plot(self):
        io.imshow(self.array)
        io.show()

    def move_center(self, dx, dy):
        if dx > 0:
            self.array = self.array[:, dx:self.array.shape[0]]
            self.array = np.c_[self.array, np.zeros((self.array.shape[0], dx))]
        elif dx < 0:
            self.array = self.array[:, 0:self.array.shape[1]+dx]
            self.array = np.c_[np.zeros((self.array.shape[0], abs(dx))), self.array]

        if dy > 0:
            self.array = self.array[0:self.array.shape[0]-dy, :]
            self.array = np.r_[np.zeros((dy, self.array.shape[1])), self.array]
        elif dy < 0:
            self.array = self.array[abs(dy):self.array.shape[1], :]
            self.array = np.r_[self.array, np.zeros((abs(dy), self.array.shape[1]))]
