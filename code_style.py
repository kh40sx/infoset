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

	def printDocStringData(self):
		print("Docstring text:")
		for token in self.docStringText:
			print(token.string, end=" ")
		print("")
		self.parseDocStringData()

	def appendTextToDocStringData(self, text):
		self.docStringText.append(text)

	def parseDocStringData(self):
		previousToken = ""
		currentPrecedingSpaces = None
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
			if tokenized.type == token.NAME or tokenized.type == token.OP:
				previousToken = stripped

		print("Docstring arguments: " + str(self.docArguments))
		if "self" in self.arguments:
			if not "self" in self.docArguments:
				print("Ignoring 'self' arg")
				self.arguments.remove("self")
		for argument in self.arguments:
			if argument not in self.docArguments:
				print("**********" + argument + " is found in " + self.name + " arglist, but not in docstring" + "**********")

	def clear(self):
		self.done = False
		self.functionLine = ""
		self.hasAtLeastOneIndent = False
		self.hasAtLeastOneDeIndent = False
		self.data = []
		self.foundDef = False
		self.name = ""
		self.arguments = []
		self.docArguments = []
		self.indentLevel = 0
		self.startArguments = False
		self.doneArguments = False
		self.startedDocString = False;
		self.endDocString = False;
		self.docStringText = []

	def __init__(self):
		self.clear()


def printFunctionData(func):
	func.printArguments()
	func.printDocStringData()
	func.arguments.clear()
	func.docArguments.clear()
	func.docStringText.clear()
	func.clear()
	print("\n============****************************************============\n")

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
					#print("Found Def!")
				elif not func.hasName() and func.hasFoundDef():
					func.setName(tokenized.string)
					print("function name:\t" + func.name)
				elif tokenized.string == "(" and func.hasName() and not func.startArguments:
					func.startArguments = True
				elif func.startArguments and not func.doneArguments:
					if tokenized.string == ")":
						func.doneArguments = True
					elif tokenized.string != "" and tokenized.type == token.NAME and (previousToken == "(" or previousToken == ","):
						func.arguments.append(tokenized.string)
				if func.isDone(tokenized.line):
					#print(tokenized)
					print("End of " + func.name + " reached!")
					if func.name != "":
						printFunctionData(func)
					func.clear()
					func = functionObject()
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
			if func.name != "":
				printFunctionData(func)

if len(sys.argv) == 1:
	print("Please provide a python script as an argument")
else:
	for pos, file in enumerate(sys.argv):
		if pos > 0:
			if file == "--test":
				file = "code_style_test.py"
			print(file)
			start_check(file)
