import matplotlib.pyplot as plt
from skimage import filters
from scipy import signal
import numpy as np
from os import path
import glob

from Plot import Plot
from Disk import Disk
import Dm3Reader3_1
from Image import Image

files = glob.glob(path.join('D:', 'Bartek_dane', 'rudzinski', '*.dm3'))[:100]
print("Load data...\n")
original = [Image(file, np.asarray(Dm3Reader3_1.ReadDm3File(file))) for file in files]

print("Make part...\n")
part = [Image(image.name, filters.sobel(image.array[115:152, 115:152])) for image in original]
Plot(part)

print('Correlate2d...')
corr_vector = \
    [Image(template.name, signal.correlate2d(part[0].array, template.array, mode='same')) for template in part]

Plot(corr_vector)

print("Fined center...\n")
disks = []
for index, corr in enumerate(corr_vector):
    i, j = np.unravel_index(corr.array.argmax(), corr.array.shape)
    disks.append(Disk(corr.name, part[index].array, i, j, None))

delta = [(disk.x - disks[0].x, disk.y - disks[0].y) for disk in disks]

center = [Image(image.name, image.array) for image in original]

for index, d in enumerate(delta):
    print(disks[index].name, d)
    center[index].move_center(d[0], -d[1])

print("Make part...\n")
part_1 = [Image(image.name, filters.sobel(image.array[122:138, 130:146])) for image in center]

print('Correlate2d...')
corr_vector_1 = \
    [Image(template.name, signal.correlate2d(part[0].array, template.array, mode='same')) for template in part_1]

print("Fined center...\n")
disks_1 = []
for index, corr in enumerate(corr_vector_1):
    i, j = np.unravel_index(corr.array.argmax(), corr.array.shape)
    disks_1.append(Disk(corr.name, part[index].array, i, j, None))

delta_1 = [(disk.x - disks_1[0].x, disk.y - disks_1[0].y) for disk in disks_1]

delta = np.array(delta)
delta_1 = np.array(delta_1)

plt.plot(delta[:, 0], delta[:, 1])
plt.figure()
plt.plot(delta_1[:, 0], delta_1[:, 1])
plt.show()

