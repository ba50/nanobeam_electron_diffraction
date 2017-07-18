import os.path as path

class Image:
    def __init__(self, file_name, array, log=False):
        self.name = path.basename(file_name)
        self.array = array

        if log:
            self.array = np.log(self.array)

