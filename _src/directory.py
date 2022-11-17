from abc import ABC, abstractmethod

class IDirectory(ABC):
    @abstractmethod
    def GetPath(self) -> str:
        pass
    @abstractmethod
    def GetSize(self) -> int:
        pass

class ADirectory():
    def __init__(self, name: str, parent: "IDirectory" = None, children: 'IDirectory' = None) -> None:
        self.name = name
        self.parent = parent
        self.children = []
        if children is not None:
            self.children = children
        self.size = self.FetchChildrenSize()

    def FetchChildrenSize(self):
        size = 0
        if self.children:
            for child in self.children:
                size += child.GetSize()
        return size

class Directory_Impl(ADirectory, IDirectory):
    def __init__(self, name: str, parent: "Directory_Impl" = None, children: 'Directory_Impl' = None) -> None:
        ADirectory.__init__(self, name, parent, children)
    def GetPath(self) -> str: #goes through parents
        pathElements = []
        pathElements.append(self.name)

        if self.parent is None: return pathElements[0]

        currParent = self.parent
        while(currParent is not None): # dont process last directory
            pathElements.insert(0, "\\")
            pathElements.insert(0, currParent.name)
            currParent = currParent.parent
        strPath = ''
        for element in pathElements:
            strPath += element
        return strPath
    def GetSize(self) -> int:
        return self.size