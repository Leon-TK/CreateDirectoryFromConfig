from abc import ABC, abstractmethod

from .directory import IDirectory

class DirectoryIterator(ABC):
    @abstractmethod
    def GetNext(self) -> IDirectory:
        pass
    @abstractmethod
    def GetSize(self) -> int:
        pass