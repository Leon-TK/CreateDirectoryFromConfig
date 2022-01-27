#from _typeshed import Self
import sys
import os
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path
class DirectoryIterator(ABC):
    @abstractmethod
    def getNext(self) -> 'Directory':
        pass

class Directory():
    def __init__(self, name: str, parent: "Directory" = None, children: 'Directory' = None) -> None:
        self.name: str = name
        self.parent: Directory = parent
        self.children: List[Directory] = []
        if children is not None:
            self.children = children
    def getPath(self):
        path = []
        path.append(self.name)
        if self.parent is None:
            return ''
        parent = self.parent
        while(parent.parent is not None): # dont handle last directory
            path.insert(0, "\\")
            path.insert(0, parent.name)
            parent = parent.parent
        strPath = ''
        for element in path:
            strPath += element
        return strPath
    def createDir(self, path):
        path = path + "\\" + self.getPath()
        pass

class ColumnDirectoryIterator(DirectoryIterator):
    def __init__(self, directoryTree: Directory) -> None:
        self.baseDir = directoryTree
        self.head = None # current directory
        self.headIndexInParent = -1 # index of current directory in parent children list
        self.headChildrenRemained = -1 # how many children did we go though
        self.parentChildrenRemained = -1
        self.prevAction = 'begin'
    def getNext(self) -> Directory:
        self.setupHead()
        return self.head
        # Go by right side of tree until the end then go up and go down again
        # go to child
        if self.childrenCountOf(self.head) > 0:
            pass
        self.goToChild(0)
        return self.head
        ###########################
        if self.hasChildrenRemaining():
            dir = self.getChildOf(self.headChildrenCount - self.headChildrenRemained)
            self.decrementChildrenRemaining()
            return dir
        # for now we have sended all children. Go to each children as head and return their children

        self.parentChildrenCount, self.parentChildrenRemained = len(self.head.children)
        self.goToChild(self.parentChildrenCount - self.parentChildrenRemained)
        if self.hasParentChildrenRemaining():
            self.decrementParentChildrenRemaining()
            self.head = self.getChildOf(self.headIndexInParent)
    def setupHead(self): # it setpups head
        if self.prevAction == "begin": # preinit
            #go to base
            self.goToBaseDirectory()
            return #TODO I dont need base directory. dont return it
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
    def goToBaseDirectory(self) -> Directory:
        self.setHead(self.baseDir)
        self.headIndexInParent = 0
        self.prevAction = "goBase"
    def goToParent(self):
        if self.getParentOf(self.head) is not None:
            self.setHead(self.getParentOf(self.head)) # head now is parent.
            parentChildrenCount = self.childrenCountOf(self.getParentOf(self.head)) # So it returns parent children count of parent head
            if parentChildrenCount is None:
                sys.exit(0)
            if parentChildrenCount == 1:
                self.headIndexInParent = 0
            else: #TODO how to determine head index?
                # go through all children and check if name is the same. if it is set index of iteration
                counter = 0
                for c in range(parentChildrenCount):
                    pChild = self.getChildOf(self.getParentOf(self.head), c)
                    if pChild.name == self.head.name:
                        break
                    counter += 1
                self.headIndexInParent = counter
        else: sys.exit(0)
    
    def setHead(self, d: Directory):
        if d is None: sys.exit(0)
        self.head = d

    def childrenCountOf(self, dir: Directory):
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

    
        
        

        # did we went through children?
        if self.headChildrenRemained == 0:
            self.headChildrenCount = 0 
            self.head = self.head.parent.parent
            # check how many children
            self.headChildrenCount, self.headChildrenRemained = len(self.head.children)
            self.head = self.directoryTree.children[0]
            self.headChildrenRemained -= 1
        else:
            pass

        return self.head

