#!/usr/bin/env python

import sys
import tokenize
import token
import io
import subprocess


class functionObject:
    """
    Class represents a function that may be found
    within a file lint.py is checking
    """

    def setName(self, newName):
        """Sets the name of the function
        Args:
            newName : new name of the function
        """
        self.name = newName

    def setFoundDef(self, newFoundDef):
        """Sets whether or not the 'def' part of the function signature has been found
        Args:
            newFoundDef : a boolean representing whether
            or not the function's "def" was found.

        """
        self.foundDef = newFoundDef

    def appendToArguments(self, newArgument):
        """Adds to the list of found function arguments in the signature
        Args:
            newArgument : The new argument to add to the list.
        """
        self.arguments.append(newArgument)

    def hasName(self):
        """Checks to see if the name of the function has been found and set already
            Returns:
                namefound : boolean representing if the function name was set
        """
        namefound = self.name != ""
        return namefound

    def hasFoundDef(self):
        """Checks to see if 'def' part of the signature was found
            Returns:
                foundDef : a boolean that represents if
                the "def" part of the function was found
        """
        foundDef = self.foundDef
        return foundDef

    # The linter uses the indent level to check if t
    # he function being checked has started/ended
    def incrementIndent(self):
        """Increments the indent level
        """
        self.indentLevel += 1
        self.hasAtLeastOneIndent = True

    def decrementIndent(self):
        """Increments the indent level
        """
        self.indentLevel -= 1
        self.hasAtLeastOneDeIndent = True

    def isDone(self, currentLine=""):
        """Checks to see if the linter has reached the end of the function
        Args:
            currentLine : the current line that is being parsed
        Returns:
            done : boolean representing if the end of the function was reached
        """
        done = None
        if currentLine != "" and currentLine != "\n" and currentLine != "\t":
            """
             len(currentLine) : length of current line
             len(currentLine.lstrip() : length of line without
             leading whitespace, i.e. tabs and spaces
             (len(currentLine) - len(currentLine.lstrip())) : the indent
             level of the current line
             self.indentLevel represents the number of indents
             that preceded the function signature.
             if the indent level of the current line is the
             same as that of the function signature, the function is ended
            """
            self.done = self.indentLevel == (
                len(currentLine) - len(
                    currentLine.lstrip())) and currentLine != self.functionLine
            """
                print("Beginning indent: " + str(self.indentLevel) +
                " current indent: " + str(len(currentLine) -
                len(currentLine.lstrip())))
            """
            done = self.done and self.hasFoundDef()
        else:
            done = False
        return done

    def printArguments(self):
        """
        Prints the arguments found in the function argument list
        """
        print(
            "Recognized arguments for function " + self.name + ": " + str(
                self.arguments))

    def printReturns(self):
        """
        Prints all returns found in the function
        """
        print(
            "Recognized returns for function " + self.name + ": " + str(
                self.returns))

    def printDocStringData(self):
        """
        Calls the function that parses the docstring text
        """
        # print("Docstring text:")
        # for token in self.docStringText:
        # print(token.string, end=" ")
        # print("")
        self.parseDocStringData()

    def appendTextToDocStringData(self, text):
        """
        Args:
             text : The text to append to the
             docstring data of the function object
        """
        self.docStringText.append(text)

    def parseDocStringData(self):
        """
        Gets all arguments and returns in the docstring.
        Before this function was called, all text
        found within the scanned function's docstring
        has already been put in self.docStringText
        """
        previousToken = ""
        currentPrecedingSpaces = None
        returnPrecedingSpaces = None
        returnSectionStarted = False
        returnLine = ""
        argsPrecedingSpaces = None
        argsSectionStarted = False
        argsLine = ""

        # Iterates over every token
        for tokenized in self.docStringText:
            stripped = tokenized.string.strip()
            # Strips all preceding and following whitespace characters
            # print("previous token " + previousToken)
            # print(tokenized)
            currentPrecedingSpaces = len(tokenized.line) - len(
                tokenized.line.lstrip())
            if stripped == ":" and previousToken == "Args":
                # Starts getting the args section data.
                # Records indentation level of the Args: line
                # print("Args section started")
                argsSectionStarted = True
                argsPrecedingSpaces = len(tokenized.line) - len(
                    tokenized.line.lstrip())
                argsLine = tokenized.line
            elif argsSectionStarted and tokenized.line != argsLine:
                if argsPrecedingSpaces == currentPrecedingSpaces:
                    # If the current line's indentation level
                    # is the same as the start of Args...
                    argsSectionStarted = False
                    # print("Args section done")
                elif len(stripped) > 0 and tokenized.string == ":":
                    # While in the Args section, add anything
                    # in front of a : to the list of arguments.
                    self.docArguments.append(previousToken)
                    # print("Appending " + stripped)
            if stripped == ":" and previousToken == "Returns":
                # Same as args section but for returns
                # print("Args section started")
                returnSectionStarted = True
                returnPrecedingSpaces = len(tokenized.line) - len(
                    tokenized.line.lstrip())
                returnLine = tokenized.line
            elif returnSectionStarted and tokenized.line != returnLine:
                if returnPrecedingSpaces == currentPrecedingSpaces:
                    returnSectionStarted = False
                    # print("Args section done")
                elif len(stripped) > 0 and tokenized.string == ":":
                    self.docReturns.append(previousToken)
                    # print("Appending " + stripped)
            if tokenized.type == token.NAME or tokenized.type == token.OP:
                previousToken = stripped

        # print("Docstring arguments: " + str(self.docArguments))

        if "self" in self.arguments:
            if "self" not in self.docArguments:
                # print("Ignoring 'self' arg")
                self.arguments.remove("self")
        if len(self.arguments) != len(self.docArguments):
            self.errorOutput.append(self.name + ": line " + str(
                self.lineNo) + ": no. of arguments in function "
                "signature and no. of arguments "
                "in docstring are not the same.")
        # Checks to see if argslist items are in docstring

        # ********************************
        # This section just iterates over the list of
        # function arguments and docstring arguments
        # and checks to see if any item in one is missing in the other.
        # If a mismatch is found, it is appended to the errorOutput array
        for pos, argument in enumerate(self.arguments):
            if argument not in self.docArguments:
                self.errorOutput.append(
                    self.name + ": line " +
                    str(self.lineNo) + ": " + argument +
                    " is found in function signature's argslist"
                    ", but not in docstring")
            elif self.docArguments[pos] != argument:
                self.errorOutput.append(
                    self.name + ": line " + str(self.lineNo) +
                    ": " + argument +
                    " is argument no. " + str(pos) +
                    " in the function signature, but argument no. " +
                    str(pos) + " in docstring is " +
                    self.docArguments[pos])
        # Checks to see if docstring argslist items are in argslist
        for pos, argument in enumerate(self.docArguments):
            if argument not in self.arguments:
                self.errorOutput.append(self.name + ": line " + str(
                    self.lineNo) + ": " + argument +
                        " is found in docstring, "
                        "but not in function signature's argslist")

        # Checks to see if function return
        # values are in return list of docstring
        for returnVar in self.returns:
            if returnVar not in self.docReturns:
                self.errorOutput.append(
                    self.name + ": line " + str(self.lineNo) +
                    ": " + returnVar + " is returned in the function, "
                    "but is not found in the return section of the docstring")

        # Checks to see if docstring return values are returned by the function
        for returnVar in self.docReturns:
            if returnVar not in self.returns:
                self.errorOutput.append(
                    self.name + ": line " + str(self.lineNo) +
                    ": " + returnVar +
                    " is in the return section of the docstring, "
                    "but is not returned in the function")

        if len(self.docStringText) == 0:
            self.errorOutput.append(self.name + ": line " + str(
                self.lineNo) + ": " + "no docstring found")

    def clear(self):
        """
        Clears all values of the function object
        """
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
        self.startedDocString = False
        self.endDocString = False
        self.docStringText = []
        self.lineNo = 0
        self.fileName = ""
        self.errorOutput = []

    def __init__(self):
        """Initializes the function object's variables
        """
        self.clear()


