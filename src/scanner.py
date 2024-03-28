import enum
from abc import ABC
from typing import Dict, List, Tuple, Callable
from contextlib import contextmanager

class TokenType(enum.Enum):
    NUM = 1
    ID = 2
    KEYWORD = 3
    SYMBOL = 4
    COMMENT = 5
    WHITESPACE = 6

    def __str__(self):
        return self.name

class ErrorType(enum.Enum):
    INVALID_INPUT = "Invalid input"
    UNCLOSED_COMMENT = "Unclosed comment"
    UNMATCHED_COMMENT = "Unmatched comment"
    INVALID_NUMBER = "Invalid number"

class CharacterSet:
    DIGITS = "0123456789"
    LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    WHITESPACE = " \t\n\r\f\v"
    EOF = chr(0)


class State(ABC):
    def __init__(self, state_id: int):
        self.state_id = state_id

class IntermediateState(State):
    def __init__(self, state_id: int):
        super().__init__(state_id)
        self.transitions: Dict[str, State] = {}

    def add_transition(self, input_chars: str, next_state: State):
        for ch in input_chars:
            assert ch not in self.transitions, f"Transition for input symbol '{ch}' already exists"
            self.transitions[ch] = next_state

    def get_next_state(self, input_char: str):
        return self.transitions.get(input_char)

class TerminalState(State):
    def __init__(self, state_id: int, get_token_func: Callable[[str], Tuple[TokenType, str, bool]]):
        super().__init__(state_id)
        self.get_token = get_token_func

class ErrorState(State):
    def __init__(self, state_id: int, error_type: ErrorType):
        super().__init__(state_id)
        self.error_type = error_type


class DFA:
    def __init__(self, start_state: IntermediateState, all_states: List[State]):
        self.start_state = start_state
        self.all_states = all_states
        self.current_state = start_state
        self.parsed_input = ""

    def reset(self):
        self.current_state = self.start_state
        self.parsed_input = ""

    def read_input(self, input_char: str):
        self.parsed_input += input_char
        next_state = self.current_state.get_next_state(input_char)
        if next_state and isinstance(next_state, IntermediateState):
            self.current_state = next_state
        return next_state

@contextmanager
def token_file_writer():
    last_token_lineno = 0
    with open("tokens.txt", "w") as tokens_file:
        def write_token_to_file(token_type: TokenType, token_string: str, lineno: int):
            nonlocal last_token_lineno
            if lineno != last_token_lineno:
                if last_token_lineno != 0:
                    tokens_file.write("\n")
                tokens_file.write(f"{lineno}.\t")
            tokens_file.write(f"({token_type}, {token_string}) ")
            last_token_lineno = lineno

        yield write_token_to_file
        tokens_file.write("\n")

