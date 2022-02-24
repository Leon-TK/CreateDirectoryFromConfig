from .arguments import IArgument

class ArgumentManager:
    def PrintHelp(argument: IArgument):
        print(argument.GetHelpMessage())