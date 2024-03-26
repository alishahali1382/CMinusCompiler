import enum
from abc import ABC
from io import TextIOWrapper
from typing import Dict, List, Tuple


class TokenType(enum.Enum):
    NUM = 1
    ID = 2
    KEYWORD = 3
    SYMBOL = 4
    COMMENT = 5
    WHITESPACE = 6

class ErrorType(enum.Enum):
    INVALID_INPUT = "Invalid input"
    UNCLOSED_COMMENT = "Unclosed comment"
    UNMATCHED_COMMENT = "Unmatched comment"
    INVALID_NUMBER = "Invalid number"

class CharacterSet(enum.Enum):
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
    def __init__(self, state_id: int, get_token_func):
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


class Scanner:
    def __init__(self):
        self.dfa = self.build_dfa()
        self.input_file = None
        self.end_of_file = False
        self.lineno = 1
        self.buffered_input = None

    @staticmethod
    def build_dfa() -> DFA:
        start = IntermediateState(0)
        all_states = [start]
        # TODO: Add all states and transitions to the DFA
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
        print(f"Error at line {lineno}: {error_type.value} - {message}")
        # TODO: Write error to error file

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
                token_type, token_string = state.get_token(self.dfa.parsed_input)
                self.dfa.reset()
                return token_type, token_string

        assert False, "End of file reached but no token detected"

    def tokenize(self):
        with open("input.txt", "r") as self.input_file, open("tokens.txt", "w") as output_file:
            while not self.end_of_file:
                token_type, token_string = self.get_next_token()
                output_file.write(f"({token_type}, {token_string})\n")
