import sys
from abc import ABC, abstractmethod

from .directory import IDirectory
from .directoryIterator import DirectoryIterator


#TODO make it as generator

class Command(ABC):
    @abstractmethod
    def Run(self):
        pass

class CommanHistory():
    def __init__(self) -> None:
        self.lastCommand = None
    def SaveLastCommand(self, cmd: Command):
        self.lastCommand = cmd

class State(ABC):
    @abstractmethod
    def Run(self):
        pass

class AState:
    def __init__(self, iterator) -> None:
        self.iterator: ColumnDirectoryIterator  = iterator

class ColumnDirectoryIterator(DirectoryIterator):
    def __init__(self, directoryTree: IDirectory) -> None:
        self.baseDir = directoryTree
        self.head = None # current directory
        self.headIndexInParent = -1 # index of current directory in parent children list
        self.headChildrenRemained = -1 # how many children did we go though
        self.parentChildrenRemained = -1
        self.prevAction = 'begin'
        self.size = self.baseDir.GetSize()
        self.state = None

    def GetSize(self) -> int:
        return self.size
        
    def SetState(self, state):
        self.state = state

    def GetNext(self) -> IDirectory:
        self.setupHead()
        return self.head

    def setupHead(self): # it setpups head
        if self.prevAction == "begin": # preinit
            #go to base
            self.goToBaseDirectory()
            return
        if self.prevAction == "goBase": # go
            if self.prevAction != "goUp" or self.prevAction == "goNeighbour" or self.prevAction == "goDown": # go down
                if self.goDown() is False:
                    if self.goNeighbour() is False:
                        if self.goUp() is False:
                            self.head = None
                        else: return
                    else: return
                else: return
            elif self.prevAction == "goUp": # go neighbour
                    if self.goNeighbour() is False:
                        if self.goUp() is False:
                            self.head = None
                        else: return
                    else: return
        else:
            if self.prevAction != "goUp" or self.prevAction == "goNeighbour" or self.prevAction == "goDown": # go down
                if self.goDown() is False:
                    if self.goNeighbour() is False:
                        if self.goUpUntilNeighbour():
                            return
                        else: sys.exit(0) # reach the root
                    else: return
                else: return
            elif self.prevAction == "goUp": # go neighbour
                    if self.goNeighbour() is False:
                        if self.goUpUntilNeighbour():
                            return
                        else: sys.exit(0) # reach the root
                    else: return
    def canGoDown(self) -> bool:
        return self.childrenCountOf(self.head) > 0
    def canGoUp(self) -> bool:
        return self.getParentOf(self.head) is not None
    def canGoNeighbour(self):
        return self.getNextNeighbourOf(self.head) is not None
    def goDown(self) -> bool: # false if we do dont go
        if self.canGoDown():
            self.head = self.getChildOf(self.head, 0)
            self.headIndexInParent = 0
            self.prevAction = 'goDown'
            return True
        else: return False
    
    def goUpUntilNeighbour(self) -> bool:
        self.prevAction = "goUp"
        while(self.prevAction != "goNeighbour"):
            if self.goUp() is False:
                self.head = None
                return False
            else: self.goNeighbour()
        return True

    def goNeighbour(self) -> bool:
        if self.canGoNeighbour():
            self.goToNeighbour()
            self.prevAction = 'goNeighbour'
            return True
        else: return False
    def goUp(self) -> bool:
        if self.canGoUp():
            self.goToParent()
            self.prevAction = 'goUp'
            return True
        else: return False

    def getChildOf(self, dir, index):
        count =  self.childrenCountOf(dir)
        if index < count:
            return dir.children[index]
        else: return None
    def getParentOf(self, dir):
        if dir is not None:
            return dir.parent
        else: return None
    def getNextNeighbourOf(self, dir): # you have to increment headindex in caller if you will set it as head
        pChildrenCount =  self.childrenCountOf(self.getParentOf(dir))
        if self.headIndexInParent + 1 < pChildrenCount:
            return self.getParentOf(dir).children[self.headIndexInParent + 1]
        else: return None

    def goToNeighbour(self):
        dir = self.getNextNeighbourOf(self.head)
        if dir is not None:
            self.setHead(dir)
            self.headIndexInParent += 1
        else: sys.exit(0)
    def goToChild(self, index):
        count = self.childrenCountOf(self.head)
        if index < count:
            self.headIndexInParent = index
            self.setHead(self.getChildOf(self.head, index))
        else: sys.exit(0)
    def goToBaseDirectory(self) -> IDirectory:
        self.setHead(self.baseDir)
        self.headIndexInParent = 0
        self.prevAction = "goBase"
    def goToParent(self):

        if self.getParentOf(self.head) is not None:
            self.setHead(self.getParentOf(self.head)) # head now is parent.
            parentChildrenCount = self.childrenCountOf(self.getParentOf(self.head)) # So it returns parent children count of parent head
            if parentChildrenCount is None:
                sys.exit(0)
            
            #set head index relative to parent
            if parentChildrenCount == 1:
                self.headIndexInParent = 0
            else:
                # go through all children and check if name is the same. if it is set index of iteration
                counter = 0
                for c in range(parentChildrenCount):
                    pChild = self.getChildOf(self.getParentOf(self.head), c)
                    if pChild.name == self.head.name:
                        break
                    counter += 1
                self.headIndexInParent = counter
        else: sys.exit(0)
    
    def setHead(self, d: IDirectory):
        if d is None: sys.exit(0)
        self.head = d

    def childrenCountOf(self, dir: IDirectory):
        if dir is None: return None
        return len(dir.children)

    def hasParentChildrenRemaining(self):
        if self.parentChildrenRemained > 0: return True
        else: return False
    def hasChildrenRemaining(self):
        if self.headChildrenRemained > 0: return True
        else: return False

    def decrementParentChildrenRemaining(self) -> bool:
        if self.parentChildrenRemained == 0:
            return False
        self.parentChildrenRemained -= 1
        return True
    def decrementChildrenRemaining(self) -> bool:
        if self.headChildrenRemained == 0:
            return False
        self.headChildrenRemained -= 1
        return True