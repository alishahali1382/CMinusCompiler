from typing import Callable, Dict, Generator, List, Optional, Tuple

import anytree

from file_writers import syntax_error_file_writer
from first_follow_calculator import FirstFollowCalculator
from parser_constants import *
from scanner import Scanner, Token, TokenType


def token_reader(scanner: Scanner) -> Generator[Tuple[Token, int], None, None]:
    with open("input.txt", "r") as scanner.input_file:
        while not scanner.end_of_file:
            token, lineno = scanner.get_next_token()
            if token.token_type in [TokenType.ID, TokenType.NUM, TokenType.KEYWORD, TokenType.SYMBOL]:
                yield token, lineno

    yield Token(TokenType.EOF, '$'), scanner.lineno

class Parser:
    def __init__(self, rules: List[GRAMMAR_RULE]):
        self.rules = rules
        self.scanner = Scanner(ignore_errors=True)
        self.token_generator = token_reader(self.scanner)
        self.lookahead = None
        self.procedures: Dict[NonTerminal, Callable] = {}
        self.eof = False
        
        first_follow_calculator = FirstFollowCalculator(rules)
        self.first_sets = first_follow_calculator.calculate_first_sets()
        self.follow_sets = first_follow_calculator.calculate_follow_sets()
        self.predict_sets = first_follow_calculator.calculate_predict_sets()
        
        self.rules[0][1].append(Terminal.EOF)
        
        for non_terminal in NonTerminal:
            self.procedures[non_terminal] = self.create_procedure(non_terminal)

    def get_lookahead(self):
        if self.eof:
            return None
        token, _ = self.get_lookahead_token()
        token_type = token.token_type
        if token_type in [TokenType.ID, TokenType.NUM, TokenType.EOF]:
            return Terminal.with_name(token_type.name)
        return Terminal.from_str(token.token_string)

    def get_lookahead_token(self):
        if self.eof:
            return None
        if self.lookahead is None:
            self.lookahead = next(self.token_generator)
        return self.lookahead

    def discard_lookahead(self):
        if self.lookahead[0].token_type == TokenType.EOF:
            self.eof = True
        self.lookahead = None

    @staticmethod
    def error(message: str, lineno: int):
        print(f"#{lineno}: syntax error, {message}")

    @staticmethod
    def getNode(non_terminal: NonTerminal, children: List[Optional[anytree.Node]]) -> anytree.Node:
        return anytree.Node(str(non_terminal), children=[child for child in children if child is not None])

    def match_procedure(self, terminal: Terminal) -> Optional[anytree.Node]:
        if self.eof:
            return None
        # TODO
        lookahead = self.get_lookahead()
        token, lineno = self.get_lookahead_token()
        if lookahead == Terminal.EOF:
            if lookahead == terminal:
                return anytree.Node("$")
            self.error(f"Unexpected EOF", lineno)
            return None

        if lookahead == terminal:
            self.discard_lookahead()
            return anytree.Node(str(token))

        if terminal == Terminal.EOF:
            if lookahead != terminal:
                self.discard_lookahead()
                return self.match_procedure(terminal)
            
        self.error(f"missing {terminal}", lineno)
        #self.discard_lookahead()
        # return self.match_procedure(terminal)
        return None

    def create_procedure(self, non_terminal: NonTerminal):
        rule_ids = [i for i, rule in enumerate(self.rules) if rule[0] == non_terminal]
        def procedure() -> Optional[anytree.Node]:
            if self.eof:
                return None
            children = []
            lookahead = self.get_lookahead()
            for i in rule_ids:
                rhs = self.rules[i][1]
                if lookahead not in self.predict_sets[i]:
                    continue
                if rhs == [Terminal.EPSILON]:
                    return anytree.Node(str(non_terminal), children=[anytree.Node("epsilon")])
                for symbol in rhs:
                    if isinstance(symbol, NonTerminal):
                        children.append(self.procedures[symbol]())  # Call NonTerminal procedure
                    else:
                        children.append(self.match_procedure(symbol))  # Match Terminal
                return self.getNode(non_terminal, children=children)

            if lookahead in self.follow_sets[non_terminal]:
                self.error(f"missing {non_terminal}", self.get_lookahead_token()[1])
                #self.discard_lookahead()
                return None
            if lookahead == Terminal.EOF:
                self.error(f"Unexpected EOF", self.get_lookahead_token()[1])
                self.discard_lookahead()
                return procedure()
            self.error(f"illegal {lookahead}", self.get_lookahead_token()[1])
            self.discard_lookahead()
            return procedure()
        return procedure
    
    def parse(self) -> anytree.Node:
        return self.procedures[NonTerminal.Program]()

    def parse_and_write(self):
        with syntax_error_file_writer() as self.error:
            root = self.parse()

        with open("parse_tree.txt", "w") as f:
            f.write(anytree.RenderTree(root).by_attr())
