import msvcrt
import sys
import winsound
import numpy as np
import random
from methodslib import methodsLib
import re

class options():
  pass
	# showLeadend = False
	# showTreble = True
	# printOneRow = False
	# showCourseBells = False

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

def printError(msgString):
	beep()
	print(msgString)
	sys.exit()

# CallList
# Class to manage selection of 'bob' and 'single' calls
# Input: biases (Array): 3 element array defining the % plain, bob and single calls
# Note: biases must sum to 100, or the input is ignored and you will get a plain course
class CallList:

	def __init__(self, tbString):
		if tbString != '':
			touchBiasArray = list(map(int, tbString.split(',')))
			if sum(touchBiasArray) != 100:
				printError('Error: Touch call ratios must add up to 100')
			self.touchCalls = 'p' * touchBiasArray[0] + 'b' * touchBiasArray[1] + 's' * touchBiasArray[2]
		else:
			self.touchCalls = 'p'


	def selectRandom(self):
		# try:
			call = random.choice(self.touchCalls)
			return 'plain' if call == 'p' else 'bob' if call == 'b' else 'single'
		# except:
		# 	return 'plain'


# MethodsList
# Class to manage the methods requested by the user
# Input:  methodString (String): string defining the requested methods as abbreviations eg 'CYN'
class MethodsList:

	def __init__(self, methodsString):
		self.methodsArray = self.getMethods(methodsString)
		self.stage = self.methodsArray[0].stage
		self.nBells = self.methodsArray[0].nBells
		self.outputString = self.outputString()
		self.nMethods = len(self.methodsArray)
		self.validate()
	
	def validateWorkingBell(self, wb):
		if not wb.isnumeric():
			printError('Error: Working bell outside limits')
		elif int(wb) < 2 or int(wb) > self.nBells:
			printError('Error: Working bell outside limits')
		else:
			return int(wb)
   
	def randomWorkingBell(self):
		return np.random.randint(2,self.nBells+1)


	def selectRandom(self):
		return random.choice(self.methodsArray)
		# return self.methodsArray[np.random.randint(0, self.nMethods)]

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
					ams.append(Method(mdb['name'], mdb['notation'], mdb['bob'], mdb['single'], mdb['stage']))
					isFound = True
					break
			if not isFound:
				print('WARNING: Could not find method with abbreviation ' + c)
		return ams

	def validate(self):
		
		if not all(x.stage==self.stage for x in self.methodsArray):
			printError('ERROR: All methods must have the same stage (number of bells)')
		elif len(self.methodsArray) == 0:
			printError('ERROR: No methods found')
		else:
			return


				

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

	def __init__(self, name, notation, bob, single, stage):
		self.name = name
		self.stage = stage
		self.plain = self.__pnArray(notation)
		self.bob = self.applyBobOrSingle(bob)
		self.single = self.applyBobOrSingle(single)
		self.nBells = self.nBells(self.stage)
		self.leadLength = self.leadLength()
		# self.callLocation = self.callLocation()
		self.callOffset = max(len(self.__pnArray(bob)), len(self.__pnArray(single)))
		

	# Replace the last elements in place array with elemtents in bob or single place string
	def applyBobOrSingle(self, pn):
		pna = self.__pnArray(pn)
		return self.plain[:-len(pna)] + pna

	# pnArray
	# Converts pn string to array
	# Input: pn (String) = place notation in the form: x58x16x12x38x14x58x16x78
	# Output: (Array) = place notation in array form: [[],[5,8]...]
	# **Note pn should exclude the comma and leadhead change
	def __pnArray(self, pn):

		# Private function applyPal.... - does what it says on the tin
		def __applyPalendromicSymmetry(arr):
			arr.extend(arr[-2::-1])
			return arr

		# Private function notationT.... - converts string based place notation to an array
		def __notationToArray(pn):

			numbs = []
			pna = []

			for char in pn:

				if char in ['x', '.']:
					if len(numbs) > 0: pna.append(numbs)
					if char == 'x': pna.append([])
					numbs = []

				elif char.isdigit():
					numbs.append(int(char))

			pna.append(numbs)

			return pna

		# main routine
		parts = pn.split(',')
		outArr = []

		for part in parts:
			arr = __notationToArray(part)
			if len(part) > 5:
				arr = __applyPalendromicSymmetry(arr)
			outArr.extend(arr)

		return outArr

	def nBells(self, stage):
		if stage == 'major': return 8
		if stage == 'triples': return 7
		if stage == 'minor': return 6
		if stage == 'doubles': return 5

	def leadLength(self):
		return len(self.plain) + 1

# startingSeq
# Returns string of charatcers defining the starting sequence of bells
# Inputs:  wb (Integer) = working bell
# Outputs: seq (String) = starting seqence of bells in the form '1...5...'
	def startingSeq(self, wb):

		beforeBell = 0
		afterBell = 0
		if options.showCourseBells:
			coursingOrder = [7,5,3,2,4,6,8]
			indx = coursingOrder.index(wb)
			if indx == 0:
				beforeBell = coursingOrder[-1]
				afterBell = coursingOrder[1]
			elif indx == len(coursingOrder)-1:
				beforeBell = coursingOrder[-2]
				afterBell = coursingOrder[0]
			else:
				beforeBell = coursingOrder[indx-1]
				afterBell = coursingOrder[indx+1]

		seq = '1' if options.showTreble else '.'

		for i in range(2, self.nBells + 1):
			if i == wb:
				seq += str(i)
			elif i == beforeBell:
				seq += 'B'
			elif i == afterBell:
				seq += 'A'
			else:
				seq += '.'

		return seq




class Lead():

	def __init__(self, **kwargs):

		self.method  = kwargs['m'] if 'm' in kwargs else ''
		self.startSeq = kwargs['s'] if 's' in kwargs else ''

		# tl = touchList
		if 'tl' in kwargs:
			self.touchList = kwargs['tl']
			self.touchCall = self.touchList.selectRandom()
		else:
			self.touchCall = 'p'

		# ml = methodList
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
		pnArr =  getattr(self.method, self.touchCall)
		row = Row(seq, 0, self.method)
		rws = [row]
		for i, pn in enumerate(pnArr):
			seq = row.nextSeq(pn)
			row = Row(seq, i+1, self.method)
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
					print(style.RESET)
					printError("SESSION CANCELLED")

		for i, row in enumerate(self.rows):
			pos = row.pos()
			# print(pos)
			if i > 0:
				__waitForKey(__expectedKey(pos, lastPos))
			lastPos = pos
			if not firstLoop and i == 0:
				continue
			row.prnt(tc = self.touchCall, mc = self.methodCall)
			errors.incrLine()




class Row():

	def __init__(self, seq, rowNumber, method):
		self.seq = seq
		self.rowNumber = rowNumber
		self.leadLength = method.leadLength
		self.touchCallRow = self.leadLength - method.callOffset - 3
		self.methodCallRow = self.touchCallRow + 1
		self.annotationRow = self.leadLength
		self.isLeadEnd = rowNumber == self.leadLength - 1
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

		if self.isLeadEnd and options.showLeadend:
			outp += style.UNDERLINE

		for c in self.seq:
			if c in ('.', 'B', 'A'):
				outp += style.WHITE + c + pad
			elif c == "1":
				outp += style.RED + c + pad
			else:
				outp += style.BLUE + c + pad

		outp += style.RESET + self.callString(tc, mc)
		if options.printOneRow:
			print("\033[F\033[J", end="")
		print(outp + '                              ')



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
		# print(self.seq)
		for i, c in enumerate(self.seq):
			if c not in ['1', '.', 'A', 'B']:
				return i + 1
