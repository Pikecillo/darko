from digidark.mathf import bilerp

import cv2

class Image:

    def __init__(self, pixels=None, sampling='none'):
        self.sampling = sampling
        self.pixels = pixels
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
