#!/usr/bin/python

import darko.image as ddi
import darko.mathf as ddm
import darko.parser as ddp

import cv2
import math
import numpy

class Interpreter:
    
    def __init__(self):
        self.symbol_table = {
            'deg': ddm.deg,
            'rad': ddm.rad,
            'sqrt': math.sqrt,
            'floor': math.floor,
            'ceil': math.ceil,
            'sin': math.sin,
            'cos': math.cos,
            'abs': abs,
            'rgb': lambda r, g, b: numpy.array([b, g, r]),
            'gray': ddm.gray,
            'choice': lambda e, t, f: t if e else f,
            'old': ddi.Image()
        }
        self.compiler = ddp.Compiler()

    def load(self, filename, imgname='old', sampling='none', scaling=1.0):
        img = ddi.Image(sampling=sampling)
        img.read(filename)

        self.symbol_table[imgname] = img.scaled(scaling) 

    def save(self, filename, imgname='new'):
        self.symbol_table[imgname].write(filename)

    def show(self, winname='digi-dark', imgname='new'):
        self.symbol_table[imgname].show(winname)

    def wait(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def eval(self, transf_src):
        (height, width) = self.symbol_table['old'].shape()

        cx = 0.5 * width
        cy = 0.5 * height
        R = math.sqrt((width ** 2 + height ** 2) / 4.0)
        new = ddi.Image(numpy.zeros_like(self.symbol_table['old'].pixels),
                        'none')
        
        self.symbol_table['X'] = width
        self.symbol_table['Y'] = height
        self.symbol_table['Z'] = 255
        self.symbol_table['R'] = R
        self.symbol_table['cx'] = cx
        self.symbol_table['cy'] = cy
        self.symbol_table['new'] = new

        transf_code = self.compiler.compile(transf_src)

        for x in range(width):
            for y in range(height):
                (r, a) = ddm.polar(x - cx, y - cy)
                
                def shifted_rec(r, a):
                    p = ddm.rect(r, a)
                    return (p[0] + cx, p[1] + cy)
                    
                self.symbol_table['x'] = x
                self.symbol_table['y'] = y
                self.symbol_table['a'] = a
                self.symbol_table['r'] = r
                
                self.symbol_table['rect'] = shifted_rec

                eval(transf_code, {}, self.symbol_table)

        return new
