from typing import List

from parser_constants import *


grammer_rules: List[GRAMMER_RULE] = [
    (NonTerminal.E, [NonTerminal.T, NonTerminal.X]),
    (NonTerminal.X, [Terminal.PLUS, NonTerminal.E]),
    (NonTerminal.X, [EPSILON]),
    (NonTerminal.T, [Terminal.PARAENTHESIS_OPEN, NonTerminal.E, Terminal.PARAENTHESIS_CLOSE]),
    (NonTerminal.T, [Terminal.INT, NonTerminal.Y]),
    (NonTerminal.Y, [Terminal.TIMES, NonTerminal.T]),
    (NonTerminal.Y, [EPSILON]),
]
