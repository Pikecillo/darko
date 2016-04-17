from digidark.mathf import bilerp

import cv2
import numpy as np
import math

class Image:

    def __init__(self, pixels=None, sampling='none'):
        self.pixels = pixels
        self.sampling = sampling
        (self.height, self.width) = self.shape()

    """
    pidx: pixel coordinate (x, y)
    """
    def __getitem__(self, pidx):
        (x, y) = pidx

        if self.sampling == 'none':
            x = max(0, min(x, self.width - 1))
            y = max(0, min(y, self.height - 1))
            return self.pixels[y][x]
        else:
            return self.bilerp_sampling(x, y)

    def __setitem__(self, pidx, pval):
        (x, y) = pidx
        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.height - 1))

        self.pixels[y][x] = pval

    def bilerp_sampling(self, x, y):
        i0 = int(max(0, min(self.height - 1, y)))
        j0 = int(max(0, min(self.width - 1, x)))
        i1 = int(max(0, min(self.height - 1, y + 1)))
        j1 = int(max(0, min(self.width - 1, x + 1)))

        c0 = np.float32(self.pixels[i0][j0])
        c1 = np.float32(self.pixels[i0][j1])
        c2 = np.float32(self.pixels[i1][j0])
        c3 = np.float32(self.pixels[i1][j1])

        s = x - math.floor(x)
        t = y - math.floor(y)

        return np.uint8(bilerp(c0, c1, c2, c3, s, t))

    def read(self, filename):
        self.pixels = cv2.imread(filename)
        (self.height, self.width) = self.shape()

    def write(self, filename):
        cv2.imwrite(filename, self.pixels)

    def show(self, win_name):
        cv2.imshow(win_name, self.pixels)

    def shape(self):
        if self.pixels == None:
            return (0, 0)

        return self.pixels.shape[0:-1]

    def resized(self, height, width, sampling='none'):
        resized = np.ndarray(dtype='uint8', shape=(height, width, 3))

        sy = float(self.height / height)
        sx = float(self.width / width)

        for i in range(height):
            for j in range(width):
                if self.sampling == 'none':
                    resized[i][j] = self.pixels[i * sy][j * sx]
                else:
                    resized[i][j] = self.bilerp_sampling(j * sx, i * sy)

        return Image(resized, self.sampling)

    def scaled(self, factor):
        return self.resized(int(self.height * factor),
                            int(self.width * factor))
