import sys
from pathlib import Path
from abc import ABC, abstractmethod

import fileSystemChecks as fsChecks

from .directory import IDirectory, Directory_Impl
from .directoryIterator import DirectoryIterator
from .columnDirectoryIterator import ColumnDirectoryIterator

class IDirectoryCreator(ABC):
    @abstractmethod
    def CreateDirectory(self) -> None:
        pass

class DirectoryCreator(IDirectoryCreator):
    def __init__(self, creationPath: str, directoryTree, bIgnoreIternalRoot) -> None:
        self.creationPath = creationPath
        self.directoryTree = directoryTree
        self.bIgnoreIternalRoot = bIgnoreIternalRoot

    def CreateDirectory(self) -> None:
        if not fsChecks.DirectoryPathCheck(self.creationPath): sys.exit(-1)

        dir: IDirectory = Directory_Impl("")
        iterator: DirectoryIterator = ColumnDirectoryIterator(self.directoryTree)

        iterCount = 0
        #dirSize = directoryTree.size()

        while(dir is not None): # TODO compare with directory size
            if iterCount == 0 and self.bIgnoreIternalRoot:
                dir = iterator.GetNext()
                if len (self.directoryTree.children) == 0:
                    print(f"Internal root {dir.name} has no children")
                    return
                iterCount += 1
                continue
            dir = iterator.GetNext() #TODO returns prematurely
            if dir is not None:
                fullPath = self.creationPath + "\\" + dir.GetPath()
                if not fsChecks.DirectoryPathCheck(fullPath): sys.exit(0)
                Path(fullPath).mkdir(parents=True,exist_ok=True)
                iterCount += 1
            else:
                print("Dir is None")
                return