class HierarchyParser():
    def __init__(self, configFileName: str, configFileDir: str) -> None:
        self.configFileName = configFileName
        self.configFileDir = configFileDir
        self.fileBuffer = ''
        self.charsToIgnore = [' ', '\r']
        self.charsCauseError = [',', '!', '\\', '/', '$']
        self.hierarchyChar = '\t'
        self.newLineChars = ['\n']
        if not self.doesConfigExist():
            self.createConfig()
            print(f"Config not founded. Creating new one... Please write directory hierarchy in {self.configFileDir}\\{self.configFileName}")
            sys.exit(0)
        self.loadConfig()

    def loadConfig(self):
        filePath = self.configFileDir + '\\' + self.configFileName
        file = open(filePath, 'r')
        self.fileBuffer = file.read()
    def createConfig(self):
        filePath = self.configFileDir + '\\' + self.configFileName
        file = open(filePath, 'w+')
        file.close()
    def doesConfigExist(self) -> bool:
        return os.path.exists(self.configFileDir + '\\' + self.configFileName)
    def hasConfigContent(self) -> bool:
        pass
    def parseHierarchy(self):
        tabCount = 0 # '\t'
        prevTabCount = 0
        newLineCount = 0 # '\n'
        dirNameBuffer = ''
        baseDirectory = Directory('BASEITERNAL')
        headDirectory: Directory = None
        addedBeforeDirectory: Directory = None
        charIndex = 0
        # line is handled after new line is reached
        for char in self.fileBuffer:
            if char in self.charsCauseError: # user have to comply syntaxis
                sys.exit(0)

            if char == self.hierarchyChar: # tab indicates where do we go
                tabCount += 1
                charIndex += 1
                continue
                """ if headDirectory.name != "BASEINTERNAL":
                    tabCount += 1
                else: # tabs have not to be at the BASEINTERNAL
                    print("Tabs are not allowed at 0 position. You must write name folder") #TODO
                    sys.exit(0)
                continue """
                                                         # next char will be last char the file so treat it as it newLineChars
            if char in self.newLineChars or charIndex == len(self.fileBuffer) - 1: # new line reach. handle buffer between prev newline and this #TODO if end of file doesnt have \n the last line will not be saved
                if charIndex == len(self.fileBuffer) - 1:
                    dirNameBuffer += char
                else: charIndex += 1 # \n is char
                if len(dirNameBuffer) == 0:
                    print("Missed folder name. You must write folder name at each line")
                    sys.exit(0)
                if tabCount == 0: # we are in base dir
                    headDirectory = baseDirectory
                    addedBeforeDirectory = Directory(dirNameBuffer, headDirectory)
                    headDirectory.children.append(addedBeforeDirectory)
                    dirNameBuffer = ''
                    prevTabCount = tabCount
                    tabCount = 0

                if tabCount > 0: # means than we go up or deeper relative to headdir
                    tabCountDif = tabCount - prevTabCount
                    if (tabCountDif > 0): # we go deeper
                        if tabCountDif > 1: # cannot fo further than 1 step
                            print(f"Cannot change dir into by 2 steps")
                            sys.exit(0)
                        headDirectory = addedBeforeDirectory
                        addedBeforeDirectory = Directory(dirNameBuffer, headDirectory)
                        headDirectory.children.append(addedBeforeDirectory)
                        dirNameBuffer = ''
                        prevTabCount = tabCount
                        tabCount = 0
                    elif (tabCountDif < 0):
                        # how many steps do we walk through upper dirs
                        addedBeforeDirectory = Directory(dirNameBuffer)
                        for count in range(abs(tabCountDif)): # go up
                            headDirectory = headDirectory.parent
                        addedBeforeDirectory.parent = headDirectory
                        headDirectory.children.append(addedBeforeDirectory)
                        dirNameBuffer = ''
                        prevTabCount = tabCount
                        tabCount = 0
                    elif (tabCountDif == 0):
                        headDirectory = addedBeforeDirectory.parent
                        addedBeforeDirectory = Directory(dirNameBuffer, headDirectory)
                        headDirectory.children.append(addedBeforeDirectory)
                        dirNameBuffer = ''
                        prevTabCount = tabCount
                        tabCount = 0 
                newLineCount += 1
                continue                            # we alredy added this char above in that case
            if char not in self.charsToIgnore and not charIndex == len(self.fileBuffer) - 1:
                dirNameBuffer += char
            charIndex += 1
        return baseDirectory

def createFolders(directoryTree, path, bIgnoreBaseRoot):
    dir = Directory("")
    iter: DirectoryIterator = ColumnDirectoryIterator(directoryTree)
    iterCount = 0
    #dirSize = directoryTree.size()
    while(dir is not None): # TODO compare with directory size
        if iterCount == 0 and bIgnoreBaseRoot: # ignore parent
            print(f"Ignoring base root")
            dir = iter.getNext()
            if len (directoryTree.children) == 0:
                print(f"Root {dir.name} has no children")
                return
            iterCount += 1
            continue
        dir = iter.getNext()
        if dir is not None:
            fullPath = path + "\\" + dir.getPath()
            Path(fullPath).mkdir(parents=True,exist_ok=True)
            iterCount += 1
        else:
            print("Dir is None")
            return
def printHelp():
    print("Arguments help:\n1. Directory where folders will be created (default is script's directory).\n\
2. Config file name to parse from (default is script's name + \'Config.txt\'). \n\
3. Config file directory (default is script's directory)\nCommands:\n-help -syntax")
def printSyntax():
    print("Syntax.\nEach line represents a folder. Paste tab before folder name to note that this folder is child of previous that has less tabs\
(if prev. line has same count of tabs, current line is not a child)\n\
Parent\n\tChild2\n\tChild3\n\tChild4\nNewParent\n\tChild1\n\tChild2\n\t\tChildOfChild\n\tChild3")
#returns list of args
def handleCmdArgs() -> list:
    mandArgc = 3
    argc = len(sys.argv) - 1
    result = []

    if argc == 0: # set defaults
        result.append(f"{os.path.dirname(__file__)}")
        result.append(Path(__file__).stem + "Config.txt")
        result.append(f"{os.path.dirname(__file__)}")
        return result

    if sys.argv[1] == "-help":
        printHelp()
        input("Press any key to exit")
        sys.exit(0)

    if sys.argv[1] == "-syntax":
        printSyntax()
        input("Press any key to exit")
        sys.exit(0)

    #handle missed args
    missedArgc = mandArgc - argc
    
    result.append(sys.argv[1])

    if missedArgc == 2: result.append(Path(__file__).stem + "Config.txt")
    else: result.append(sys.argv[2])

    if missedArgc == 1: result.append(f"{os.path.dirname(__file__)}")
    else: result.append(sys.argv[3])
    

    return result
#########################

#args: look printHelp()
args = handleCmdArgs()
parser = HierarchyParser(args[1], args[2])
tree = parser.parseHierarchy()
createFolders(tree, args[0], True)
