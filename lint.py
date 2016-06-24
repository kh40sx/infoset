#!/usr/bin/python

import sys
import tokenize
import token
import io

class functionObject:
    def setName(self, newName):
        self.name = newName
    def setFoundDef(self, newFoundDef):
        self.foundDef = newFoundDef
    def appendToArguments(self, newArgument):
        self.arguments.append(newArgument)
    def hasName(self):
        return self.name != ""
    def hasFoundDef(self):
        return self.foundDef
    def incrementIndent(self):
        self.indentLevel+=1
        self.hasAtLeastOneIndent = True
    def decrementIndent(self):
        self.indentLevel-=1
        self.hasAtLeastOneDeIndent = True
    def isDone(self, currentLine = ""):
        if currentLine != "" and currentLine != "\n" and currentLine != "\t":
            self.done = self.indentLevel == (len(currentLine) - len(currentLine.lstrip())) and currentLine != self.functionLine
            #print("Beginning indent: " + str(self.indentLevel) + " current indent: " + str(len(currentLine) - len(currentLine.lstrip())))
            return self.done and self.hasFoundDef()
        else:
            return False
    def printArguments(self):
        print("Recognized arguments for function " + self.name + ": " + str(self.arguments))

    def printReturns(self):
        print("Recognized returns for function " + self.name + ": " + str(self.returns))


    def printDocStringData(self):
        #print("Docstring text:")
        #for token in self.docStringText:
            #print(token.string, end=" ")
        #print("")
        self.parseDocStringData()

    def appendTextToDocStringData(self, text):
        self.docStringText.append(text)

    def parseDocStringData(self):
        previousToken = ""
        currentPrecedingSpaces = None
        returnPrecedingSpaces = None
        returnSectionStarted = False
        returnLine = ""
        argsPrecedingSpaces = None
        argsSectionStarted = False
        argsLine = ""
        for tokenized in self.docStringText:
            stripped = tokenized.string.strip()
            #print("previous token " + previousToken)
            #print(tokenized)
            currentPrecedingSpaces = len(tokenized.line) - len(tokenized.line.lstrip())
            if stripped == ":" and previousToken == "Args":
                #print("Args section started")
                argsSectionStarted = True
                argsPrecedingSpaces = len(tokenized.line) - len(tokenized.line.lstrip())
                argsLine = tokenized.line
            elif argsSectionStarted and tokenized.line != argsLine:
                if argsPrecedingSpaces == currentPrecedingSpaces:
                    argsSectionStarted = False
                    #print("Args section done")
                elif len(stripped) > 0 and tokenized.string == ":":
                    self.docArguments.append(previousToken)
                    #print("Appending " + stripped)
            if stripped == ":" and previousToken == "Returns":
                #print("Args section started")
                returnSectionStarted = True
                returnPrecedingSpaces = len(tokenized.line) - len(tokenized.line.lstrip())
                returnLine = tokenized.line
            elif returnSectionStarted and tokenized.line != returnLine:
                if returnPrecedingSpaces == currentPrecedingSpaces:
                    returnSectionStarted = False
                    #print("Args section done")
                elif len(stripped) > 0 and tokenized.string == ":":
                    self.docReturns.append(previousToken)
                    #print("Appending " + stripped)
            if tokenized.type == token.NAME or tokenized.type == token.OP:
                previousToken = stripped

