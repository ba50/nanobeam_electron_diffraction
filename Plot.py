import matplotlib.pyplot as plt


class Plot:
    def __init__(self, images, cmap='gray'):
        self.images = images
        self.curr_pos = 0
        self.cmap = cmap

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('key_press_event', self.key_event)
        self.draw()
        plt.show()

    def key_event(self, e):
        if e.key == 'right':
            self.curr_pos += 1
        elif e.key == 'left':
            self.curr_pos -= 1
        else:
            return

        self.curr_pos = self.curr_pos % len(self.images)
        self.draw()

    def draw(self):
        self.ax.cla()

        self.fig.suptitle(self.images[self.curr_pos].name, fontsize=20)

        self.ax.imshow(self.images[self.curr_pos].array, cmap=self.cmap)

        circles = [plt.Circle((disk[0], disk[1]), disk[2], color='r', alpha=.50) for disk in self.images[self.curr_pos].disks]
        for circle in circles:
            self.ax.add_artist(circle)

        self.fig.canvas.draw()
