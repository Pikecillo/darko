import cmath
import math
from numpy import float32

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
Linear interpolation
"""
def lerp(v0, v1, t):
    return v0 * (1 - t) + v1 * t

"""
Bilinear interpolation
"""
def bilerp(v0, v1, v2, v3, s, t):
    return lerp(lerp(v0, v1, s), lerp(v2, v3, s), t)

"""
Pixel average
"""
def gray(pixel):
    return float32(pixel).sum() / pixel.size