class Scanner:
    keywords = ["if", "else", "void", "int", "for", "break", "return", "endif"]
    
    def __init__(self):
        self.dfa = self.build_dfa()
        self.end_of_file = False
        self.lineno = 1
        self.buffered_input = None
        self.symbol_table = []
        for key in Scanner.keywords:
            self.adding_symbol_table(key)

    @staticmethod
    def build_dfa() -> DFA:
        start = IntermediateState(0)
        all_states = [start]
        
        all_states.append(TerminalState(1, Scanner.get_token_symbol_without_ignore))
        start.add_transition(';', all_states[1])
        all_states.append(TerminalState(2, Scanner.get_token_symbol_without_ignore))
        start.add_transition(':', all_states[2])
        all_states.append(TerminalState(3, Scanner.get_token_symbol_without_ignore))
        start.add_transition(',', all_states[3])
        all_states.append(TerminalState(4, Scanner.get_token_symbol_without_ignore))
        start.add_transition('[', all_states[4])
        all_states.append(TerminalState(5, Scanner.get_token_symbol_without_ignore))
        start.add_transition(']', all_states[5])
        all_states.append(TerminalState(6, Scanner.get_token_symbol_without_ignore))
        start.add_transition('(', all_states[6])
        all_states.append(TerminalState(7, Scanner.get_token_symbol_without_ignore))
        start.add_transition(')', all_states[7])
        all_states.append(TerminalState(8, Scanner.get_token_symbol_without_ignore))
        start.add_transition('{', all_states[8])
        all_states.append(TerminalState(9, Scanner.get_token_symbol_without_ignore))
        start.add_transition('}', all_states[9])
        all_states.append(TerminalState(10, Scanner.get_token_symbol_without_ignore))
        start.add_transition('+', all_states[10])
        all_states.append(TerminalState(11, Scanner.get_token_symbol_without_ignore))
        start.add_transition('-', all_states[11])
        all_states.append(IntermediateState(12))
        start.add_transition('*', all_states[12])
        all_states.append(TerminalState(13, Scanner.get_token_symbol_with_ignore))
        all_states[12].add_transition(CharacterSet.DIGITS+CharacterSet.LETTERS+CharacterSet.WHITESPACE+"[({", all_states[13])
        all_states.append(ErrorState(14, ErrorType.UNMATCHED_COMMENT))
        all_states[12].add_transition('/', all_states[14])
        all_states.append(IntermediateState(15))
        start.add_transition('=', all_states[15])
        all_states.append(TerminalState(16, Scanner.get_token_symbol_with_ignore))
        all_states[15].add_transition(CharacterSet.DIGITS+CharacterSet.LETTERS+CharacterSet.WHITESPACE+"[({", all_states[16])
        all_states.append(TerminalState(17, Scanner.get_token_symbol_without_ignore))
        all_states[15].add_transition('=', all_states[17])
        all_states.append(TerminalState(18, Scanner.get_token_symbol_without_ignore))
        start.add_transition('<', all_states[18])
        
        all_states.append(IntermediateState(19))
        start.add_transition(CharacterSet.LETTERS, all_states[19])
        all_states[19].add_transition(CharacterSet.DIGITS+CharacterSet.LETTERS, all_states[19])
        all_states.append(TerminalState(20, Scanner.get_token_ID))
        all_states[19].add_transition(CharacterSet.WHITESPACE+CharacterSet.EOF+";:,+=-<*})]", all_states[20])
        
        all_states.append(IntermediateState(21))
        start.add_transition(CharacterSet.DIGITS, all_states[21])
        all_states[21].add_transition(CharacterSet.DIGITS, all_states[21])
        all_states.append(TerminalState(22, Scanner.get_token_NUM))
        all_states[21].add_transition(CharacterSet.WHITESPACE+CharacterSet.EOF+"/;:,[]{}()+-*=<", all_states[22])
        all_states.append(ErrorState(23, ErrorType.INVALID_NUMBER))
        all_states[21].add_transition(CharacterSet.LETTERS, all_states[23])
        
        all_states.append(IntermediateState(24))
        start.add_transition('/', all_states[24])
        all_states.append(IntermediateState(25))
        all_states[24].add_transition('*', all_states[25])
        all_states.append(IntermediateState(26))
        all_states[25].add_transition('*', all_states[26])
        all_states[25].add_transition(CharacterSet.DIGITS+CharacterSet.LETTERS+CharacterSet.WHITESPACE+"/;:,[]{}()+-=<", all_states[25])
        all_states[26].add_transition(CharacterSet.DIGITS+CharacterSet.LETTERS+CharacterSet.WHITESPACE+"*;:,[]{}()+-=<", all_states[25])
        all_states.append(TerminalState(27, Scanner.get_token_comment))
        all_states[26].add_transition('/', all_states[27])
        all_states.append(ErrorState(28, ErrorType.UNCLOSED_COMMENT))
        all_states[25].add_transition(CharacterSet.EOF, all_states[28])
        all_states[26].add_transition(CharacterSet.EOF, all_states[28])
        
        all_states.append(TerminalState(29, Scanner.get_token_whitespace))
        start.add_transition(CharacterSet.WHITESPACE, all_states[29])
        
        return DFA(start, all_states)

    def read_char(self) -> str:
        if self.buffered_input:
            input_char = self.buffered_input
            self.buffered_input = None
            return input_char
        
        input_char = self.input_file.read(1)
        if input_char == "\n":
            self.lineno += 1
        if not input_char:
            self.end_of_file = True
        return input_char

    def report_error(self, lineno: int, error_type: ErrorType, message: str):
        if error_type == ErrorType.INVALID_INPUT:
            message = message[-1] #TODO: but in some samples in doc we have the whole message
        elif error_type == ErrorType.UNCLOSED_COMMENT:
            if len(message) > 7:
                message = message[:7] + "..."
                
        print(f"Error at line {lineno}: {error_type.value} - {message}")
        # TODO: Write error to error file        
        
    def adding_symbol_table(self, input_string: str):
        if input_string not in self.symbol_table:
            self.symbol_table.append(input_string)
            #TODO: write this input_string to file with number len(self.symbol_table)

    def get_next_token(self) -> Tuple[TokenType, str]:
        lineno = self.lineno
        while not self.end_of_file:
            input_char = self.read_char()
            state = self.dfa.read_input(input_char)
            
            if state is None:
                self.report_error(lineno, ErrorType.INVALID_INPUT, self.dfa.parsed_input)
                self.dfa.reset()
                continue
            
            if isinstance(state, ErrorState):
                self.report_error(lineno, state.error_type, self.dfa.parsed_input)
                self.dfa.reset()
                continue
            
            if isinstance(state, TerminalState):
                token_type, token_string, ignore_last = state.get_token(self.dfa.parsed_input)
                
                if token_type == TokenType.ID:
                    self.adding_symbol_table(token_string)
                
                if ignore_last:
                    self.buffered_input = self.dfa.parsed_input[-1]
                self.dfa.reset()
                return token_type, token_string

        assert False, "End of file reached but no token detected"

    def tokenize(self):
        with open("input.txt", "r") as self.input_file, token_file_writer() as write_token_to_file:
            while not self.end_of_file:
                token_type, token_string = self.get_next_token()
                if token_type not in [TokenType.WHITESPACE, TokenType.COMMENT]:
                    write_token_to_file(token_type, token_string, self.lineno)

    def get_token_symbol_without_ignore(input_string: str) -> Tuple[str, str, bool]:
        return (TokenType.SYMBOL, input_string, False)

    def get_token_symbol_with_ignore(input_string: str) -> Tuple[str, str, bool]:
        return (TokenType.SYMBOL, input_string[:-1], True)

    def get_token_ID(input_string: str) -> Tuple[str, str, bool]:
        if input_string[:-1] in Scanner.keywords:
            return(TokenType.KEYWORD, input_string[:-1], True)
        else:
            return(TokenType.ID, input_string[:-1], True)
        
    def get_token_NUM(input_string: str) -> Tuple[str, str, bool]:
        return(TokenType.NUM, input_string[:-1], True)
    
    def get_token_comment(input_string: str) -> Tuple[str, str, bool]:
        return(TokenType.COMMENT, input_string, False)
    
    def get_token_whitespace(input_string: str) -> Tuple[str, str, bool]:
        return(TokenType.WHITESPACE, input_string, False)