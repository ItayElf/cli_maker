from cli_maker.cli_function import CliFunction
from cli_maker.line_parser import parse_line
import sys

class Cli(object):
    def __init__(self) -> None:
        super().__init__()
        self.functions = {}

    def cli_function(self, arguments=None, flags=None):
        def decorator(func):
            f = CliFunction(func, arguments, flags)
            self.functions[f.name] = f

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper
        return decorator

    def run(self):
        fname, regular, arguments, flags = parse_line(sys.argv[1:])
        if fname not in self.functions:
            print(f"Unknown function: {fname}")
            return
        
        try:
            self.functions[fname](regular, arguments, flags)
        except Exception as e:
            print(e)