def printFunctionData(func):
    # func.printArguments()
    # func.printReturns()
    func.printDocStringData()

    func.arguments.clear()
    func.docArguments.clear()
    func.returns.clear()
    func.docReturns.clear()
    func.docStringText.clear()
    # print("\n============****************************************============\n")


def getLineNumber(file, lineToCheck):
    """
    Gets the line number of a line in a specified file
    Args:
        file : the file that contains the line
        lineToCheck : the line to find the line number of
    Returns:
        pos : the line number of the line in the file. -1 if not found
    """
    pos = -1
    with open(file) as f:
        content = f.readlines()

    for counter, line in enumerate(content):
        if line.strip() == lineToCheck.strip():
            pos = counter + 1
            return pos

    return pos


def start_check(file):
    """
    Args:
        file: The current python script being scanned.
    Returns:
        errorOutput: The list of errors the linter found.
    """
    with open(file) as f:
        content = f.readlines()
    func = functionObject()
    previousToken = None
    func.fileName = file
    errorOutput = []
    for line in content:
        line = io.StringIO(line).readline
        token_generator = tokenize.generate_tokens(line)
        tokenized = None
        try:
            for tokenized in token_generator:
                # print(tokenized.string + "\t" +
                # token.tok_name.get(tokenized.type))
                # print(tokenized.string)
                # print(tokenized)
                if func.startedDocString and func.hasFoundDef():
                    func.appendTextToDocStringData(tokenized)
                elif tokenized.string == "def" and not func.hasFoundDef():
                    # If the current token is "def",
                    # then this is the start of a function
                    # Sets the hasFoundDef flag,
                    # which basically says the start
                    # of a function has been found
                    # Also records the indentation
                    # level of the function signature
                    func.setFoundDef(True)
                    func.functionLine = tokenized.line
                    func.lineNo = getLineNumber(file, tokenized.line)
                    # print(tokenized)
                    func.indentLevel = len(tokenized.line) - len(
                        tokenized.line.lstrip())
                elif not func.hasName() and func.hasFoundDef():
                    # The next token after a "def" is always the function name.
                    # Sets the function's name
                    func.setName(tokenized.string)
                    # print("function name:\t" + func.name)
                elif tokenized.string == "(" and func.hasName()\
                        and not func.startArguments:
                    # After the function name is the opening parentheses for
                    # the function's argument list
                    func.startArguments = True
                elif func.startArguments and not func.doneArguments:
                    # Appends to the list of function
                    # arguments until a ) is encountered
                    if tokenized.string == ")":
                        func.doneArguments = True
                    elif tokenized.string != "" and \
                        tokenized.type == token.NAME and \
                            (previousToken == "(" or previousToken == ","):
                                func.arguments.append(tokenized.string)
                elif previousToken == "return" and func.doneArguments:
                    # Adds anything found after
                    # "return" to the list of function arguments
                    func.returns.append(tokenized.string)
                if func.isDone(tokenized.line):
                    # Prints function data and clears the object
                    # print(tokenized)
                    # print("End of " + func.name + " reached!")
                    if func.name != "":
                        printFunctionData(func)
                        errorOutput.extend(func.errorOutput)
                    func.clear()
                    func = functionObject()
                    func.fileName = file

                    """A function may be like:
                    def func1():
                        ...
                    def func2():
                        ...
                    where there is no separating line b/w the end of the first
                    and the start of the second.
                    The following if statement accounts for that possibility.
                    """
                    if tokenized.string == "def":
                        func.setFoundDef(True)
                        func.functionLine = tokenized.line
                        func.lineNo = getLineNumber(file,
                                                    tokenized.line)
                        # print(tokenized)
                        func.indentLevel = len(tokenized.line) - len(
                            tokenized.line.lstrip())
                previousToken = tokenized.string
        except tokenize.TokenError:
            # This is raised on multi-line comments,
            # ie docstrings for some reason.
            if tokenized is not None:
                stripped = tokenized.line.strip()
                if stripped[
                   :3] == "\"\"\"" and not func.startedDocString:
                    func.startedDocString = True
                    # print("Docstring beginning")
                    # print(tokenized)
                elif stripped[
                     -3:] == "\"\"\"" and func.startedDocString:
                    func.startedDocString = False
                    # print("Docstring end")
    # This part executes when the EOF is reached.
    if not func.isDone():
        # If it reaches EOF, then the function is done,
        if func.name != "":
            printFunctionData(func)
            errorOutput.extend(func.errorOutput)
            func.clear()
    # returns the error output so that it may be printed
    return errorOutput
