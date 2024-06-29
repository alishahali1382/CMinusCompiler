# 400109905 - Ali Shahali
# 400109287 - Arefe Boushehrian

import sys

from parser_constants import grammar_rules
from prd_parser import Parser

sys.setrecursionlimit(1000)

parser = Parser(grammar_rules)
parser.parse_and_write()

print("\n")
for i, line in enumerate(parser.codegen.PB):
    if line != None:
        print(f"{i}\t({', '.join((str(x) if x is not None else ' ') for x in line)} )")