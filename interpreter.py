import cv2
import numpy
import re

"""
Lexical analyzer
"""
class Lexer:
    Identifier =  1
    IntegerLit =  2
    BinaryOp   =  3
    Assignment = 4
    OpenBra    =  5
    CloseBra   =  6
    OpenPar    =  7
    ClosePar   =  8
    Comma      =  9
    Filename   =  10
    End        = 11
    Unknown    = 12

    token_type = {
        1:  Identifier,
        2:  IntegerLit,
        3:  BinaryOp,
        4: Assignment,
        5:  OpenBra,
        6:  CloseBra,
        7:  OpenPar,
        8:  ClosePar,
        9:  Comma,
        10:  Filename,
        11: End,
        12: Unknown
    }

    def __init__(self):
        lexems = r"""\s*(?:
          ([_a-zA-Z]+[_\w]*) # Identifier
        | (\d+)              # Integer literal
        | ([+\-*/])         # Binary operator
        | (=)
        | ([\[])             # Opening bracket
        | ([\]])             # Closing bracket
        | ([\(])             # Opening parenthesis
        | ([\)])             # Closing parenthesis
        | (,)                # Comma
        | '(\w+\.\w+)'       # Filename
        | ($)                # End
        | (.+?)              # Unknown
        )"""

        self.compiled_re = re.compile(lexems, re.VERBOSE)

    def tokenize(self, command):
        self.scan = self.compiled_re.scanner(command)

    def next_token(self):
        token = self.scan.match()

        if not token:
            return None
        else:
            return (Lexer.token_type[token.lastindex],
                    token.group(token.lastindex))

class Parser:

    def __init__(self, interpreter):
        self.lexer = Lexer()
        self.interpreter = interpreter

    def match(self, token_type):
        token = self.lexer.next_token()

        print "Matching " + str(token_type) + " " + str(token)

        if token_type == Lexer.End:
            if token[0] == token_type:
                return True
            else:
                print "Error - too many arguments"
                return False

        if token[0] != token_type:
            print "Mismatched token " + str(token[1])
            return None

        return token[1]

    def parse_command(self, command):
        self.lexer.tokenize(command)

        identifier = self.match(Lexer.Identifier)

        if not identifier:
            print "Error - unrecognized command"
        else:
            if identifier == 'q':
                return False
            elif identifier == 'c':
                self.parse_create_command()
            elif identifier == 'r':
                self.parse_read_command()
            elif identifier == 'w':
                self.parse_write_command()
            else:
                self.parse_transformation()

        return True

    def parse_create_command(self):
        X = self.match(Lexer.IntegerLit)

        if X:
            Y = self.match(Lexer.IntegerLit)

            if Y:
                if self.match(Lexer.End):
                    self.interpreter.create_image(int(X), int(Y))
            else:
                print "Error - invalid Y dimension"

        else:
            print "Error - invalid X dimension"

    def parse_read_command(self):
        filename = self.match(Lexer.Filename)

        if filename and self.match(Lexer.End):
            self.interpreter.read_file(filename)
    
    def parse_write_command(self):
        filename = self.match(Lexer.Filename)

        if filename and self.match(Lexer.End):
            self.interpreter.write_file(filename)

    def parse_transformation(self):
        lhs = 'new[y][x]'

        if self.match(Lexer.Assignment):
            rhs = self.parse_rhs()

            if rhs:
                self.interpreter.transform(lhs, rhs)
        else:
            print "Error - invalid transformation"

    def parse_lhs(self):
        identifier = self.match(Lexer.Identifier)
        print identifier
        if identifier == 'new':
            return 'new[y][x]'

    def parse_rhs(self):
        return 'Z - old[y][x] * 0.5'

class Interpreter:

    def __init__(self):
        self.parser = Parser(self)
        self.new = None
        self.old = None

    def execute(self, command):
        return self.parser.parse_command(command)

    def create_image(self, X, Y):
        self.old = numpy.zeros(dtype='uint8', shape=(Y, X, 3))
        self.new = numpy.zeros_like(self.old)

    def read_file(self, filename):
        self.old = cv2.imread(filename)
        self.new = numpy.zeros_like(self.old)

    def write_file(self, filename):
        cv2.imwrite(filename, self.new)

    def transform(self, lhs, rhs):
        (Y, X) = self.old.shape[0:-1]
        Z = 255

        statement = lhs + '=' + rhs

        print statement

        for y in range(Y):
            for x in range(X):
                locals = {
                    "new": self.new,
                    "old": self.old,
                    "x": x,
                    "y": y,
                    "X": X,
                    "Y": Y,
                    "Z": Z
                }

                exec(statement, {}, locals)

if __name__ == '__main__':
    program = [
        'c 256 512',
        'w \'img1.jpg\'',
        'r \'icon.jpg\'',
        'new = Z - old',
        'w \'img2.jpg\'',
        'q'
    ]
    command = 0
    interpreter = Interpreter()

    while interpreter.execute(program[command]):
        print "Parsing " + program[command]
        command = command + 1
