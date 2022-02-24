from abc import ABC, abstractmethod

class IArgument(ABC):
    @abstractmethod
    def GetHelpMessage() -> str:
        pass
    @abstractmethod
    def GetCommand() -> str:
        pass
    @abstractmethod
    def GetPosition() -> int:
        pass
    @abstractmethod
    def GetValue(self) -> str:
        pass
    @abstractmethod
    def SetValue(self, value: str):
        pass
    @abstractmethod
    def HasValue() -> bool:
        pass
    @abstractmethod
    def CanOmmitCommandName() -> bool:
        pass
    @abstractmethod
    def CanOmmitPosition() -> bool:
        pass

class AArgument():
    def __init__(self) -> None:
        self.value = None

class Help(AArgument, IArgument):
    def __init__(self) -> None:
        AArgument.__init__(self)
    def GetCommand() ->str:
        return "-help"
    def GetPosition() -> int:
        return None
    def GetHelpMessage() -> str:
        return f"Arguments help:\n1. {DirPath().GetCommand()} Directory where folders will be created (default is script's directory).\n\
2. {ConfigName().GetCommand()} Config file name to parse from (default is script's name + \'Config.txt\'). \n\
3. {ConfigPath().GetCommand()} Config file directory (default is script's directory)\nCommands:\n-help -syntax"
    def GetValue(self) -> str:
        return self.value
    def SetValue(self, value: str):
        self.value = value
    def CanOmmitCommandName() -> bool:
        return False;
    def HasValue() -> bool:
        return False
    def CanOmmitPosition() -> bool:
        return True
class Syntax(AArgument, IArgument):
    def __init__(self) -> None:
        AArgument.__init__(self)
    def GetCommand() ->str:
        return "-syntax"
    def GetPosition() -> int:
        return None
    def GetHelpMessage() -> str:
        return "Syntax.\nEach line represents a folder. Paste tab before folder name to note that this folder is child of previous that has less tabs\
(if prev. line has same count of tabs, current line is not a child)\n\
Parent\n\tChild2\n\tChild3\n\tChild4\nNewParent\n\tChild1\n\tChild2\n\t\tChildOfChild\n\tChild3"
    def GetValue(self) -> str:
        return self.value
    def SetValue(self, value: str):
        self.value = value
    def CanOmmitCommandName() -> bool:
        return False;
    def HasValue() -> bool:
        return False
    def CanOmmitPosition() -> bool:
        return True
class ConfigName(AArgument, IArgument):
    def __init__(self) -> None:
        AArgument.__init__(self)
    def GetCommand() ->str:
        return "-cfgName="
    def GetPosition() -> int:
        return 3
    def GetHelpMessage() -> str:
        return "Name of a config"
    def GetValue(self) -> str:
        return self.value
    def CanOmmitCommandName() -> bool:
        return True;
    def SetValue(self, value: str):
        self.value = value
    def HasValue() -> bool:
        return True
    def CanOmmitPosition() -> bool:
        return True
class ConfigPath(AArgument,IArgument):
    def __init__(self) -> None:
        AArgument.__init__(self)
    def GetCommand() ->str:
        return "-cfgPath="
    def GetPosition() -> int:
        return 4
    def GetHelpMessage() -> str:
        return "Directory of a config"
    def GetValue(self) -> str:
        return self.value
    def CanOmmitCommandName() -> bool:
        return True;
    def SetValue(self, value: str):
        self.value = value
    def HasValue() -> bool:
        return True
    def CanOmmitPosition() -> bool:
        return True
class DirPath(AArgument,IArgument):
    def __init__(self) -> None:
        AArgument.__init__(self)
    def GetCommand() ->str:
        return "-dirPath="
    def GetPosition() -> int:
        return 2
    def GetHelpMessage() -> str:
        return "Directory where folders will be created"
    def GetValue(self) -> str:
        return self.value
    def CanOmmitCommandName() -> bool:
        return True;
    def SetValue(self, value: str):
        self.value = value
    def HasValue() -> bool:
        return True
    def CanOmmitPosition() -> bool:
        return True