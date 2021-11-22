
import os
import sys, getopt
import numpy as np
import re
#from practicenight import style, beep, pnStrToArr, getStartingSeq
from practicenight import *


os.system('')

# look for input arguments
try:
	opts, args = getopt.getopt(sys.argv[1:],"m:b:t:f:",["methods=","workingBell=","touchOptions="])
except getopt.GetoptError:
	print('practice.py -m <methods> -b <workingBell> -t <touchOptions>')
	sys.exit(2)

forceMethodChange = False
for opt, arg in opts:
	if opt in ("-m", "--methods"):
		requestedMethods = re.split('(?=[A-Z])', arg)
	if opt in ("-b", "--workingBell`"):
		workingBell = int(arg)
	if opt in ("-t", "--touchOptions"):
		touchBias = list(map(int, arg.split(',')))
		if sum(touchBias) != 100:
			print("WARNING: Touch biases must add up to 100 - ignoring input")
		else:
			plain = ['plain'] * touchBias[0]
			bob = ['bob'] * touchBias[1]
			single = ['single'] * touchBias [2]
			callOptions = [item for sublist in [plain, bob, single] for item in sublist]

		
try:
	workingBell
except:
	print('WARNING: No working bell provided, so chosing one at random')
	workingBell = np.random.randint(2,9)
	print('Working Bell = ' + str(workingBell))

try: 	
	callOptions
except:
	callOptions = ['plain']

activeMethods = getActiveMethods(requestedMethods)
for method in activeMethods:
	print(method.name)
nextMethod = activeMethods[0]

errorCount = 0
nLines = 0

#printRow(seq, workingBell, False, "    (" + str(pos) + "PB " + nextMethod.name + ")")
#printStatsLine(errorCount, nLines)


pos = workingBell
seq = getStartingSeq(workingBell)
printRow(nLines, seq, workingBell, False, '')
printStats(errorCount, nLines)

while True:

	# Select a method at random from list of active methods, and get notation
	method = nextMethod
	nextMethod = activeMethods[np.random.randint(0,len(activeMethods))]
	call = np.random.choice(callOptions)
	rows = method.Rows(seq, call)
	seq = rows[-1]
	
	#for i, row in enumerate(rows):
	for i, row in enumerate(rows):
	
		if i == 0: continue
			
		newPos = row.find(str(workingBell)) + 1
		
		
		if newPos > pos:
			expectedStroke = keys.RIGHT
		elif newPos < pos:
			expectedStroke = keys.LEFT
		else:
			expectedStroke = keys.DOWN
	
		errorCount += waitForExpectedKeystroke(expectedStroke)
		nLines +=1
  
		cs = method.callString(i, nextMethod, call, newPos)
		printRow(nLines, row, workingBell, method.isLeadEnd(i), cs)
		printStats(errorCount, nLines)
		
		
		pos = newPos
		#cs = callString(row, nextMethod, call, newPos)
		
		#printRow(row, workingBell, row == len(pna) - 2, cs)
		#printStatsLine(errorCount, nLines)

		
	#pna = pnStrToArr(method.notation, method.plain)
#	try:
#		touchCall = np.random.choice(touchList)
#	except:
#		touchCall = 'plain'
		
#	pna = method.fullLead(touchCall)

#	nextMethod = activeMethods[np.random.randint(0,len(activeMethods))]
	
#	row = 0 
	
#	while row < len(pna):

#		nextSeq = getNextSeq(pna[row], seq)
#		nextPos = nextSeq.find(str(workingBell)) + 1

#		if nextPos > pos:
#			expectedStroke = keys.RIGHT
#		elif nextPos < pos:
#			expectedStroke = keys.LEFT
#		else:
#			expectedStroke = keys.DOWN
		
#		errorCount += waitForExpectedKeystroke(expectedStroke)
#		nLines += 1
		
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
#			
#		printRow(nextSeq, workingBell, row == len(pna) - 2, call)
#		printStatsLine(errorCount, nLines)
		
#		seq=nextSeq
#		pos=nextPos
#		
#		row += 1
		

