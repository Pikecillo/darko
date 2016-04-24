import cProfile
import sys

sys.path.append('..')

import digidark.interpreter

def benchmarks_none():
    ddi = digidark.interpreter.Interpreter()
    
    ddi.load('../docs/images/feynman.jpg', sampling='none')
    
    ddi.eval('new[x, y] = old[rect(r / 2, a)]')
    ddi.eval('new[x, y] = old[rect(r, a + rad(45))]')

def benchmarks_bilerp():
    ddi = digidark.interpreter.Interpreter()
    
    ddi.load('../docs/images/feynman.jpg', sampling='bilinear')

    ddi.eval('new[x, y] = old[rect(r / 2, a)]')
    ddi.eval('new[x, y] = old[rect(r, a + rad(45))]')

if __name__ == '__main__':
    cProfile.run('benchmarks_none()')
    cProfile.run('benchmarks_bilerp()')
