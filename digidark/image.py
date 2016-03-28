from digidark.mathf import bilerp

import cv2
import numpy

class Image:

    def __init__(self, pixels=None, sampling='none'):
        self.pixels = pixels
        self.sampling = sampling
        (self.height, self.width) = self.shape()

    def __getitem__(self, pidx):
        (j, i) = pidx
        i = max(0, min(i, self.height - 1))
        j = max(0, min(j, self.width - 1))

        if self.sampling == 'none':
            return self.pixels[i][j]
        else:
            return bilerp(self.pixels, i, j)

    def __setitem__(self, pidx, pval):
        (j, i) = pidx
        i = max(0, min(i, self.height - 1))
        j = max(0, min(j, self.width - 1))

        self.pixels[i][j] = pval

    def read(self, filename):
        self.pixels = cv2.imread(filename)
        (self.height, self.width) = self.shape()

    def write(self, filename):
        cv2.imwrite(filename, self.pixels)

    def show(self, win_name):
        cv2.imshow(win_name, self.pixels)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def shape(self):
        if self.pixels == None:
            return (0, 0)

        return self.pixels.shape[0:-1]

    def resize(self, height, width):
        resized = numpy.ndarray(dtype='uint8', shape=(height, width, 3))

        sy = self.height / height
        sx = self.width / width

        for i in range(height):
            for j in range(width):
                if self.sampling == 'none':
                    resized[i][j] = self.pixels[i * sy][j * sx]
                else:
                    resized[i][j] = bilerp(self.pixels,
                                           (i + 0.5) * sy, (j + 0.5) * sx)

        return Image(resized, self.sampling)

    def scale(self, factor):
        return self.resize(int(self.height * factor),
                           int(self.width * factor))

