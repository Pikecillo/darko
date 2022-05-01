import sys

sys.path.append('..')

import darko.interpreter

ddi = darko.interpreter.Interpreter()

ddi.load('../docs/images/feynman.jpg', sampling='bilinear')

ddi.eval('new[x, y] = old[rect(r / 2, a)]')
ddi.save('../docs/images/feynman-zoomed.jpg')

ddi.eval('new[x, y] = old[rect(r, a + rad(45))]')
ddi.save('../docs/images/feynman-rotated.jpg')

ddi.eval('new[x, y] = old[abs(X / 2 - x), y]')
ddi.save('../docs/images/feynman-mirrored.jpg')

transformation = """
new[x, y] =
    0.33 * ((gray(Z - old[x - 25, y]) / Z) * rgb(0, 0, 255)) +
    0.33 * ((gray(Z - old[x, y]) / Z) * rgb(0, 255, 0)) +
    0.33 * ((gray(Z - old[x + 25, y]) / Z) * rgb(255, 0, 0))
"""
ddi.eval(transformation)
ddi.save('../docs/images/feynman-lsd.jpg')

transformation = """
new[x, y] =
    old[x % (X / 2) * 2, y % (Y / 2) * 2] *
        ((x < X / 2 ?
            (y < Y / 2 ? rgb(255, 0, 0) : rgb(0, 255, 0)) :
            (y < Y / 2 ? rgb(255, 255, 0) : rgb(0, 255, 255))) / Z)
"""
ddi.eval(transformation)
ddi.save('../docs/images/feynman-mosaic.jpg')

transformation = """
new[x, y] = gray(old[floor(x / 2) * 2, floor(y / 2) * 2]) > 150 ?
    rgb(255, 255, 255) : rgb(0, 0, 0)
"""
ddi.eval(transformation)
ddi.save('../docs/images/feynman-icon.jpg')
