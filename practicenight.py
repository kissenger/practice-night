import msvcrt
import sys
import winsound
import numpy as np
from methodslib import methodsLib
import re

optAnnotations = False

class keys():
	ARROWS = 224
	DOWN = 80
	LEFT = 75
	RIGHT = 77
	CTRL_C = 3
	
class style():
	BLUE = '\033[34m'
	RED = '\033[31m'
	UNDERLINE = '\033[4m'
	RESET = '\033[0m'
	WHITE = '\033[37m'
	GREY =  '\033[90m'
	
def beep():
	BEEP_MS = 200
	BEEP_HZ = 300
	winsound.Beep(BEEP_HZ, BEEP_MS)


# CallList
# Class to manage selection of 'bob' and 'single' calls
# Input: biases (Array): 3 element array defining the % plain, bob and single calls
# Note: biases must sum to 100, or the input is ignored and you will get a plain course
class CallList:

	def __init__(self, touchBiasArray):
		if touchBiasArray:
			plain = ['plain'] * touchBiasArray[0]
			bob = ['bob'] * touchBiasArray[1]
			single = ['single'] * touchBiasArray[2]
			self.touchCallList = [item for sublist in [plain, bob, single] for item in sublist]
		else:
			self.touchCallList = ['plain']

	def selectRandom(self):
		return np.random.choice(self.touchCallList)



# MethodsList
# Class to manage the methods requested by the user
# Input:  methodString (String): string defining the requested methods as abbreviations eg 'CYN'
class MethodsList:

	def __init__(self, methodsString):
		self.methodsArray = self.getMethods(methodsString)
		self.outputString = self.outputString()
		self.nMethods = len(self.methodsArray)

	def selectRandom(self):
		return self.methodsArray[np.random.randint(0, self.nMethods)]

	# getActiveMethods
	# Input:   str (String) = string defining the requested methods as abbreviations eg 'CYStN'
	# Returns: ams (Array) = array of Method instances from methodsLib
	def getMethods(self, str):
		strArr = re.split('(?=[A-Z])', str)[1:]
		ams = []
		for c in strArr:
			isFound = False
			for mdb in methodsLib:
				if mdb['abbr'] == c:
					ams.append(Method(mdb['name'], mdb['notation'], mdb['plain'], mdb['bob'], mdb['single'], mdb['stage']))
					isFound = True
					break
			if not isFound:
				print('WARNING: Could not find method with abbreviation ' + c) 
		return ams

	def outputString(self):
		na = ''
		for method in self.methodsArray:
			na += method.name + ', '
		return na[:-2]



# ErrorCounter
# Class to manage number of input errors across practiced leads
class ErrorCounter():
	
	def __init__(self):
		self.errorCount = 0
		self.nLines = 0

	def incrErr(self):
		self.errorCount += 1
		self.prnt()
	
	def incrLine(self):
		self.nLines += 1
		self.prnt()

	def prnt(self):
		sr = 100 if self.nLines == 0 else (1 - self.errorCount / self.nLines) * 100
		print(f'Errors: {self.errorCount:d}, Rows: {self.nLines:d}, Success rate: {sr:.1f}%', end = '      \r')



# Method
# Class to manage the unpacking of a method via its place notation
class Method:

	def __init__(self, name, notation, plain, bob, single, stage):
		self.name = name
		self.stage = stage
		self.notation = notation
		self.pnLead = self.pnLead()
		self.plain = self.pnLeadEnd(plain)
		self.bob = self.pnLeadEnd(bob)
		self.single = self.pnLeadEnd(single)
		self.nBells = self.nBells(self.stage)
		self.leadLength = self.leadLength()

	# pnFullLead
	# Combine the PN for standard lead with the desired lead-end
	def pnFullLead(self, call):
		return self.pnLead + [getattr(self, call)]

	# pnLeadEnd
	# Converts the lead-end place notation into an array of integers, eg '12' --> [1, 2]
	def pnLeadEnd(self, pn):
		return list(map(int, pn))

	# pnLead
	# Converts pn string to array
	# Input: pn (String) = place notation in the form: x58x16x12x38x14x58x16x78
	# Output: (Array) = place notation in array form: [[],[5,8]...]
	# **Note pn should exclude the comma and leadhead change	
	def pnLead(self):
	
		pna = []
		numbs = []
		for char in self.notation:
			
			if char in ["x", "."]:
				if len(numbs) > 0: pna.append(numbs)
				if char == "x": pna.append([])
				numbs = []
				
			elif char.isdigit():
				numbs.append(int(char))
			
		pna.append(numbs)
		pna.extend(pna[-2::-1])
		
		return pna
		
	# def isLeadEnd(self, rowNumb):
	# 	return rowNumb == self.leadLength - 1
		
	def nBells(self, stage):
		if stage == 'major': return 8
		if stage == 'triples': return 7
		if stage == 'minor': return 6
		if stage == 'doubles': return 5
		
	def leadLength(self):
		return len(self.pnLead) + 1

# startingSeq
# Returns string of charatcers defining the starting sequence of bells
# Inputs:  wb (Integer) = working bell
# Outputs: seq (String) = starting seqence of bells in the form '1...5...'
	def startingSeq(self, wb):

		seq = '1'
		for i in range(2, 9):
			if i == wb:
				seq += str(i)
			else:
				seq += '.'
				
		return seq
		




