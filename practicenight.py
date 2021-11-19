import msvcrt
import sys
import winsound
import os
from methodslib import methodsLib

optReminderAtLeadHead = False
optUnderlineLeadend = False

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
		#self.rows = self.rows()


	def isLeadEnd(self, rowNumb):
		return rowNumb == self.leadLength - 1
		
	def callString(self, n, nm, c, np):

		cs = ''
		if n == self.leadLength - 3:
			if c in ['bob', 'single']:
				cs += c.upper() + "!" 
		elif n == self.leadLength - 2:
			if nm.name != self.name:
				cs += nm.name.upper() + "! "
		elif n == self.leadLength:
			if optReminderAtLeadHead:
				cs += '(' + str(np) + 'PB ' + nm.name + ") "
			
		return cs

		
	def nBells(self, stage):
		if stage == 'major': return 8
		if stage == 'triples': return 7
		if stage == 'minor': return 6
		if stage == 'doubles': return 5
		
	def leadLength(self):
	
		return len(self.pnLead) + 1
		#n = self.nBells * 2
		#if self.clss in ['surprise', 'treble bob', 'delight']:
		#	n *= 2
		#return n
			
	#def callPosition(self):
#		if self.clss == 'principle'
		
	def rows(self, startSeq, call):
		seq = startSeq
		rs = [seq]
		for i, pn in enumerate(self.pnLead):
			seq = getNextSeq(pn, seq)
			rs.append(seq)
		seq = getNextSeq(getattr(self, call), seq)
		rs.append(seq)
		return rs
		
	def fullLead(self, call):
		return self.lead + [getattr(self, call)]
		
	# pnStrToArr
	# Convert pn string to array
	# Inputs:
	# 	pn (String) = place nottation in the form: x58x16x12x38x14x58x16x78
	# 		**Note pn should exclude the comma and leadhead change	
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
		
	def pnLeadEnd(self, pn):
	
		return list(map(int, pn))
	
#	def getRows(self, ss, pb, call):
		
#		seq = ss
#		rows = [[1, seq]]
#		for i, pn in enumerate(self.fullLead(call)):
#			seq = getNextSeq(pn, seq)
#			rows.append([i+2, seq])
		
#		return rows

	def nextPB(self, pb, call):
	
		seq = getStartingSeq(pb)
		for pn in self.fullLead(call):
			seq = getNextSeq(pn, seq)

		return seq.find(str(pb)) + 1
		
	class Row:
		def __init__(self, n, seq):
			self.n = n
			self.seq = seq
			
		#def colourPrint():
		# to do
		
#	class LeadRows:
#		def __init__(self, seq):
#		
#			self.startSeq = seq
#			self.rows = [Method.Row(1, seq)]
#			print(self.name)
#			for i, pn in enumerate(Method.lead):
#				seq = getNextSeq(pn, seq)
#				rows.append(Method.Row(i+2, seq))
		
# printRow
# print a formatted sequence with treble coloured red and working bell coloured blue
# Inputs:
#   nl (Integer) = line number
# 	s (String) = sequence of bells
#   le (Boolean) = True if this is the last row in the lead end (underlined)
#   wb (Integer) = working bell
#   call (String) = string to print after row (eg call for touch or change of method)
def printRow(nl, s, wb, le, call):
	
	print('\033[K', end='')

	if nl % 2 == 0:
		backOrHand = 'BS'
	else:
		backOrHand = 'HS'
  
	print(style.GREY + '[' + str(nl).zfill(5) + '] ' + backOrHand + '   ', end = '')
	
	for c in s:
		
		if optUnderlineLeadend:
			if le:
				print(style.UNDERLINE, end = '')
			else:
				print(style.RESET, end = '')
			
		if c == "1":
			print(style.RED + "1", end = ' ')
		elif c == str(wb):
			print(style.BLUE + str(wb), end = ' ')
		else:
			print(style.WHITE + c, end = ' ')
	
	print(style.RESET + call)


def printStats(ec, n):
	#print('Errors: ' + str(ec) + ', Rows: ' + str(n) + ', Success rate: ' + str(100-ec/n*100), end = '\r')
	if n == 0:
		sr = 100
	else:
		sr = (1-ec/n)*100
		
	print(f'Errors: {ec:d}, Rows: {n:d}, Success rate: {sr:.1f}%', end = '\r')
	
# getActiveMethods
# Inputs:
#	rms (Array) = requested methods - array of characters defining the short names of methods eg ['B', 'N', 'C']
# Outputs:
# 	amc (Array) = array of methods from methodsLib
def getActiveMethods(rms):
	ams = []
	for m in rms:
		isFound = False
		for mdb in methodsLib:
			if mdb['abbr'] == m:
				ams.append(Method(mdb['name'], mdb['notation'], mdb['plain'], mdb['bob'], mdb['single'], mdb['stage']))
				isFound = True
				break
		if not isFound:
			print('WARNING: Could not find method with abbreviation ' + m) 
	return ams
				

# getStartingSeq
# Returns string of charatcers defining the starting sequence of bells
# Only the treble and working bell are represented as numbers, other bells as "."	
# Inputs:
# 	wb (Integer) = working bell
# Outputs: 
# 	seq (String) = starting seqence of bells 
def getStartingSeq(wb):

	pos = wb - 1
	seq = "1"
	for i in range(2, 9):
		if i == wb:
			seq += str(i)
		else:
			seq += "."
			
	return seq

	
# nextSeq
# Return the next sequence of bells from the provided place notation for row
# Inputs:
# 	pn (Integer Array) = place notation for current change eg [3, 4]
#   s (String) = sequence for current row  eg '1..7....'
# Output:
#   ns(String) = sequence of bells for next row
def getNextSeq(pn, s):

	ns = ''
	j = 1
	while j <= 8:
		if j not in pn:
			ns += s[j-1:j+1][::-1]
			j += 1
		else:
			ns += s[j-1]
		j += 1
		
	return ns
	
	
# waitForExpectedKeystroke
# Inputs
# 	eks (Integer) = Expected Keystroke
def waitForExpectedKeystroke(eks):

	ne = 0
	
	while True:
	
		ks = ord(msvcrt.getch())
		
		if ks == keys.ARROWS:
			ks = ord(msvcrt.getch())
			if ks == eks:
				return ne
			else:
				ne = 1
				#printStatsLine(ne, nr)
				beep()
		
		elif ks == keys.CTRL_C:
			beep()
			print(style.RESET)
			print("SESSION CANCELLED")
			sys.exit()
			
# getCall
# returns a call (bob, single, change of method, or PB reminder)
# Inputs:
# 	r (Integer) = number of current row
#   lel (Integer) = length of lead end (number of rows per lead)
#   cm (method) = current method
#   nm (method) = next method
#   tc (touch call) = bob, single or plain


		
#		call=''
#		if row == len(pna) - 3:
#			if nextMethod != method:
#				call = "    " + nextMethod.name.upper() + "! "
#		elif row == len(pna) - 4:		
#			if touchCall in ['bob', 'single']:
#				call = "    " + touchCall.upper() + "! "
#		elif row == len(pna) - 1:
#			call = "    (" + str(nextPos) + "PB " + nextMethod.name + ") "
#		else:
#			call = ""		