class CliFunction(object):
    def __init__(self, func, arguments, flags) -> None:
        super().__init__()
        self.func = func
        self.name = func.__name__

        if arguments == None:
            self.arguments = set()
        else:
            self.arguments = set(arguments)

        if flags == None:
            self.flags = set()
        else:
            self.flags = set(flags)
    
    def __call__(self, regular, arguments, flags):
        for k in arguments.keys():
            if k not in self.arguments:
                raise Exception(f"Illegal argument: {k}")
        for k in flags.keys():
            if k not in self.flags:
                raise Exception(f"Illegal flag: {k}")
        
        return self.func(*regular, **arguments, **flags)

    def __repr__(self) -> str:
        return f"CliFunction({self.name=}, {self.arguments=}, {self.flags=}"
    
