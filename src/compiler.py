# 400109905 - Ali Shahali
# 400109287 - Arefe Boushehrian

import anytree

from parser_constants import grammar_rules
from prd_parser import Parser

parser = Parser(grammar_rules)
node = parser.parse()
print(anytree.RenderTree(node).by_attr())