if len(sys.argv) == 1:
    print("Please provide a python script as an argument")
else:
    pep8Command = "pep8"
    pyFlakesCommand = "pyflakes"
    arguments = sys.argv
    pos = 0
    pep8Output = []
    pyflakesOutput = []
    scriptOutput = {}
    while pos < len(arguments):
        file = arguments[pos]
        if pos > 0:
            if file == "--test":
                arguments.append("code_style_test.py")
            # Allows the user to change the command to invoke pep8 and pyflakes
            elif file.startswith("--pep8invocation="):
                pep8Command = file[17:]
            elif file.startswith("--pyflakesinvocation="):
                pyFlakesCommand = file[21:]
            else:
                # Invokes pep8, pyflakes and then the linter itself.
                pep8Output.append(
                    subprocess.run(
                        [pep8Command, file],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True).stdout
                )
                pyflakesOutput.append(
                    subprocess.run([pyFlakesCommand, file],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True).stdout)
                scriptOutput[file] = start_check(file)
        pos += 1
    # Prints all the errors
    print("pep8 output:")
    for error in pep8Output:
        print(error)
    print()
    print("pyflakes output:")
    for error in pyflakesOutput:
        print(error)
    print()
    print("Script output:")
    print()
    for file in scriptOutput:
        fileErrors = scriptOutput.get(file)
        if len(fileErrors) > 0:
            print(file + ": ")
        for error in fileErrors:
            print("\t" + error)
        print()
