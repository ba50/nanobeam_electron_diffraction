import copy
import os.path as path

import numpy as np
import matplotlib.pyplot as plt
from skimage import filters
from scipy import misc


class BraggImage:
    def __init__(self, file_name, array):
        self.name = path.basename(file_name)
        self.array = np.copy(array)
        self.disks = []

    def log(self, clip_min=1e3, clip_max=1e4):
        temp = copy.deepcopy(self)
        temp.array = np.log(np.clip(temp.array, clip_min, clip_max))
        return temp

    def soble(self):
        temp = copy.deepcopy(self)
        temp.array = filters.sobel(self.array)
        return temp

    def move(self, dx, dy):
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

    def find_disks(self):
        pass

    def save(self, file):
        misc.imsave(file, self.array)

    def plot(self):
        fig, ax = plt.subplots()
        circles = [plt.Circle((disk[0], disk[1]), disk[2], color='r', alpha=.25) for disk in self.disks]
        for circle in circles:
            ax.add_artist(circle)
        plt.imshow(self.array, cmap='gray')
        plt.show()
