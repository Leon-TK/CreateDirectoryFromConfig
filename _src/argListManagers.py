from abc import ABC, abstractmethod

from .arguments import IArgument
from .argumentLineParser import IArgumentLineParser, ArgumentLineListParser, ArgumentLineStrParser

class IArgumentLineManager(ABC):
    @abstractmethod
    def hasArgument(argName) -> bool:
        pass
    @abstractmethod
    def isArgumentAtDefaultPosition(self, defaultArgument) -> bool:
        pass
    @abstractmethod
    def GetArg(self, argName) -> IArgument:
        pass
    @abstractmethod
    def ParseArgs(self) -> list:
        pass

class ArgumentLineListManager(IArgumentLineManager):
    def __init__(self, argLine: list) -> None:
        assert(len(argLine) > 0)

        self.rawArgs: list = argLine
        self.parsedArgs = []

    def hasArgument(self, argName) -> bool:
        assert(len(argName) > 0)

        if len(self.ParseArgs) > 0:
            for arg in self.parsedArgs:
                if argName in arg.GetCommand(): return True
            return False
        return None

    def isArgumentAtDefaultPosition(self, defaultArgument: IArgument) -> bool: #TODO argument class gives only default position
        assert(defaultArgument is not None and type(defaultArgument) is IArgument)

        hasArgument = self.hasArgument(defaultArgument.GetCommand())
        if hasArgument is False or None: return None

        arg = self.GetArg(defaultArgument.GetCommand())
        if arg is None: return None
        if arg is type(defaultArgument): #TODO change to isinstance()
            if arg.GetPosition() == defaultArgument.GetPosition(): return True #TODO change it. read above
            else: return False
        return None

    def GetArg(self, argName) -> IArgument:
        assert (len(argName) > 0)

        if len(self.parsedArgs) > 0:
            for argElem in self.parsedArgs:
                if argElem is not None:
                    if argName == argElem.GetCommand():
                        return argElem
            return None
        return None

    def ParseArgs(self) -> list:
        parser: IArgumentLineParser = ArgumentLineListParser()
        if len(self.rawArgs) > 0:
            self.parsedArgs = parser.Parse(self.rawArgs)
            return self.parsedArgs
        return None

#TODO
class ArgumentLineStrManager(IArgumentLineManager):
    def __init__(self, argLine: str) -> None:
        self.argLine = argLine
        self.parser: IArgumentLineParser = ArgumentLineListParser()
        self.args = list()

    def hasArgument(self, argName) -> bool:
        return argName in self.argLine

    def isArgumentAtDefaultPosition(self, defaultArgument) -> bool:
        if not self.hasArgument(defaultArgument.GetCommand()) : return False
        arg = self.GetArg(defaultArgument.GetCommand())
        if arg.GetPosition() == defaultArgument.GetPosition(): return True
        return False

    def GetArg(self, argName) -> IArgument:
        if not self.hasArgument(argName): return None
        for arg in self.args:
            if argName in arg.GetCommand() and len(argName) == len(arg.GetCommand()): return arg
        return None

    def ParseArgs(self) -> list:
        self.args = self.parser.Parse()
        return self.args