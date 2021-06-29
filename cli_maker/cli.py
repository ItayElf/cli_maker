from cli_maker.cli_function import CliFunction
from cli_maker.line_parser import parse_line
import sys
import inspect

class Cli(object):
    def __init__(self) -> None:
        super().__init__()
        self._functions = {}

    def cli_function(self, func):
        sig = inspect.signature(func)
        arguments = {}
        flags = set()
        for key, param in sig.parameters.items():
            if param.default != inspect.Parameter.empty:
                if param.annotation == bool:
                    flags.add(key)
                else:
                    if param.annotation == inspect.Parameter.empty or param.annotation == any:
                        arguments[key] = str
                    else:
                        arguments[key] = param.annotation
        
        f = CliFunction(func, arguments, flags)
        self._functions[f.name] = f

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
        

    def run(self):
        fname, regular, arguments, flags = parse_line(sys.argv[1:])
        if fname not in self._functions:
            print(f"Unknown function: {fname}")
            return
        
        try:
            self._functions[fname](regular, arguments, flags)
        except Exception as e:
            print(e)