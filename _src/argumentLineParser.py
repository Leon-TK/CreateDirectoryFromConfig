from abc import ABC, abstractmethod

from .arguments import *

class IArgumentLineParser(ABC):
    @abstractmethod
    def Parse(argLine: str) -> list:
        pass

class ArgumentLineListParser(IArgumentLineParser):
    def Parse(self, argLine: list) -> list:
        assert(len(argLine) > 0)

        parsedArgs: list = []

        argCount = 0
        for i in range(len(argLine)):
            parsed = self.ParseLineArgument(argLine[i], i + 1)
            if parsed is not None: parsedArgs.append(parsed)
        return parsedArgs

    def ParseLineArgument(self, argSignature: str, position: int) -> IArgument:
        assert(position >= 0)
        assert(len(argSignature) > 0)

        argClasses = [Help, Syntax, DirPath, ConfigName, ConfigPath]

        splittedArg = argSignature.split("=")
        assert(len(splittedArg) <= 2)

        for argClass in argClasses:
            parsedName = ""
            obj = argClass()
            hasValue = argClass.HasValue()
            if hasValue: parsedName = splittedArg[0] + "=" #add = because split() deletes it
            else: parsedName = splittedArg[0]
            missValue = False
            if hasValue and len(splittedArg) == 2:
                if len(splittedArg[1]) == 0: missValue = True

            hasPosition = argClass.GetPosition() is not None
            missPosition = False
            canOmmitName = argClass.CanOmmitCommandName
            canOmmintPos = argClass.CanOmmitPosition()
            if hasPosition and not canOmmintPos and argClass.GetPosition() != position: missPosition = True

            if argClass.GetCommand() == parsedName:
                if missValue or missPosition: return None
                if hasValue:
                    obj.SetValue(splittedArg[1])
                if hasPosition:
                    pass
                return obj
            continue
        return None


class ArgumentLineStrParser(IArgumentLineParser):
    def Parse(argLine) -> list:
        args: IArgument = []
        return args
