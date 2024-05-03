import enum
from typing import List, Tuple, Union

__all__ = ['NonTerminal', 'Terminal', 'GRAMMER_RHS', 'GRAMMER_RULE', 'EPSILON', 'EOF']

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

GRAMMER_RHS = List[Union[NonTerminal, Terminal]]
GRAMMER_RULE = Tuple[NonTerminal, GRAMMER_RHS]
EPSILON = Terminal.EPSILON
EOF = Terminal.EOF