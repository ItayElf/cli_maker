from cli_maker.cli import Cli

cli = Cli()

@cli.cli_function
def foo(bar:str, times:int=5, space:bool=False):
    for i in range(int(times)):
        print(bar, end=" " if space else "")

cli.run()