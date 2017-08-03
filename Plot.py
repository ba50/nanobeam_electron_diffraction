import matplotlib.pyplot as plt
import numpy as np


class Plot:
    def __init__(self):
        self.image = np.zeros((20, 20))

        self.fig, self.ax = plt.subplots()
        self.draw()
        plt.show(block=False)

    def update(self, image):
        self.image = image
        self.draw()

    def draw(self):
        self.ax.cla()
        self.ax.imshow(self.image, cmap='gray')
        self.fig.canvas.draw()
