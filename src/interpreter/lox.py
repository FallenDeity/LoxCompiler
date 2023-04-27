import pathlib

from src.exceptions import PyLoxEception, PyLoxKeyboardInterrupt
from src.lexer import Lexer
from src.logger import Logger
from src.parser import Parser

from .interpreter import Interpreter
from .resolver import Resolver

__all__: tuple[str, ...] = ("PyLox",)


class PyLox:
    parser: Parser
    interpreter: Interpreter
    resolver: Resolver

    def __init__(self, source: str | pathlib.Path = "") -> None:
        self.logger = Logger(name="PyLox")
        self.lexer = Lexer(source, self.logger)

    def run_prompt(self) -> None:
        while True:
            try:
                source = input(">>> ")
            except KeyboardInterrupt:
                self.logger.debug("Exiting PyLox...")
                raise PyLoxKeyboardInterrupt
            else:
                self.logger.info("Running PyLox...")
                self.lexer.source = f"{source}\n"
                try:
                    tokens = self.lexer.scan_tokens()
                    self.parser = Parser(tokens, self.logger, self.lexer.source)
                    self.logger.info(self.parser.parse())
                    self.logger.info("Finished running PyLox.")
                except PyLoxEception:
                    continue

    def run(self) -> None:
        self.logger.info("Running PyLox...")
        tokens = self.lexer.scan_tokens()
        self.parser = Parser(tokens, self.logger, self.lexer.source)
        statements = self.parser.parse()
        if self.parser._has_error:
            return
        self.interpreter = Interpreter(self.lexer._source, self.logger)
        self.resolver = Resolver(self.interpreter)
        self.resolver._resolve(statements)
        self.interpreter.interpret(statements)
        self.logger.info("Finished running PyLox.")
