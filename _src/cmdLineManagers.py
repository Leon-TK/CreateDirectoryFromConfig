from ast import parse
import sys
import os
from pathlib import Path

from _fileSystemChecks import fileSystemChecks as fsChecks

from .directory import IDirectory, Directory_Impl
from .directoryIterator import DirectoryIterator
from .columnDirectoryIterator import ColumnDirectoryIterator
from .parser import HierarchyParser
from .argumentManagers import *
from .arguments import *
from .argListManagers import IArgumentLineManager, ArgumentLineListManager



class CmdLineManager:
    def __init__(self, cmdLine: list) -> None:
        self.cmdLine = cmdLine
        self.configName = None
        self.configPath = None
        self.dirPath = None
        self.parsedArgs = []
        self.Prosess()

    def GetConfigName(self) -> str:
        return self.configName
    def GetConfigPath(self) -> str:
        return self.configPath
    def GetDirPath(self) -> str:
        return self.dirPath
    
    def ParseArgs(self, args) -> list:
        argsManager: IArgumentLineManager = ArgumentLineListManager(args)
        self.parsedArgs =  argsManager.ParseArgs()
        return self.parsedArgs

    def CalcMissedArgsCount(self, mandArgCount, parsedArgs) -> int:
        argc = len(parsedArgs)
        return mandArgCount - argc

    def ProsessAllMissedArgs(self):
        ArgumentManager.PrintHelp(Help())
        #self.CreateConfigFile(self.GetDefaultConfigPath(), self.GetDefaultConfigName())
        input("Press any key to exit")
        sys.exit(0)
        
    def ProsessParsedArgs(self, args):
        for arg in args:
            if type(arg) is Help:
                ArgumentManager.PrintHelp(arg)
                input("Press any key to exit")
                sys.exit(0)
            if type(arg) is Syntax:
                ArgumentManager.PrintHelp(arg)
                input("Press any key to exit")
                sys.exit(0)
            if type(arg) is ConfigName:
                self.configName = arg.GetValue()
            if type(arg) is ConfigPath:
                self.configPath = arg.GetValue()
            if type(arg) is DirPath:
                self.dirPath = arg.GetValue()

    def ProsessDirPath(self):
        if self.dirPath is not None:
            if not self.CheckDirectoryPath(self.dirPath): sys.exit(0)
        else:
            self.dirPath = self.GetDefaultDirectoryPath()
            ArgumentManager.PrintHelp(Help())
            sys.exit(0)
    def ProsessConfigName(self):
        if self.configName is not None:
            if not self.CheckConfigName(self.configName): sys.exit(0)
        else:
            self.configName = self.GetDefaultConfigName()
    def ProsessConfigPath(self):
        if self.configPath is not None:
            if not self.CheckConfigPath(self.configPath): sys.exit(0)
        else:
            self.configPath = self.GetDefaultConfigPath()

    def Prosess(self) -> list:
        parsedArgs = self.ParseArgs(self.cmdLine)
        mandatoryArgsCount = 3
        missedArgc = self.CalcMissedArgsCount(mandatoryArgsCount, parsedArgs)

        if missedArgc == mandatoryArgsCount: self.ProsessAllMissedArgs()

        self.ProsessParsedArgs(self.parsedArgs)

        self.ProsessDirPath()

        self.ProsessConfigName()

        self.ProsessConfigPath()

    def GetDefaultConfigName(self) -> str:
        return f"{Path(__file__).stem}Config.txt"

    def GetDefaultConfigPath(self) -> str:
        return f"{os.path.dirname(__file__)}"

    def GetDefaultDirectoryPath(self) -> str:
        return f"{os.path.dirname(__file__)}"

    def CheckDirectoryPath(self, path) -> bool:
        if not fsChecks.DirectoryPathCheck(path, False): return False
        return True

    def CheckConfigName(self, name) -> bool:
        if not fsChecks.FileNameCheck(name, False, False): return False
        return True

    def CheckConfigPath(self, path) -> bool:
        if not fsChecks.DirectoryPathCheck(path, False): return False
        return True