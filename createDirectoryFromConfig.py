#SPDX-FileCopyrightText: � 2022 Leonid Tkachenko leon24rus@gmail.com
#SPDX-License-Identifier: MIT License

import sys

from _src.parser import HierarchyParser
from _src.cmdLineManagers import CmdLineManager
from _src.directoryCreators import DirectoryCreator, IDirectoryCreator
import _src.configManager as configManager

#########################
#args: look printHelp()

if __name__ == "__main__":
    cmdLineManager = CmdLineManager(sys.argv)
    cfgManager = configManager.ConfigManager(cmdLineManager.GetConfigName(), cmdLineManager.GetConfigPath())
    if not cfgManager.doesConfigExist():
        print(f"Config does not exist") 
        sys.exit(0)
    if not cfgManager.hasConfigContent(): 
        print(f"Config has no content")
        sys.exit(0)
    parser = HierarchyParser(cfgManager.FetchBuffer())
    tree = parser.parseHierarchy()

    dirCreator: IDirectoryCreator = DirectoryCreator(cmdLineManager.GetDirPath(), tree, True)
    dirCreator.CreateDirectory()
    cfgManager.CloseFile() #TODO: because of unfinished iterator, this statement won't execute