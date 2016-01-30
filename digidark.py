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

def intensity(pixel):
    return numpy.float32(pixel).sum(axis=0) / 3

def bath(img, i, j, stripe=16):
    oldj = j + (j % stripe) - stripe
    width = img.shape[1]

    if oldj >= 0 and oldj < width:
        return img[i][oldj]
    else:
        return img[i][j]

def twist(img, i, j, spin=3.0, radius=4.0):
    height = img.shape[0]
    width = img.shape[1]
    R = math.sqrt((width ** 2 + height ** 2) / radius)
    x = j - 0.5 * width;
    y = i - 0.5 * height;

    (r, p) = to_polar(x, y);
    (x, y) = to_rect(r, p + spin * r / R);
  
    x = x + 0.5 * width + 0.5;
    y = y + 0.5 * height + 0.5;

    if x >= 0 and y >= 0 and x < width and y < height:
        return img[y][x]

    return numpy.array([0, 0, 0])

def fisheye(img, i, j):
    height = img.shape[0]
    width = img.shape[1]
    R = math.sqrt((width ** 2 + height ** 2) / 4.0);
    x = j - 0.5 * width;
    y = i - 0.5 * height;

    (r, p) = to_polar(x, y);
    (x, y) = to_rect(1.5 * r * r / R, p);
  
    x = x + 0.5 * width + 0.5;
    y = y + 0.5 * height + 0.5;

    if x >= 0 and y >= 0 and x < width and y < height:
        return img[y][x]

    return numpy.array([0, 0, 0])

def spiralbath(img, i, j):
    width = img.shape[1]
    height = img.shape[0]

    x = j - 0.5 * width
    y = i - 0.5 * height

    (r, p) = to_polar(x, y)
 
    x = x + 0.5 * width + 0.5
    y = y + 0.5 * height + 0.5

    oldj = j + ((int)(to_degrees(p) + r / 4) % 64) - 16;

    if oldj >= 0 and oldj < width:
        return img[i][oldj]

    return img[i][j]

def funhouse(img, i, j):
    width = img.shape[1]
    height = img.shape[0]
    C1 = 1.18
    C2 = 150
    C3 = 89

    y = i + math.sin(to_radians(i * C1)) * C3;
    x = j + math.sin(to_radians(j)) * C2;

    if x >= 0 and y >= 0 and x < width and y < height:
        return img[y][x]

def hippie(img, i, j):
    factor = 128 - (j - 128) ** 2 - (i - 128) ** 2
    pixel = numpy.uint32(img[i][j])

    return numpy.uint8(pixel ^ (pixel * factor) >> 25)

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
  
    print (i, j)

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

    R = math.sqrt(width ** 2 + height ** 2) / 2
    x = j - 0.5 * width
    y = i - 0.5 * height

    (r, p) = to_polar(x, y)
    (x, y) = to_rect(0.5 * math.sqrt(r * R), p)
  
    x = x + 0.5 * width + 0.5
    y = y + 0.5 * height + 0.5

    if x >= 0 and y >= 0 and x < width and y < height:
        return img[y][x]
    
    return numpy.array([0, 0, 0])

def transform(source_img, func, *args):
    transformed_img = numpy.empty_like(source_img)
    shape = source_img.shape

    for i in range(shape[0]):
        for j in range(shape[1]):
            if func in [bentley, melt, oil]:
                func(source_img, transformed_img, i, j, *args)
            else:
                transformed_img[i][j] = func(source_img, i, j, *args)

    return transformed_img

if __name__ == '__main__':
    func_map = {
        bath: (24,),
        twist: (6.0, 2.0),
        fisheye: None,
        spiralbath: None,
        funhouse: None,
        hippie: None,
        indian: None,
        caricature: None,
        bentley: None,
        oil: None,
        melt: None,
    }
    func = bath

    source = cv2.imread('the_bride.jpg')
    
    if func_map[func]:
        transformed = transform(source, func, *func_map[func])
    else:
        transformed = transform(source, func)
        
    cv2.imshow('Source', source)
    cv2.imshow('Transformed', transformed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
