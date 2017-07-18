import matplotlib.pyplot as plt


class Plot:
    def __init__(self, images, cmap='gray'):
        self.images = images
        self.curr_pos = 0
        self.cmap = cmap

        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('key_press_event', self.key_event)
        self.ax = self.fig.add_subplot(111)
        self.fig.suptitle(self.images[self.curr_pos].name, fontsize=20)
        self.ax.imshow(self.images[self.curr_pos].array, cmap=self.cmap)
        plt.show()

    def key_event(self, e):
        if e.key == 'right':
            self.curr_pos += 1
        elif e.key == 'left':
            self.curr_pos -= 1
        else:
            return

        self.curr_pos = self.curr_pos % len(self.images)
        self.ax.cla()
        self.fig.suptitle(self.images[self.curr_pos].name, fontsize=20)
        self.ax.imshow(self.images[self.curr_pos].array, cmap=self.cmap)
        self.fig.canvas.draw()
