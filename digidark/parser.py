from simpleparse.parser import Parser
from simpleparse.dispatchprocessor import DispatchProcessor, dispatchList, getString

grammar = """

root := transformation

transformation := ( name, index, assign, expr )

assign := '='

expr := ( trinary )
        / ( term )

trinary := ( term, '?', term, ':', term )

term := ( factor, binaryop, term )
      / ( factor )

binaryop := '**' / '/' / '%' / '+' / '-' / '>' / '<' / '=='
          / '<=' / '>=' / '!=' / '*' / '&&' / '||'

unaryop := '-' / '!'

factor := ( opar, expr, cpar )
        / ( unaryop, factor )
        / ( name, index )
        / ( function )
        / ( name )
        / ( number )

function := ( name, opar, parameters, cpar )

parameters := ( expr, ',', parameters )
            / ( expr )

opar := '('

cpar := ')'

name := [_a-zA-Z], [_a-zA-Z0-9]*

number := ( float )
        / ( integer )

integer := [0-9]+

float := ( integer, '.', integer )

index := ( '[', expr, ',', expr, ']' )
       / ( '[', function, ']' ) 

"""

def test_grammar():
    cases = {
        "trans" : [ ("Z-old", True),
                    ("old=Z-old", False),
                    ("Z*log(old)/log(Z)", True),
                    ("old>Z/2?Z-old:old", True),
                    ("x>y/5&&y/5>0?old[x*5,y*5]:0", True),
                    ("new=old[x+y,x]", True),
                    ("new[x,y]=Z-old", True),
                    ("", False) ],
        "fileref" : [ ("$1", True),
                      ("x0", True),
                      ("$10a", False),
                      ("$0000", False),
                      ("", False) ],
        "number" : [ ("1000", True),
                     ("afd", False),
                     ("", False) ],
        "name" : [ ("_0", True),
                   ("", False) ],
        "value" : [ ("9", True),
                    ("900", True),
                    ("0000", True),
                    ("", False),
                    ("x9", False),
                    ("", False) ],
        "index" : [ ("[6,9]", True),
                    ("6+9", False),
                    ("[6+9,1]", True),
                    ("[x+y,8]", True),
                    ("", False) ]
    }

    cases2 = {
        "transformation" : [ ('new[x,y]=avg(old[floor(x/10)* 10,floor(y/10)*10])>100?rgb(255, 255, 255):rgb(0, 0, 0)', True),
        ('new[x, y] = Z - old[x, y]', True),
        ('new[x, y] = old[X - x, y]', True),
        ('new[x, y] = old[x + (x % 32) - 16, y]', True),
        ('new[x, y - gray(old[x, y]) * 0.1] = old[x, y]', True),
        ('new[x, y] = old[rect(r, a + rad(180))]', True),
        ('new[x, y] = old[rect(r, a - r / 50)]', True),
        ('new[x, y] = old[rect(1.5 * r ** 2 / R, a)]', True),
        ('new[x, y] = old[rect(0.5 * sqrt(r * R), a)]', True),
        ('new[x, y] = old[x + sin(rad(x)) * 150, y + sin(rad(y * 1.18)) * 89]', True),
        ('new[x, y] = old[x, y + (deg(a) + r / 4) % 64 - 16]', True),
        ('new[x, y] = old[x, y + 10 * sin(rad(y) * 10)]', True),
        ('new[x, y] = old[x + 10 * sin(rad(y) * 5), y + 10 * sin(rad(x) * 5)]', True),
        ('new[x, y] = old[x + 10 * sin(rad(y) * 10), y]', True),
        ('new[x, y] = old[rect(r + 10 * sin(rad(r) * 10), a - r / 50)]', True),
        ('new[x, y] = old[rect(1.5 * r ** 2 / R + 10 * sin(rad(r) * 10), a)]', True),
        ('new[x, y] = old[floor(x / 10) * 10, floor(y / 10) * 10]', True)]
    }

    parser = Parser(grammar)
    
    for production in cases2.keys():
        for case in cases2[production]:
            tsrc = case[0].replace(" ", "")
            success, children, nextchar = parser.parse(tsrc, production=production)
            if (success and nextchar == len(tsrc)) == case[1]:
                print "Test passed: ", production, tsrc
            else:
                print "Test failed: ", production, tsrc, nextchar
                print tsrc
                print " " * nextchar, '^'

class SyntaxTreeProcessor(DispatchProcessor):

    def transformation(self, info, buffer):
        (tag, left, right, children) = info
        res = dispatchList(self, children, buffer)
        return " ".join(res)

    def assign(self, info, buffer):
        return getString(info, buffer)

    def expr(self, info, buffer):
        (tag, left, right, children) = info
        res = dispatchList(self, children, buffer)
        return " ".join(res)

    def trinary(self, info, buffer):
        (tag, left, right, children) = info
        ret = dispatchList(self, children, buffer)
        return "%s if %s else %s" % (ret[1], ret[0], ret[2])

    def term(self, info, buffer):
        (tag, left, right, children) = info
        res = dispatchList(self, children, buffer)
        return " ".join(res)

    def binaryop(self, info, buffer):
        return getString(info, buffer)

    def factor(self, info, buffer):
        (tag, left, right, children) = info
        res = dispatchList(self, children, buffer)
        return " ".join(res)

    def function(self, info, buffer):
        (tag, left, right, children) = info
        res = dispatchList(self, children, buffer)
        return " ".join(res)

    def parameters(self, info, buffer):
        (tag, left, right, children) = info
        res = dispatchList(self, children, buffer)
        return ", ".join(res)

    def opar(self, info, buffer):
        return getString(info, buffer)

    def cpar(self, info, buffer):
        return getString(info, buffer)

    def number(self, info, buffer):
        (tag, left, right, children) = info
        res = dispatchList(self, children, buffer)
        return "".join(res)

    def integer(self, info, buffer):
        return getString(info, buffer)

    def float(self, info, buffer):
        (tag, left, right, children) = info
        res = dispatchList(self, children, buffer)
        return ".".join(res)

    def name(self, info, buffer):
        return getString(info, buffer)

    def value(self, info, buffer):
        return getString(info, buffer)

    def index(self, info, buffer):
        (tag, left, right, children) = info
        ret = dispatchList(self, children, buffer)
        if len(ret) == 2:
            return "[%s, %s]" % tuple(ret)
        else:
            return "[%s]" % tuple(ret)

class Compiler:

    def __init__(self):
        self.parser = Parser(grammar)
        self.translator = SyntaxTreeProcessor()

    def compile(self, command):
        cmd = command.replace(" ", "")
        (success, children, nextchar) = self.parser.parse(cmd)
        result = self.translator((success, children, nextchar), cmd)
        python_src = result[1][0]

        return compile(python_src, '', 'exec')

