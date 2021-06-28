from cli_maker.cli import Cli

cli = Cli()

@cli.cli_function(arguments=["times"], flags=["space"])
def foo(bar, times=5, space=False):
    for i in range(int(times)):
        print(bar, end=" " if space else "")

cli.run()