import copy
import numpy as np


class BinReader:
    @staticmethod
    def read_bin_file(files_path, bin_):
        data = np.zeros([len(files_path), bin_.shape[0], bin_.shape[1]],
                        bin_.dtype)
        for index, file in enumerate(files_path):
            data[index, :, :] = copy.deepcopy(np.memmap(file,
                                                        dtype=bin_.dtype,
                                                        mode='r',
                                                        offset=bin_.offset,
                                                        shape=bin_.shape))
        return data
