from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from os import path
import glob

import Dm3Reader3
from Image import Image
from Plot import Plot

files = sorted(glob.glob(path.join('*.dm3')))
original = [Image(file, np.asarray(Dm3Reader3.ReadDm3File(file)).reshape(668, 672)) for file in files]

part = [Image(image.name,
        image.array[318:352, 306:339])
        for image in original]

print(len(part))

corr_vector =   [Image(template.name,
                signal.correlate2d(part[0].array, template.array))
                for template in part]

print(len(corr_vector))

for index, corr in enumerate(corr_vector):
    i, j = np.unravel_index(corr.array.argmax(), corr.array.shape)
    part[index].array[i, j] = 0

Plot(part)

