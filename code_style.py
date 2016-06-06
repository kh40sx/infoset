#!/usr/bin/python

import sys
import tokenize
import token
import io

class functionObject:
	foundDef = False
	name = ""
	arguments = []
	indentLevel = 0
	startArguments = False
	doneArguments = False
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
	def decrementIndent(self):
		self.indentLevel-=1
	def isDone(self):
		return self.indentLevel == -1 and self.doneArguments

def start_check(file):
	with open(file) as f:
		content = f.readlines()
	func = functionObject()
	for line in content:
		line = io.StringIO(line).readline
		token_generator = tokenize.generate_tokens(line)
		try:
			for tokenized in token_generator:
				#print(tokenized.string + "\t" + token.tok_name.get(tokenized.type))
				print(tokenized.string)
				if tokenized.string == "def" and not func.hasFoundDef():
					func.setFoundDef(True)
					print("Found Def!")
				elif tokenized.type == token.INDENT and func.hasFoundDef():
					func.incrementIndent()
				elif tokenized.type == token.DEDENT and func.hasFoundDef():
					func.decrementIndent()
				elif not func.hasName() and func.hasFoundDef():
					func.setName(tokenized.string)
					print("Set function name!")
				elif tokenized.string == "(" and func.hasName() and not func.startArguments:
					func.startArguments = True	
				elif func.startArguments and not func.doneArguments:
					if tokenized.string == ")":
						func.doneArguments = True
					elif tokenized.string != "":
						func.arguments.append(tokenized.string)
				if func.isDone():
					print("Function is done!")	
					func = functionObject()
		except tokenize.TokenError:
			pass	
	if not func.isDone(): #If it reaches EOF and the function has finished listing arguments, then the function is done
		print("Function is done!")	

if len(sys.argv) == 1:
	print("Please provide a python script as an argument")
else:
	for pos, file in enumerate(sys.argv):
		if pos > 0:
			print(file)
			start_check(file)
