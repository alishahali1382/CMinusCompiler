
from contextlib import contextmanager


@contextmanager
def base_file_writer(filename: str):
    last_lineno = 0
    with open(filename, "w") as file:
        def write_to_file(content: str, lineno: int):
            nonlocal last_lineno
            if lineno != last_lineno:
                if last_lineno != 0:
                    file.write("\n")
                file.write(f"{lineno}.\t")
            file.write(content)
            file.flush()
            last_lineno = lineno

        yield file, write_to_file

@contextmanager
def token_file_writer():
    with base_file_writer("tokens.txt") as (file, file_writer):
        def write_token_to_file(token, lineno: int):
            file_writer(f"{token} ", lineno)

        yield write_token_to_file
        file.write("\n")

@contextmanager
def lexical_error_file_writer():
    no_error = True
    with base_file_writer("lexical_errors.txt") as (file, file_writer):
        def write_error_to_file(error_type, message: str, lineno: int):
            nonlocal no_error
            no_error = False
            file_writer(f"({message}, {error_type}) ", lineno)

        yield write_error_to_file
        file.write("There is no lexical error." if no_error else "\n")
