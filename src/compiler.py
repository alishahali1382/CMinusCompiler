# 400109905 - Ali Shahali
# 400109287 - Arefe Boushehrian

import sys

from parser_constants import grammar_rules
from prd_parser import Parser

sys.setrecursionlimit(1000)

parser = Parser(grammar_rules)
parser.parse_and_write()

print("\n")
with open("output.txt", "w") as f:
    lastline = -1
    for i, line in enumerate(parser.codegen.PB):
        if line != None:
            code = f"{i}\t({', '.join((str(x) if x is not None else ' ') for x in line)} )"
            #assert lastline == i-1, f"Line {i} is not in order, last line was {lastline}"
            code = "\n"*(i-lastline-1) + code
            lastline = i
            f.write(code + "\n")
            if parser.codegen.comment[i] != None:
                code = f"{code:<40}" #{parser.codegen.comment[i]}
            print(code)

with open("semantic_errors.txt", "w") as f:
    f.write("The input program is semantically correct.\n")
