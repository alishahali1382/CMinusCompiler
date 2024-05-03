import enum
from typing import List, Tuple, Union

__all__ = ['NonTerminal', 'Terminal', 'GRAMMAR_RHS', 'GRAMMAR_RULE', 'EPSILON', 'EOF', 'grammar_rules']

class NonTerminal(enum.Enum):
    E = 'E'
    T = 'T'
    X = 'X'
    Y = 'Y'

    def __str__(self):
        return self.value

    def __repr__(self):
        return rf"'{self.value}'"

class Terminal(enum.Enum):
    EPSILON = 'EPSILON'
    EOF = '$'
    PARAENTHESIS_OPEN = '('
    PARAENTHESIS_CLOSE = ')'
    PLUS = '+'
    TIMES = '*'
    INT = 'int'

    def __str__(self):
        return self.value

    def __repr__(self):
        return rf"'{self.value}'"

GRAMMAR_RHS = List[Union[NonTerminal, Terminal]]
GRAMMAR_RULE = Tuple[NonTerminal, GRAMMAR_RHS]
EPSILON = Terminal.EPSILON
EOF = Terminal.EOF


grammar_rules: List[GRAMMAR_RULE] = [
    (NonTerminal.E, [NonTerminal.T, NonTerminal.X]),
    (NonTerminal.X, [Terminal.PLUS, NonTerminal.E]),
    (NonTerminal.X, [EPSILON]),
    (NonTerminal.T, [Terminal.PARAENTHESIS_OPEN, NonTerminal.E, Terminal.PARAENTHESIS_CLOSE]),
    (NonTerminal.T, [Terminal.INT, NonTerminal.Y]),
    (NonTerminal.Y, [Terminal.TIMES, NonTerminal.T]),
    (NonTerminal.Y, [EPSILON]),
]
