from simpleparse.parser import Parser

# Popi grammar rules as defined in Beyond Photography
popi_grammar = """

trans := ( 'new', index, '=', expr )
       / ( 'new', '=', expr )
       / expr

expr := ( term, '?', expr, ':', expr )
      / ( term )

term := ( factor, binaryop, term )
      / ( factor )

binaryop := '*' / '/' / '%' / '+' / '-' / '>' / '=='
          / '<=' / '>=' / '!=' / '^' / '&&' / '||'

factor := ( '(', expr, ')' )
        / ( '-', factor )
        / ( '!', factor )
        / ( name, index )
        / ( name, '(', expr, ')' )
        / ( name )
        / ( fileref )
        / ( value )

fileref := ( '$', number, index )
         / ( '$', number )
         / ( name )

number := [1-9], [0-9]*

name := [_a-zA-Z], [_a-zA-Z0-9]*

value := [0-9]+

index := '[', expr, ',', expr, ']'

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
        "fileref" : [ ("$1", True), ("x0", True), ("$10a", False),
                      ("$0000", False), ("", False) ],
        "number" : [ ("1000", True), ("afd", False), ("", False) ],
        "name" : [ ("_0", True), ("", False) ],
        "value" : [ ("9", True), ("900", True), ("0000", True),
                    ("", False), ("x9", False), ("", False) ],
        "index" : [ ("[6,9]", True), ("6+9", False), ("[6+9,1]", True),
                    ("[x+y,8]", True), ("", False) ]
    }

    parser = Parser(popi_grammar)
    
    for production in cases.keys():
        for case in cases[production]:
            success, children, nextchar = parser.parse(
                case[0], production=production)
            if (success and nextchar == len(case[0])) == case[1]:
                print "Test passed: ", production, case, nextchar
            else:
                print "Test failed: ", production, case, nextchar

test_grammar()
