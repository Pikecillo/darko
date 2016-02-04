#!/usr/bin/python

import cv2
import math
import cmath
import numpy
import random

def to_polar(x, y):
    return cmath.polar(complex(x, y))

def to_rect(r, p):
    z = cmath.rect(r, p)
    return (z.real, z.imag)

def to_degrees(rad):
    return rad / math.pi * 180.0

def to_radians(deg):
    return deg / 180.0 * math.pi

def lerp(v0, v1, t):
    return v0 * (1.0 - t) + v1 * t

def bilerp(img, y, x):
    (height, width) = img.shape[:-1]
    i = max(0.5, min(height - 1.5, float(y)))
    j = max(0.5, min(width - 1.5, float(x)))
    c0 = numpy.float32(img[i - 0.5][j - 0.5])
    c1 = numpy.float32(img[i - 0.5][j + 0.5])
    c2 = numpy.float32(img[i + 0.5][j - 0.5])
    c3 = numpy.float32(img[i + 0.5][j + 0.5])

    s = j + 0.5 - math.ceil(j - 0.5)
    t = i + 0.5 - math.ceil(i - 0.5)

    return numpy.uint8(lerp(lerp(c0, c1, s), lerp(c2, c3, s), t))

def intensity(pixel):
    return numpy.float32(pixel).sum() / pixel.size

def bath(img, i, j, stripe=16):
    width = img.shape[1]
    x = max(0, min(j + (j % stripe) - stripe, width - 1))

    return img[i][x]

def twist(img, i, j, spin=3.0, radius=4.0):
    (height, width) = img.shape[:-1]
    R = math.sqrt((width ** 2 + height ** 2) / radius)

    half_width = 0.5 * width
    half_height = 0.5 * height

    (r, p) = to_polar(j - half_width, i - half_height)
    (x, y) = to_rect(r, p + spin * r / R);

    x = max(0.0, min(x + half_width, width - 1.0))
    y = max(0.0, min(y + half_height, height - 1.0))

    return bilerp(img, y, x)

def fisheye(img, i, j):
    (height, width) = img.shape[:-1]
    R = math.sqrt((width ** 2 + height ** 2) / 4.0)

    half_width = 0.5 * width
    half_height = 0.5 * height

    (r, p) = to_polar(j - half_width, i - half_height);
    (x, y) = to_rect(1.5 * r ** 2 / R, p);
  
    x = max(0, min(x + half_width, width - 1))
    y = max(0, min(y + half_height, height - 1))

    return bilerp(img, y, x)

def spiralbath(img, i, j):
    (height, width) = img.shape[:-1]

    (r, p) = to_polar(j - 0.5 * width, i - 0.5 * height)

    x = max(0, min(j + ((int)(to_degrees(p) + r / 4) % 64) - 16, width - 1))

    return bilerp(img, i, x)

def funhouse(img, i, j):
    (height, width) = img.shape[:-1]
    C1 = 1.18
    C2 = 150
    C3 = 89

    y = max(0, min(i + math.sin(to_radians(i * C1)) * C3, height - 1))
    x = max(0, min(j + math.sin(to_radians(float(j))) * C2, width - 1))

    return bilerp(img, y, x)

def hippie(img, i, j):
    factor = 128 - (j - 128) ** 2 - (i - 128) ** 2
    pixel = numpy.uint32(img[i][j])

    return numpy.uint8(pixel ^ (pixel * factor) >> 17)

def indian(img, i, j):
    width = img.shape[1]
    height = img.shape[2] 
    factor = 128 - (j - 128) ** 2 - (i - 128) ** 2

    old_pixel = numpy.uint32(img[i][j]);
    new_pixel = old_pixel ^ (old_pixel * factor) >> 25
  
    k = 0.01
    b = 1 / (1 + math.exp(-2 * k * (j - 0.5 * width)))
    c = 1 / (1 + math.exp(-2 * k * (j - 0.5 * width)))

    new_pixel = (b - 1) * c * new_pixel + b * (1 - c) * old_pixel

    return numpy.uint8(new_pixel)

def bentley(src_img, tar_img, i, j):
    height = src_img.shape[0]

    pixel = src_img[i][j];
    level = intensity(pixel);
  
    if(i + level / 4 < height):
        tar_img[i + level / 4][j] = pixel