class Lead():

	def __init__(self, **kwargs):

		self.method  = kwargs['m'] if 'm' in kwargs else ''
		self.startSeq = kwargs['s'] if 's' in kwargs else ''

		if 'tl' in kwargs:
			self.touchList = kwargs['tl']
			self.touchCall = self.touchList.selectRandom()
		else:
			self.touchCall = 'plain'
   
		if 'ml' in kwargs:
			self.methodList = kwargs['ml']
			self.nextMethod = self.methodList.selectRandom()
			self.methodCall = self.nextMethod.name if self.nextMethod != self.method else ''
		else:
			self.methodCall = ''

		self.length = self.method.leadLength
		self.rows = self.rows()
		self.lastSeq = self.lastRow().seq
		self.endPlaceBell = self.lastRow().pos()

	def rows(self):
		seq = self.startSeq
		fullLeadPN = self.method.pnFullLead(self.touchCall)
		row = Row(seq, 0, self.length)
		rws = [row]
		for i, pn in enumerate(fullLeadPN):
			seq = row.nextSeq(pn)
			row = Row(seq, i+1, self.length)
			rws.append(row)
		return rws

	def lastRow(self):
		return self.rows[len(self.rows)-1]

	# Practice a Lead
	# Input: 	errors (ErrorCounter) - Instance of ErrorCounter class
	# Input:	firstLoop (Boolean) - False will suppress printing of first row - required for multiple leads
	def practice(self, errors, firstLoop):

		# __expectedKey
		# Returns: the input keystroke expected based on the direction of movement of the working bell
		def __expectedKey(pos, lastPos):
			if pos > lastPos:
				return keys.RIGHT
			elif pos < lastPos:
				return keys.LEFT
			else:
				return keys.DOWN

		# __waitForKey
		# Waits for user input and returns only when the expected keystroke is recieved
		# Returns: (Integer) - the number of input errors before correct input
		def __waitForKey(eks):

			isErr = False
			while True:
			
				ks = ord(msvcrt.getch())
				if ks == keys.ARROWS:
					ks = ord(msvcrt.getch())
					if ks == eks:
						return 
					else:
						if not isErr: errors.incrErr()
						isErr = True
						beep()
				
				elif ks == keys.CTRL_C:
					beep()
					print(style.RESET)
					print("SESSION CANCELLED")
					sys.exit()							

		for i, row in enumerate(self.rows):
			pos = row.pos()
			if i > 0:
				__waitForKey(__expectedKey(pos, lastPos))
			lastPos = pos
			if not firstLoop and i == 0:
				continue
			row.prnt(tc = self.touchCall, mc = self.methodCall)
			errors.incrLine()




class Row():
  
	def __init__(self, seq, rowNumber, leadLength):
		self.seq = seq 
		self.rowNumber = rowNumber
		self.leadLength = leadLength
		self.touchCallRow = self.leadLength - 3
		self.methodCallRow = self.leadLength - 2
		self.annotationRow = self.leadLength 
		self.isLeadEnd = rowNumber == leadLength - 1
		self.stroke = 'BS' if rowNumber % 2 == 0 else 'HS'

	# prnt
	# Input: (optional) tc = touchCall
	# Input: (optional) mc = methodCall
	def prnt(self, **kwargs):

		tc = kwargs['tc'] if 'tc' in kwargs else ''
		mc = kwargs['mc'] if 'mc' in kwargs else ''

		outp = ''
		pad = ' '
		outp += style.GREY + self.stroke + '   '
		if self.isLeadEnd and optAnnotations:
			outp += style.UNDERLINE
		
		for c in self.seq:
			if c == ".":
				outp += style.WHITE + c + pad
			elif c == "1":
				outp += style.RED + c + pad
			else:
				outp += style.BLUE + c + pad

		outp += style.RESET + self.callString(tc, mc)
		print(outp + '                              ')




	
# 	print('\033[K', end='')

# 	if nl % 2 == 0:
# 		backOrHand = 'BS'
# 	else:
# 		backOrHand = 'HS'
  
# 	print(style.GREY + '[' + str(nl).zfill(5) + '] ' + backOrHand + '   ', end = '')
	
# 	for c in s:
		
# 		if optUnderlineLeadend:
# 			if le:
# 				print(style.UNDERLINE, end = '')
# 			else:
# 				print(style.RESET, end = '')
			
# 		if c == "1":
# 			print(style.RED + "1", end = ' ')
# 		elif c == str(wb):
# 			print(style.BLUE + str(wb), end = ' ')
# 		else:
# 			print(style.WHITE + c, end = ' ')
	
# 	print(style.RESET + call)


	# callString
	# Returns a string to print to console at the appropriate point, warning of method change or touch call
	# tc (String) = touchCall - plain bob or single
	# mc (String) = methodCall - method at next lead end
	def callString(self, tc, mc):
		outp = ''
		if self.rowNumber == self.touchCallRow:
			if tc in ['bob', 'single']:
				outp += tc.upper() + '!'
		if self.rowNumber == self.methodCallRow:
			if mc:
				outp += mc.upper() + '!'
		return outp

	# nextSeq
	# Returns: next sequence based on transformation of the current row based on the provided place notation (as array)
	def nextSeq(self, pn):
		nr = ''
		j = 1
		while j <= 8:
			if j not in pn:
				nr += self.seq[j-1:j+1][::-1]
				j += 1
			else:
				nr += self.seq[j-1]
			j += 1
		return nr

	# pos	
	# Returns: postion of the working bell in the current row
	def pos(self):
		for i, c in enumerate(self.seq):
			if c not in ['1', '.']:
				return i + 1
