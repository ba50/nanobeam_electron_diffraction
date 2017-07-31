import copy
import numpy as np


class BinReader:
    @staticmethod
    def read_bin_file(file_name, shape):
        data = copy.deepcopy(np.memmap(file_name, dtype=np.int32,  mode='r', offset=10, shape=shape))
        return data
