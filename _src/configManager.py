import sys
import os

from .stringUtils import Append

class ConfigManager:
    def __init__(self, cfgName, cfgDir) -> None:
        self.cfgName = cfgName
        self.cfgDir = cfgDir
        self.file = None
        self.LoadFile()

    def LoadFile(self):
        path = Append(self.cfgDir, self.cfgName)
        try:
            self.file = open(path, 'r') #TODO do I need 'r'?
        except FileNotFoundError:
                print(f"{path} config's not found'")
                sys.exit(0)

    def CloseFile(self):
        self.file.close()

    def FetchBuffer(self) -> str:
        assert(self.file is not None)
        currPos = self.file.tell()
        buffer = self.file.read()
        self.file.seek(currPos)
        return buffer

    def doesConfigExist(self) -> bool:
        return os.path.exists(Append(self.cfgDir, self.cfgName))

    def hasConfigContent(self) -> bool:
        return len(self.FetchBuffer()) > 0