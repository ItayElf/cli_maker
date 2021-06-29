from cli_maker.cli import Cli

cli = Cli()

@cli.cli_function(names=["f"])
def foo(bar:str, times:int=5, space:bool=False):
    """
    Prints a variable number of times with or without space.

    Usage:
        example.py foo [bar] <times> <space>
        example.py foo "Hello World!" -times 10 --space 

    Parameters:
        bar:     the printed variable
        -times:  number of times to print "bar"
        --space: prints with spaces
    """
    for i in range(times):
        print(bar, end=" " if space else "")

cli.run()