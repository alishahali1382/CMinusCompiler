import enum
from typing import List, Tuple, Union

__all__ = ['NonTerminal', 'Terminal', 'GRAMMAR_RHS', 'GRAMMAR_RULE', 'EPSILON', 'EOF', 'grammar_rules']

class NonTerminal(enum.Enum):
    Program = 'Program'
    Declaration_list = 'Declaration-list'
    Declaration = 'Declaration'
    Declaration_initial = 'Declaration-initial'
    Declaration_prime = 'Declaration-prime'
    Var_declaration_prime = 'Var-declaration-prime'
    Fun_declaration_prime = 'Fun-declaration-prime'
    Type_specifier = 'Type-specifier'
    Params = 'Params'
    Param_list = 'Param-list'
    Param = 'Param'
    Param_prime = 'Param-prime'
    Compound_stmt = 'Compound-stmt'
    Statement_list = 'Statement-list'
    Statement = 'Statement'
    Expression_stmt = 'Expression-stmt'
    Selection_stmt = 'Selection-stmt'
    Else_stmt = 'Else-stmt'
    Iteration_stmt = 'Iteration-stmt'
    Return_stmt = 'Return-stmt'
    Return_stmt_prime = 'Return-stmt-prime'
    Expression = 'Expression'
    B = 'B'
    H = 'H'
    Simple_expression_zegond = 'Simple-expression-zegond'
    Simple_expression_prime = 'Simple-expression-prime'
    C = 'C'
    Relop = 'Relop'
    Additive_expression = 'Additive-expression'
    Additive_expression_prime = 'Additive-expression-prime'
    Additive_expression_zegond = 'Additive-expression-zegond'
    D = 'D'
    Addop = 'Addop'
    Term = 'Term'
    Term_prime = 'Term-prime'
    Term_zegond = 'Term-zegond'
    G = 'G'
    Signed_factor = 'Signed-factor'
    Signed_factor_prime = 'Signed-factor-prime'
    Signed_factor_zegond = 'Signed-factor-zegond'
    Factor = 'Factor'
    Var_call_prime = 'Var-call-prime'
    Var_prime = 'Var-prime'
    Factor_prime = 'Factor-prime'
    Factor_zegond = 'Factor-zegond'
    Args = 'Args'
    Arg_list = 'Arg-list'
    Arg_list_prime = 'Arg-list-prime'

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
    MINUS = '-'
    STAR = '*'
    EQUAL = '='
    DOUBLE_EQUAL = '=='
    GREATER = '<'
    INT = 'int'
    ID = 'ID'
    NUM = 'NUM'
    SEMICOLON = ';'
    BRACKET_OPEN = '['
    BRACKET_CLOSE = ']'
    BRACE_OPEN = '{'
    BRACE_CLOSE = '}'
    VOID = 'void'
    COMMA = ','
    BREAK = 'break'
    IF = 'if'
    ENDIF = 'endif'
    ELSE = 'else'
    FOR = 'for'
    RETURN = 'return'

    def __str__(self):
        return self.value

    def __repr__(self):
        return rf"'{self.value}'"

    @staticmethod
    def from_str(s: str):
        for terminal in Terminal:
            if terminal.value == s:
                return terminal
        assert 0, f"Terminal with value {s} not found"

    @staticmethod
    def with_name(name: str):
        for terminal in Terminal:
            if terminal.name == name:
                return terminal
        assert 0, f"Terminal with name {name} not found"

GRAMMAR_RHS = List[Union[NonTerminal, Terminal]]
GRAMMAR_RULE = Tuple[NonTerminal, GRAMMAR_RHS]
EPSILON = Terminal.EPSILON
EOF = Terminal.EOF


