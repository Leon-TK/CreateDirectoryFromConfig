import sys
from pathlib import Path

from interface import *


#TODO: create normal implementation of cmd line processing
if __name__ == "__main__":

    print(dir())

    src = sys.argv[1]
    bUseSameDirectory = "-s" in sys.argv
    dst = sys.argv[2] if not bUseSameDirectory else Path(src).parent

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