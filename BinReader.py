import copy
import numpy as np


class BinReader:
    @staticmethod
    def read_bin_file(file_name, dtype, offset, shape):
        data = copy.deepcopy(np.memmap(file_name, dtype=dtype,  mode='r', offset=offset, shape=shape))
        return data
