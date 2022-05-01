import cProfile
import sys

sys.path.append('..')

import darko.interpreter

def benchmarks_none():
    darko_interpreter = darko.interpreter.Interpreter()
    
    darko_interpreter.load('../docs/images/feynman.jpg', sampling='none')
    
    darko_interpreter.eval('new[x, y] = old[rect(r / 2, a)]')
    darko_interpreter.eval('new[x, y] = old[rect(r, a + rad(45))]')

def benchmarks_bilerp():
    darko_interpreter = darko.interpreter.Interpreter()
    
    darko_interpreter.load('../docs/images/feynman.jpg', sampling='bilinear')

    darko_interpreter.eval('new[x, y] = old[rect(r / 2, a)]')
    darko_interpreter.eval('new[x, y] = old[rect(r, a + rad(45))]')

if __name__ == '__main__':
    cProfile.run('benchmarks_none()')
    cProfile.run('benchmarks_bilerp()')