grammar_rules: List[GRAMMAR_RULE] = [
    (NonTerminal.Program, [NonTerminal.Declaration_list, Terminal.EOF]),
    (NonTerminal.Declaration_list, [NonTerminal.Declaration, NonTerminal.Declaration_list]),
    (NonTerminal.Declaration_list, [Terminal.EPSILON]),
    (NonTerminal.Declaration, [NonTerminal.Declaration_initial, NonTerminal.Declaration_prime]),
    (NonTerminal.Declaration_initial, [NonTerminal.Type_specifier, Terminal.ID]),
    (NonTerminal.Declaration_prime, [NonTerminal.Fun_declaration_prime]),
    (NonTerminal.Declaration_prime, [NonTerminal.Var_declaration_prime]),
    (NonTerminal.Var_declaration_prime, [Terminal.SEMICOLON]),
    (NonTerminal.Var_declaration_prime, [Terminal.BRACKET_OPEN, Terminal.NUM, Terminal.BRACKET_CLOSE, Terminal.SEMICOLON]),
    (NonTerminal.Fun_declaration_prime, [Terminal.PARAENTHESIS_OPEN, NonTerminal.Params, Terminal.PARAENTHESIS_CLOSE, NonTerminal.Compound_stmt]),
    (NonTerminal.Type_specifier, [Terminal.INT]),
    (NonTerminal.Type_specifier, [Terminal.VOID]),
    (NonTerminal.Params, [Terminal.INT, Terminal.ID, NonTerminal.Param_prime, NonTerminal.Param_list]),
    (NonTerminal.Params, [Terminal.VOID]),
    (NonTerminal.Param_list, [Terminal.COMMA, NonTerminal.Param, NonTerminal.Param_list]),
    (NonTerminal.Param_list, [Terminal.EPSILON]),
    (NonTerminal.Param, [NonTerminal.Declaration_initial, NonTerminal.Param_prime]),
    (NonTerminal.Param_prime, [Terminal.BRACKET_OPEN, Terminal.BRACKET_CLOSE]),
    (NonTerminal.Param_prime, [Terminal.EPSILON]),
    (NonTerminal.Compound_stmt, [Terminal.BRACE_OPEN, NonTerminal.Declaration_list, NonTerminal.Statement_list, Terminal.BRACE_CLOSE]),
    (NonTerminal.Statement_list, [NonTerminal.Statement, NonTerminal.Statement_list]),
    (NonTerminal.Statement_list, [Terminal.EPSILON]),
    (NonTerminal.Statement, [NonTerminal.Expression_stmt]),
    (NonTerminal.Statement, [NonTerminal.Compound_stmt]),
    (NonTerminal.Statement, [NonTerminal.Selection_stmt]),
    (NonTerminal.Statement, [NonTerminal.Iteration_stmt]),
    (NonTerminal.Statement, [NonTerminal.Return_stmt]),
    (NonTerminal.Expression_stmt, [NonTerminal.Expression, Terminal.SEMICOLON]),
    (NonTerminal.Expression_stmt, [Terminal.BREAK, Terminal.SEMICOLON]),
    (NonTerminal.Expression_stmt, [Terminal.SEMICOLON]),
    (NonTerminal.Selection_stmt, [Terminal.IF, Terminal.PARAENTHESIS_OPEN, NonTerminal.Expression, Terminal.PARAENTHESIS_CLOSE, NonTerminal.Statement, NonTerminal.Else_stmt]),
    (NonTerminal.Else_stmt, [Terminal.ENDIF]),
    (NonTerminal.Else_stmt, [Terminal.ELSE, NonTerminal.Statement, Terminal.ENDIF]),
    (NonTerminal.Iteration_stmt, [Terminal.FOR, Terminal.PARAENTHESIS_OPEN, NonTerminal.Expression, Terminal.SEMICOLON, NonTerminal.Expression, Terminal.SEMICOLON, NonTerminal.Expression, Terminal.PARAENTHESIS_CLOSE, NonTerminal.Statement]),
    (NonTerminal.Return_stmt, [Terminal.RETURN, NonTerminal.Return_stmt_prime]),
    (NonTerminal.Return_stmt_prime, [Terminal.SEMICOLON]),
    (NonTerminal.Return_stmt_prime, [NonTerminal.Expression, Terminal.SEMICOLON]),
    (NonTerminal.Expression, [NonTerminal.Simple_expression_zegond]),
    (NonTerminal.Expression, [Terminal.ID, NonTerminal.B]),
    (NonTerminal.B, [Terminal.EQUAL, NonTerminal.Expression]),
    (NonTerminal.B, [Terminal.BRACKET_OPEN, NonTerminal.Expression, Terminal.BRACKET_CLOSE, NonTerminal.H]),
    (NonTerminal.B, [NonTerminal.Simple_expression_prime]),
    (NonTerminal.H, [Terminal.EQUAL, NonTerminal.Expression]),
    (NonTerminal.H, [NonTerminal.G, NonTerminal.D, NonTerminal.C]),
    (NonTerminal.Simple_expression_zegond, [NonTerminal.Additive_expression_zegond, NonTerminal.C]),
    (NonTerminal.Simple_expression_prime, [NonTerminal.Additive_expression_prime, NonTerminal.C]),
    (NonTerminal.C, [NonTerminal.Relop, NonTerminal.Additive_expression]),
    (NonTerminal.C, [Terminal.EPSILON]),
    (NonTerminal.Relop, [Terminal.GREATER]),
    (NonTerminal.Relop, [Terminal.DOUBLE_EQUAL]),
    (NonTerminal.Additive_expression, [NonTerminal.Term, NonTerminal.D]),
    (NonTerminal.Additive_expression_prime, [NonTerminal.Term_prime, NonTerminal.D]),
    (NonTerminal.Additive_expression_zegond, [NonTerminal.Term_zegond, NonTerminal.D]),
    (NonTerminal.D, [NonTerminal.Addop, NonTerminal.Term, NonTerminal.D]),
    (NonTerminal.D, [Terminal.EPSILON]),
    (NonTerminal.Addop, [Terminal.PLUS]),
    (NonTerminal.Addop, [Terminal.MINUS]),
    (NonTerminal.Term, [NonTerminal.Signed_factor, NonTerminal.G]),
    (NonTerminal.Term_prime, [NonTerminal.Signed_factor_prime, NonTerminal.G]),
    (NonTerminal.Term_zegond, [NonTerminal.Signed_factor_zegond, NonTerminal.G]),
    (NonTerminal.G, [Terminal.STAR, NonTerminal.Signed_factor, NonTerminal.G]),
    (NonTerminal.G, [Terminal.EPSILON]),
    (NonTerminal.Signed_factor, [Terminal.PLUS, NonTerminal.Factor]),
    (NonTerminal.Signed_factor, [Terminal.MINUS, NonTerminal.Factor]),
    (NonTerminal.Signed_factor, [NonTerminal.Factor]),
    (NonTerminal.Signed_factor_prime, [NonTerminal.Factor_prime]),
    (NonTerminal.Signed_factor_zegond, [Terminal.PLUS, NonTerminal.Factor]),
    (NonTerminal.Signed_factor_zegond, [Terminal.MINUS, NonTerminal.Factor]),
    (NonTerminal.Signed_factor_zegond, [NonTerminal.Factor_zegond]),
    (NonTerminal.Factor, [Terminal.PARAENTHESIS_OPEN, NonTerminal.Expression, Terminal.PARAENTHESIS_CLOSE]),
    (NonTerminal.Factor, [Terminal.ID, NonTerminal.Var_call_prime]),
    (NonTerminal.Factor, [Terminal.NUM]),
    (NonTerminal.Var_call_prime, [Terminal.PARAENTHESIS_OPEN, NonTerminal.Args, Terminal.PARAENTHESIS_CLOSE]),
    (NonTerminal.Var_call_prime, [NonTerminal.Var_prime]),
    (NonTerminal.Var_prime, [Terminal.BRACKET_OPEN, NonTerminal.Expression, Terminal.BRACKET_CLOSE]),
    (NonTerminal.Var_prime, [Terminal.EPSILON]),
    (NonTerminal.Factor_prime, [Terminal.PARAENTHESIS_OPEN, NonTerminal.Args, Terminal.PARAENTHESIS_CLOSE]),
    (NonTerminal.Factor_prime, [Terminal.EPSILON]),
    (NonTerminal.Factor_zegond, [Terminal.PARAENTHESIS_OPEN, NonTerminal.Expression, Terminal.PARAENTHESIS_CLOSE]),
    (NonTerminal.Factor_zegond, [Terminal.NUM]),
    (NonTerminal.Args, [NonTerminal.Arg_list]),
    (NonTerminal.Args, [Terminal.EPSILON]),
    (NonTerminal.Arg_list, [NonTerminal.Expression, NonTerminal.Arg_list_prime]),
    (NonTerminal.Arg_list_prime, [Terminal.COMMA, NonTerminal.Expression, NonTerminal.Arg_list_prime]),
    (NonTerminal.Arg_list_prime, [Terminal.EPSILON]),
]


if __name__ == '__main__':
    from itertools import groupby
    grouped = groupby(grammar_rules, lambda x: x[0])
    for i, (non_terminal, rules) in enumerate(grouped, 1):
        print(f"{i}. {non_terminal} ->", " | ".join(" ".join(str(x) for x in rhs) for _, rhs in rules))
