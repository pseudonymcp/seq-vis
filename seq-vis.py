import numpy as np
import scipy.ndimage
from scipy.misc import toimage
from scipy.misc import imsave
import math
import sys

# ===== Configuration
# ----- Specify sequence file for import
filename = sys.argv[1]

# ----- Specify ratio of output graphics
width = 4.0
height = 3.0

# for mcs16
# width = 20.5
# height = 1.0
ratio = height / width

# ----- Specify colors
colA = [210, 22, 72]  # red
colC = [255, 209, 54]  # yellow
colG = [22, 192, 210]  # turquoise
colT = [185, 210, 22]  # green
colDefault = [255, 255, 255]  # white

# for black/white GC-content
# colA = [255, 255, 255] # white
# colC = [0, 0, 0] # black
# colG = [0, 0, 0] # black
# colT = [255, 255, 255] # white
# colDefault = [120, 120, 120] # grey


# ===== Program
# ----- Import sequence data and join sequence
with open(filename, "r") as f:
    fList = f.read().splitlines()
seq = str.join("", fList[:])

# ----- Calculate side length for a square
# seq = seq[:len(seq)/6]
# side = int(math.sqrt(len(seq)))
# x = side
# y = side

x = int(math.sqrt(len(seq) / ratio))
y = int(x * ratio)
# print ratio, x, y

# ----- Create numpy array with square dimensions and 8-bit color values
data = np.zeros((y, x, 3), dtype=np.uint8)

# ----- Convert sequence into color values
pos = 0
line = 0

while line < y:
    while pos < x:
        if seq[(line) * x + pos] == 'A':
            col = colA
        elif seq[(line) * x + pos] == 'T':
            col = colT
        elif seq[(line) * x + pos] == 'G':
            col = colG
        elif seq[(line) * x + pos] == 'C':
            col = colC
        else:
            col = colDefault
        data[line, pos] = col
        pos += 1
    pos = 0
    line += 1

# ----- Resample array as needed (for larger images)
# Resample by a factor of 2 with nearest interpolation:
# scipy.ndimage.zoom(x, 2, order=0)
# ... with bilinear interpolation: order=1
# ... with cubic interpolation: order=3
# do not zoom along the z-axis -> (2,2,1)
data2 = scipy.ndimage.zoom(data, (2, 2, 1), order=0)
# data2 = scipy.ndimage.zoom(data2, (6, 6, 1), order=0)
# data2 = scipy.ndimage.zoom(data2, (2, 2, 1), order=0)

# ----- Save image
bild = toimage(data2)
# bild.show()
bild = imsave(filename + '.png', data2)
