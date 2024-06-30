import enum
from typing import List, Tuple, Union
from code_gen import SemanticRoutine

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
    (NonTerminal.Program, [NonTerminal.Declaration_list]), # OK
    (NonTerminal.Declaration_list, [NonTerminal.Declaration, NonTerminal.Declaration_list]), # OK
    (NonTerminal.Declaration_list, [Terminal.EPSILON]), # OK
    (NonTerminal.Declaration, [NonTerminal.Declaration_initial, NonTerminal.Declaration_prime]), # OK
    (NonTerminal.Declaration_initial, [SemanticRoutine.SA_BEGIN_DECLERATION, NonTerminal.Type_specifier, Terminal.ID, SemanticRoutine.SA_ASSIGN_NAME]), # OK
    (NonTerminal.Declaration_prime, [SemanticRoutine.SA_DECLERATION_ROLE_FUNCTION, NonTerminal.Fun_declaration_prime]), # OK
    (NonTerminal.Declaration_prime, [NonTerminal.Var_declaration_prime]), # OK
    (NonTerminal.Var_declaration_prime, [SemanticRoutine.SA_DECLERATION_ROLE_VARIABLE, Terminal.SEMICOLON]), # OK
    (NonTerminal.Var_declaration_prime, [Terminal.BRACKET_OPEN, Terminal.NUM, SemanticRoutine.PNUM, Terminal.BRACKET_CLOSE, SemanticRoutine.SA_DECLERATION_ROLE_ARRAY, Terminal.SEMICOLON]), # OK
    (NonTerminal.Fun_declaration_prime, [Terminal.PARAENTHESIS_OPEN, NonTerminal.Params, Terminal.PARAENTHESIS_CLOSE, SemanticRoutine.SA_BEGIN_FUNCTION_STATEMENT, NonTerminal.Compound_stmt, SemanticRoutine.SA_FUNCTION_RETURN_JUMP, SemanticRoutine.SA_END_FUNCTION_STATEMENT]), # TODO
    (NonTerminal.Type_specifier, [Terminal.INT, SemanticRoutine.SA_TYPE_SPECIFIER_INT]), #Ok
    (NonTerminal.Type_specifier, [Terminal.VOID, SemanticRoutine.SA_TYPE_SPECIFIER_VOID]), #Ok
    (NonTerminal.Params, [SemanticRoutine.SA_BEGIN_DECLERATION, Terminal.INT, SemanticRoutine.SA_TYPE_SPECIFIER_INT, Terminal.ID, SemanticRoutine.SA_ASSIGN_NAME, NonTerminal.Param_prime, NonTerminal.Param_list]), #Ok
    (NonTerminal.Params, [Terminal.VOID]), #Ok
    (NonTerminal.Param_list, [Terminal.COMMA, NonTerminal.Param, NonTerminal.Param_list]), #maybe cause duplicate type specifier #TODO
    (NonTerminal.Param_list, [Terminal.EPSILON]), #Ok
    (NonTerminal.Param, [NonTerminal.Declaration_initial, NonTerminal.Param_prime]), #Ok
    (NonTerminal.Param_prime, [SemanticRoutine.SA_PARAM_ROLE_ARRAY, Terminal.BRACKET_OPEN, Terminal.BRACKET_CLOSE]), #Ok
    (NonTerminal.Param_prime, [Terminal.EPSILON, SemanticRoutine.SA_PARAM_ROLE_INT]), #Ok
    (NonTerminal.Compound_stmt, [SemanticRoutine.SCOPE_ENTER, Terminal.BRACE_OPEN, NonTerminal.Declaration_list, NonTerminal.Statement_list, Terminal.BRACE_CLOSE, SemanticRoutine.SCOPE_EXIT]), #Ok
    (NonTerminal.Statement_list, [NonTerminal.Statement, NonTerminal.Statement_list]), #Ok
    (NonTerminal.Statement_list, [Terminal.EPSILON]), #Ok
    (NonTerminal.Statement, [NonTerminal.Expression_stmt]), #Ok
    (NonTerminal.Statement, [NonTerminal.Compound_stmt]), #Ok 
    (NonTerminal.Statement, [NonTerminal.Selection_stmt]), #Ok
    (NonTerminal.Statement, [NonTerminal.Iteration_stmt]), #Ok
    (NonTerminal.Statement, [NonTerminal.Return_stmt]), #Ok
    (NonTerminal.Expression_stmt, [NonTerminal.Expression, Terminal.SEMICOLON, SemanticRoutine.POP]), #OK
    (NonTerminal.Expression_stmt, [SemanticRoutine.SA_CHECK_BREAK_JP_SAVE, Terminal.BREAK, Terminal.SEMICOLON]), #OK
    (NonTerminal.Expression_stmt, [Terminal.SEMICOLON, SemanticRoutine.POP]), #Ok
    (NonTerminal.Selection_stmt, [Terminal.IF, Terminal.PARAENTHESIS_OPEN, NonTerminal.Expression, Terminal.PARAENTHESIS_CLOSE, SemanticRoutine.SAVE, NonTerminal.Statement, NonTerminal.Else_stmt]),
    (NonTerminal.Else_stmt, [Terminal.ENDIF, SemanticRoutine.JPF]), #Ok
    (NonTerminal.Else_stmt, [Terminal.ELSE, SemanticRoutine.JPF_SAVE, NonTerminal.Statement, Terminal.ENDIF, SemanticRoutine.JP]), #Ok
    (NonTerminal.Iteration_stmt, [Terminal.FOR, Terminal.PARAENTHESIS_OPEN, NonTerminal.Expression, Terminal.SEMICOLON, SemanticRoutine.LABEL, NonTerminal.Expression, Terminal.SEMICOLON, SemanticRoutine.SAVE_JUMP, NonTerminal.Expression, Terminal.PARAENTHESIS_CLOSE, SemanticRoutine.JUMP_FILL, NonTerminal.Statement, SemanticRoutine.FOR]), #Ok
    (NonTerminal.Return_stmt, [Terminal.RETURN, NonTerminal.Return_stmt_prime, SemanticRoutine.SA_FUNCTION_RETURN_JUMP]), #Ok
    (NonTerminal.Return_stmt_prime, [Terminal.SEMICOLON]), # OK #Ok
    (NonTerminal.Return_stmt_prime, [NonTerminal.Expression, SemanticRoutine.SA_FUNCTION_RETURN_VALUE, Terminal.SEMICOLON]), # OK #Ok
    (NonTerminal.Expression, [NonTerminal.Simple_expression_zegond]), #Ok
    (NonTerminal.Expression, [Terminal.ID, SemanticRoutine.PID, NonTerminal.B]), #Ok
    (NonTerminal.B, [Terminal.EQUAL, NonTerminal.Expression, SemanticRoutine.PID_ASSIGN]), # OK
    (NonTerminal.B, [Terminal.BRACKET_OPEN, NonTerminal.Expression, Terminal.BRACKET_CLOSE, SemanticRoutine.SA_INDEX_ARRAY_POP, NonTerminal.H]), #Ok
    (NonTerminal.B, [NonTerminal.Simple_expression_prime]), # OK
    (NonTerminal.H, [Terminal.EQUAL, NonTerminal.Expression, SemanticRoutine.PID_ASSIGN]), #Ok
    (NonTerminal.H, [NonTerminal.G, NonTerminal.D, NonTerminal.C]), #Ok
    (NonTerminal.Simple_expression_zegond, [NonTerminal.Additive_expression_zegond, NonTerminal.C]), #Ok
    (NonTerminal.Simple_expression_prime, [NonTerminal.Additive_expression_prime, NonTerminal.C]), #Ok
    (NonTerminal.C, [NonTerminal.Relop, NonTerminal.Additive_expression, SemanticRoutine.DO_RELOP]), # OK
    (NonTerminal.C, [Terminal.EPSILON]), # OK
    (NonTerminal.Relop, [Terminal.GREATER, SemanticRoutine.PUSH_RELOP_GREATER]), # OK
    (NonTerminal.Relop, [Terminal.DOUBLE_EQUAL, SemanticRoutine.PUSH_RELOP_EQUAL]), # OK
    (NonTerminal.Additive_expression, [NonTerminal.Term, NonTerminal.D]), #Ok
    (NonTerminal.Additive_expression_prime, [NonTerminal.Term_prime, NonTerminal.D]), #Ok
    (NonTerminal.Additive_expression_zegond, [NonTerminal.Term_zegond, NonTerminal.D]), #Ok
    (NonTerminal.D, [NonTerminal.Addop, NonTerminal.Term, SemanticRoutine.DO_ADDOP, NonTerminal.D]), #Ok
    (NonTerminal.D, [Terminal.EPSILON]), #Ok
    (NonTerminal.Addop, [Terminal.PLUS, SemanticRoutine.PUSH_PLUS]), #Ok
    (NonTerminal.Addop, [Terminal.MINUS, SemanticRoutine.PUSH_MINUS]), #Ok
    (NonTerminal.Term, [NonTerminal.Signed_factor, NonTerminal.G]), #Ok
    (NonTerminal.Term_prime, [NonTerminal.Signed_factor_prime, NonTerminal.G]), #Ok
    (NonTerminal.Term_zegond, [NonTerminal.Signed_factor_zegond, NonTerminal.G]), #Ok
    (NonTerminal.G, [Terminal.STAR, NonTerminal.Signed_factor, SemanticRoutine.DO_MULTIPLY, NonTerminal.G]), # OK
    (NonTerminal.G, [Terminal.EPSILON]), # OK
    (NonTerminal.Signed_factor, [Terminal.PLUS, NonTerminal.Factor]), # OK
    (NonTerminal.Signed_factor, [Terminal.MINUS, NonTerminal.Factor, SemanticRoutine.NEGATE_SS_TOP]), # OK
    (NonTerminal.Signed_factor, [NonTerminal.Factor]), # OK
    (NonTerminal.Signed_factor_prime, [NonTerminal.Factor_prime]), #Ok
    (NonTerminal.Signed_factor_zegond, [Terminal.PLUS, NonTerminal.Factor]), # OK
    (NonTerminal.Signed_factor_zegond, [Terminal.MINUS, NonTerminal.Factor, SemanticRoutine.NEGATE_SS_TOP]), # OK
    (NonTerminal.Signed_factor_zegond, [NonTerminal.Factor_zegond]), #Ok
    (NonTerminal.Factor, [Terminal.PARAENTHESIS_OPEN, NonTerminal.Expression, Terminal.PARAENTHESIS_CLOSE]), # OK
    (NonTerminal.Factor, [Terminal.ID, SemanticRoutine.PID, NonTerminal.Var_call_prime]), #Ok
    (NonTerminal.Factor, [Terminal.NUM, SemanticRoutine.PNUM]), # OK
    (NonTerminal.Var_call_prime, [SemanticRoutine.SA_BEGIN_FUNCTION_CALL, Terminal.PARAENTHESIS_OPEN, NonTerminal.Args, Terminal.PARAENTHESIS_CLOSE, SemanticRoutine.SA_END_FUNCTION_CALL]), # OK
    (NonTerminal.Var_call_prime, [NonTerminal.Var_prime]), #Ok
    (NonTerminal.Var_prime, [Terminal.BRACKET_OPEN, NonTerminal.Expression, Terminal.BRACKET_CLOSE, SemanticRoutine.SA_INDEX_ARRAY_POP]), #Ok
    (NonTerminal.Var_prime, [Terminal.EPSILON]), # OK
    (NonTerminal.Factor_prime, [SemanticRoutine.SA_BEGIN_FUNCTION_CALL, Terminal.PARAENTHESIS_OPEN, NonTerminal.Args, Terminal.PARAENTHESIS_CLOSE, SemanticRoutine.SA_END_FUNCTION_CALL]), # OK
    (NonTerminal.Factor_prime, [Terminal.EPSILON]), #Ok
    (NonTerminal.Factor_zegond, [Terminal.PARAENTHESIS_OPEN, NonTerminal.Expression, Terminal.PARAENTHESIS_CLOSE]), # OK
    (NonTerminal.Factor_zegond, [Terminal.NUM, SemanticRoutine.PNUM]), # OK
    (NonTerminal.Args, [NonTerminal.Arg_list]), # OK
    (NonTerminal.Args, [Terminal.EPSILON]), # OK
    (NonTerminal.Arg_list, [NonTerminal.Expression, NonTerminal.Arg_list_prime]), # OK
    (NonTerminal.Arg_list_prime, [Terminal.COMMA, NonTerminal.Expression, NonTerminal.Arg_list_prime]), # OK
    (NonTerminal.Arg_list_prime, [Terminal.EPSILON]), # OK
]


if __name__ == '__main__':
    from itertools import groupby
    from termcolor import colored
    grouped = groupby(grammar_rules, lambda x: x[0])
    for i, (non_terminal, rules) in enumerate(grouped, 1):
        print(f"{i}. {non_terminal} ->", " | ".join(" ".join((colored(x, 'red') if isinstance(x, SemanticRoutine) else str(x)) for x in rhs) for _, rhs in rules))