def melt(src_img, tar_img, i, j):
    width = src_img.shape[1]
    height = src_img.shape[0]

    print (i, j)

    y = random.random() % (height - 1);
    x = random.random() % width;
    curr = tar_img[y][x]
    next = tar_img[y + 1][x]

    while y < height - 1 and intensity(curr) <= intensity(next):
        tar_img[y][x] = next
        tar_img[y + 1][x] = curr
        y = y + 1

        if y < height - 1:
            curr = tar_img[y][x]
            next = tar_img[y + 1][x]

def oil(src_img, tar_img, i, j):
    width = src_img.shape[1]
    height = src_img.shape[0]
    level = numpy.zeros(256)
    colors = numpy.array([[0, 0, 0] for w in range(256)])

    for y in range(i - 3, i + 4):
        for x in range(j - 3, j + 4):
            if x >= 0 and x < width and y >= 0 and y < height:
                pixel = src_img[y][x]
                lum = intensity(pixel)
                level[lum] = level[lum] + 1                
                colors[lum] = pixel;

    pixel = src_img[i][j]
    max_level = level.max();
    tar_img[i][j] = colors[max_level]

def caricature(img, i, j):
    width = img.shape[1]
    height = img.shape[0]

    half_width = 0.5 * width
    half_height = 0.5 * height

    R = math.sqrt(width ** 2 + height ** 2) / 2
    (r, p) = to_polar(j - half_width, i - half_height)
    (x, y) = to_rect(0.5 * math.sqrt(r * R), p)
  
    x = max(0, min(x + half_width, width - 1))
    y = max(0, min(y + half_height, height - 1))

    return bilerp(img, y, x)

def iconic(source_img, target_img, threshold=120, bsize=8):
    src_shape = source_img.shape

    bsize = min(src_shape[:-1]) / 48

    icon_shape = ((src_shape[0] + bsize - 1) / bsize,
                  (src_shape[1] + bsize - 1) / bsize)
    icon = numpy.ndarray(shape=icon_shape)

    for i in range(icon_shape[0]):
        for j in range(icon_shape[1]):
            iend = min((i + 1) * bsize, src_shape[0] - 1)
            jend = min((j + 1) * bsize, src_shape[0] - 1)

            block = source_img[i * bsize : iend, j * bsize : jend]
            intensity = block.sum() / block.size

            icon[i][j] = 255 if intensity > threshold else 0

    for i in range(src_shape[0]):
        for j in range(src_shape[1]):
            y = min(i / bsize, src_shape[0] - 1)
            x = min(j / bsize, src_shape[1] - 1)

            v = icon[y][x]
            target_img[i][j] = numpy.array([v, v, v])

def upsample(img, bi):
    (height, width) = img.shape[0:-1]
    upsampled = numpy.ndarray(dtype='uint8',
                              shape=(height * 2, width * 2, 3))

    for i in range(height * 2):
        for j in range(width * 2):
            if bi:
                upsampled[i][j] = bilerp(img, (i + 0.5) / 2.0,
                                         (j + 0.5) / 2.0)
            else:
                upsampled[i][j] = img[i / 2][j / 2]

    return upsampled

def transform(img, func, *args):
    transformed_img = numpy.empty_like(img)
    (height, width) = img.shape[0:-1]

    if func in [iconic]:
        func(img, transformed_img, *args)
    else:
        for i in range(height):
            for j in range(width):
                if func in [bentley, melt, oil]:
                    func(img, transformed_img, i, j, *args)
                else:
                    transformed_img[i][j] = func(img, i, j, *args)

    return transformed_img

if __name__ == '__main__':
    func_map = {
        bath: (24,),
        twist: (3.0, 4.0),
        fisheye: None,
        spiralbath: None,
        funhouse: None,
        hippie: None,
        indian: None,
        caricature: None,
        bentley: None,
        oil: None,
        melt: None,
        iconic: (120, 8)
    }
    func = caricature

    source = cv2.imread('images/me.jpg')

    if func_map[func]:
        transformed = transform(source, func, *func_map[func])
    else:
        transformed = transform(source, func)

    cv2.imshow('Source', source)
    cv2.imshow('Transformed', transformed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
