from cli_maker.cli_function import CliFunction
from cli_maker.line_parser import parse_line
from textwrap import dedent
import sys
import inspect

class Cli(object):
    def __init__(self) -> None:
        super().__init__()
        self._functions = {}

    def cli_function(self, names=None):
        def decorator(func):
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
            if names != None:
                for n in names:
                    self._functions[n] = f

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper
        return decorator

    def _show_all_functions(self):
        all_names = sorted(list(set([f.name for f in self._functions.values()])))
        length = len(max(all_names, key=lambda x: len(x)))
        print("Commands:")
        for name in all_names:
            if self._functions[name].func.__doc__:
                splt = dedent(self._functions[name].func.__doc__).split('\n')
                i = 0
                desc = splt[i]
                while not desc:
                    i += 1
                    if i == len(splt):
                        desc = "\n".join(splt)
                        break
                    desc = splt[i]
                print(f"  {name.ljust(length, ' ')}  {desc}")
            else:
                print(f"  {name.ljust(length, ' ')}  ")


    def run(self):
        @self.cli_function(names=["h"])
        def help(fname):
            """Shows help about a specific function."""
            if fname not in self._functions:
                print(f"Unkown function: {fname}")
                return
            elif fname == "help" or fname == "h":
                self._show_all_functions()
                return

            names = [k for k in self._functions.keys() if self._functions[k].name == fname]
            original_name = self._functions[names[0]].name
            names.remove(original_name)
            if len(names) == 0:
                print(original_name + "\n" + "-"*len(original_name), end="")
            else:
                print(f"{original_name} (also {', '.join(names)})\n" + "-"*len(f"{original_name} (also {', '.join(names)})"), end="")
            print(dedent(self._functions[original_name].func.__doc__) if self._functions[original_name].func.__doc__ else "\nNo documentation found.")

        try:
            fname, regular, arguments, flags = parse_line(sys.argv[1:])
        except TypeError:
            self._show_all_functions()
            return
        if fname not in self._functions:
            print(f"Unknown function: {fname}")
            return
        
        try:
            self._functions[fname](regular, arguments, flags)
        except Exception as e:
            print(e)