#        print("Docstring arguments: " + str(self.docArguments))
        if "self" in self.arguments:
            if not "self" in self.docArguments:
                #print("Ignoring 'self' arg")
                self.arguments.remove("self")
        if len(self.arguments) != len(self.docArguments):
            print(self.name + ": no. of arguments in function signature and no. of arguments in docstring are not the same.")
        for pos, argument in enumerate(self.arguments):
            if argument not in self.docArguments:
                print(self.name + ": " + argument + " is found in function signature's argslist, but not in docstring")
            elif self.docArguments[pos] != argument:
                print(self.name + ": " + argument + " is argument no. " + str(pos) + " in the function signature, but argument no. " + str(pos) + " in docstring is " + self.docArguments[pos])

        for returnVar in self.returns:
            if returnVar not in self.docReturns:
                print(self.name + ": " + returnVar + " is returned in the function, but is not found in the return section of the docstring")

        for returnVar in self.docReturns:
            if returnVar not in self.returns:
                print(self.name + ": " + returnVar + " is in the return section of the docstring, but is not returned in the function")

        if len(self.docStringText) == 0:
            print(self.name + ": no docstring found")

    def clear(self):
        self.done = False
        self.functionLine = ""
        self.hasAtLeastOneIndent = False
        self.hasAtLeastOneDeIndent = False
        self.data = []
        self.foundDef = False
        self.name = ""
        self.arguments = []
        self.returns = []
        self.docArguments = []
        self.docReturns = []
        self.indentLevel = 0
        self.startArguments = False
        self.doneArguments = False
        self.startedDocString = False;
        self.endDocString = False;
        self.docStringText = []

    def __init__(self):
        self.clear()


def printFunctionData(func):
    #func.printArguments()
    #func.printReturns()
    func.printDocStringData()
    func.arguments.clear()
    func.docArguments.clear()
    func.returns.clear()
    func.docReturns.clear()
    func.docStringText.clear()
    func.clear()
    #print("\n============****************************************============\n")

def start_check(file):
    with open(file) as f:
        content = f.readlines()
    func = functionObject()
    previousToken = None
    for line in content:
        line = io.StringIO(line).readline
        token_generator = tokenize.generate_tokens(line)
        tokenized = None
        try:
            for tokenized in token_generator:
                #print(tokenized.string + "\t" + token.tok_name.get(tokenized.type))
                #print(tokenized.string)
                #print(tokenized)
                if func.startedDocString and func.hasFoundDef():
                    func.appendTextToDocStringData(tokenized)
                elif tokenized.string == "def" and not func.hasFoundDef():
                    func.setFoundDef(True)
                    func.functionLine = tokenized.line
                    #print(tokenized)
                    func.indentLevel = len(tokenized.line) - len(tokenized.line.lstrip())
                elif not func.hasName() and func.hasFoundDef():
                    func.setName(tokenized.string)
                    #print("function name:\t" + func.name)
                elif tokenized.string == "(" and func.hasName() and not func.startArguments:
                    func.startArguments = True
                elif func.startArguments and not func.doneArguments:
                    if tokenized.string == ")":
                        func.doneArguments = True
                    elif tokenized.string != "" and tokenized.type == token.NAME and (previousToken == "(" or previousToken == ","):
                        func.arguments.append(tokenized.string)
                elif previousToken == "return" and func.doneArguments:
                    func.returns.append(tokenized.string)
                if func.isDone(tokenized.line):
                    #print(tokenized)
                    #print("End of " + func.name + " reached!")
                    if func.name != "":
                        printFunctionData(func)
                    func.clear()
                    func = functionObject()
                    if tokenized.string == "def":
                        func.setFoundDef(True)
                        func.functionLine = tokenized.line
                        #print(tokenized)
                        func.indentLevel = len(tokenized.line) - len(tokenized.line.lstrip())
                previousToken = tokenized.string
        except tokenize.TokenError:
            #This is raised on multi-line comments, ie docstrings for some reason.
            if tokenized != None:
                stripped = tokenized.line.strip()
                if stripped[:3] == "\"\"\"" and not func.startedDocString:
                    func.startedDocString = True
                    #print("Docstring beginning")
                    #print(tokenized)
                elif stripped[-3:] == "\"\"\"" and func.startedDocString:
                    func.startedDocString = False
                    #print("Docstring end")

    if not func.isDone(): #If it reaches EOF and the function has finished listing arguments, then the function is done
                printFunctionData(func)

if len(sys.argv) == 1:
    print("Please provide a python script as an argument")
else:
    for pos, file in enumerate(sys.argv):
        if pos > 0:
            if file == "--test":
                file = "code_style_test.py"
            #print(file)
            start_check(file)
