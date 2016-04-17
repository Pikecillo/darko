from simpleparse.parser import Parser
from simpleparse.dispatchprocessor import *

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

