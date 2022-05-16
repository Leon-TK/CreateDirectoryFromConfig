import sys

import fileSystemChecks as fsChecks

from .directory import IDirectory, Directory_Impl

class HierarchyParser():
    def __init__(self, configBuffer: str) -> None:
        self.cfgContent = configBuffer
        self.charsToIgnore = [' ', '\r']
        self.charsCauseError = [',', '!', '\\', '/', '$']
        self.hierarchyChar = '\t'
        self.newLineChars = ['\n']

    class ParseContext:
        def __init__(self) -> None:
            self.hierarchyDepth = 0 # '\t'
            self.prevHierarchyDepth = 0
            self.newLineCount = 0 # '\n'
            self.accumNameBuffer = ''
            self.rootDirectory = Directory_Impl('BASEITERNAL')
            self.currParentDirectory: IDirectory = None #current dir
            self.currDirectory: IDirectory = None
            self.charIndex = 0
            self.char = ''
            self.cfgContent = ''
            self.newLineChars = []
            self.charsToIgnore = []
            self.hierarchyChar = ''

        def IncrCharIndex(self):
            self.charIndex += 1

        def ProsessHierarchyChar(self) -> bool:
            self.hierarchyDepth += 1
            self.IncrCharIndex()
            return True

        def ProsessErrorChar(self):
            sys.exit(0)

        def ProsessNormalChar(self):
            self.accumNameBuffer += self.char
            self.IncrCharIndex()

        def ProsessLastChar(self) -> bool :
            if self.char in self.newLineChars or self.char in self.charsToIgnore or self.char in self.hierarchyChars: return True
            self.accumNameBuffer += self.char
            return False

        def ProsessEmptyBuffer(self):
            print("Missed folder name. You must write folder name at each line")
            sys.exit(0)

        def ClearNameBuffer(self):
            self.accumNameBuffer = ''

        def ResetHierarchyDepth(self):
            self.hierarchyDepth = 0

        def UpdatePrevHierarchyDepth(self):
            self.prevHierarchyDepth = self.hierarchyDepth
        
        def AppendAddedBeforeToChildren(self):
            self.currParentDirectory.children.append(self.currDirectory)
            self.currParentDirectory.size += 1
            
        def ProsessRootFolders(self):
            self.currParentDirectory = self.rootDirectory
            self.currDirectory = Directory_Impl(self.accumNameBuffer, self.currParentDirectory)
            self.Update()

        def Update(self):
            self.AppendAddedBeforeToChildren()
            self.ClearNameBuffer()
            self.UpdatePrevHierarchyDepth()
            self.ResetHierarchyDepth()

        def ProsessZeroDepthDelta(self):
            self.currParentDirectory = self.currDirectory.parent
            if not fsChecks.DirectoryNameCheck(self.accumNameBuffer):
                print("Invalid directory name has parsed")
                sys.exit(0)
            self.currDirectory = Directory_Impl(self.accumNameBuffer, self.currParentDirectory)
            self.Update()

        def ProsessPosDepthDelta(self, depthDelta):
            if depthDelta > 1: # cannot go further than 1 step
                print(f"Cannot create directory with depth greater than 1 than root")
                sys.exit(0)
            self.currParentDirectory = self.currDirectory
            if not fsChecks.DirectoryNameCheck(self.accumNameBuffer):
                print("Invalid directory name has parsed")
                sys.exit(0)
            self.currDirectory = Directory_Impl(self.accumNameBuffer, self.currParentDirectory)
            self.Update()

        def ProsessNegDepthDelta(self, depthDelta):
            # how many steps do we walk through upper dirs
            if not fsChecks.DirectoryNameCheck(self.accumNameBuffer):
                print("Invalid directory name has parsed")
                sys.exit(0)
            self.currDirectory = Directory_Impl(self.accumNameBuffer)

            for i in range(abs(depthDelta)): # go up
                self.currParentDirectory = self.currParentDirectory.parent
            
            self.currDirectory.parent = self.currParentDirectory
            self.Update()

        def CalcDepthDelta(self):
            return self.hierarchyDepth - self.prevHierarchyDepth

        def ProsessNestedFolders(self):
            depthDelta = self.CalcDepthDelta()

            if (depthDelta > 0): # folder will be nested in previous one
                self.ProsessPosDepthDelta(depthDelta)
            elif (depthDelta < 0): # folder will be nested in previous one that has lesser depth by 1
                self.ProsessNegDepthDelta(depthDelta)
            elif (depthDelta == 0): # folder will be nested in previous one that has lesser depth by 1
                self.ProsessZeroDepthDelta()

        def ProsessLine(self) -> bool:
            if self.charIndex == len(self.cfgContent) - 1:
                if self.ProsessLastChar(): return True
            else: self.IncrCharIndex() # \n is char

            if len(self.accumNameBuffer) == 0:
                self.ProsessEmptyBuffer()
            
            if self.hierarchyDepth == 0: # we are in base dir
                self.ProsessRootFolders()

            if self.hierarchyDepth > 0: # means than we go up or deeper relative to headdir
                self.ProsessNestedFolders()
            self.newLineCount += 1
            return True
    
    def isErrorChar(self, char) -> bool:
        return char in self.charsCauseError
    def isHierarchyChar(self, char) -> bool:
        return char == self.hierarchyChar
    def isNewlineChar(self, char) -> bool:
        return char in self.newLineChars
    def isLastChar(self, charIndex) -> bool:
        return charIndex == len(self.cfgContent) - 1 #TODO charIndex not updated evetytime
    def isIgnoreChar(self, char) -> bool:
        return char in self.charsToIgnore

    def parseHierarchy(self) -> IDirectory:
        context = HierarchyParser.ParseContext()
        context.cfgContent = self.cfgContent
        context.newLineChars = self.newLineChars
        context.charsToIgnore = self.charsToIgnore
        context.hierarchyChars = self.hierarchyChar
        
        # line is processd after "new line" is reached
        for char in self.cfgContent:
            context.char = char
            
            if self.isErrorChar(context.char):
                context.ProsessErrorChar()

            if self.isHierarchyChar(context.char):
                if context.ProsessHierarchyChar(): continue

            if self.isNewlineChar(context.char) or self.isLastChar(context.charIndex): # new line reach. process buffer between prev newline and this #TODO if end of file doesnt have \n the last line will not be saved
                if context.ProsessLine(): continue

            if not self.isIgnoreChar(context.char) and not self.isLastChar(context.charIndex):
                context.ProsessNormalChar()

        return context.rootDirectory
