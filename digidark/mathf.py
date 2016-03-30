import cmath
import math
from numpy import float32, uint8

"""
Convert from rectangular coordinates to polar

polar(x, y) -> (r, a)

x: x rectangular component
y: y rectangular component
r: polar module
a: polar angle
"""
def polar(x, y):
    return cmath.polar(complex(x, y))

def rect(r, a):
    z = cmath.rect(r, a)
    return (z.real, z.imag)

"""
Convert from radians to degrees

deg(rads) -> degs

rads: Angle in radians
degs: Angle in degrees
"""
def deg(rads):
    return rads / math.pi * 180.0

"""
Convert from degrees to radians

rad(degs) -> rads

degs: Angle in degrees
rads: Angle in radians
"""
def rad(degs):
    return degs / 180.0 * math.pi

"""
Bilinear interpolation
"""
def bilerp(img, y, x):
    (height, width) = img.shape[:-1]
    i = max(0.5, min(height - 1.5, float(y)))
    j = max(0.5, min(width - 1.5, float(x)))
    c0 = float32(img[i - 0.5][j - 0.5])
    c1 = float32(img[i - 0.5][j + 0.5])
    c2 = float32(img[i + 0.5][j - 0.5])
    c3 = float32(img[i + 0.5][j + 0.5])

    s = j + 0.5 - math.ceil(j - 0.5)
    t = i + 0.5 - math.ceil(i - 0.5)

    return uint8((c0 * (1.0 - s) + c1 * s) * (1.0 - t) +
                 (c2 * (1.0 - s) + c3 * s) * t)

"""
Pixel average
"""
def gray(pixel):
    return float32(pixel).sum() / pixel.size
