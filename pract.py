
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
 
touchBias = None
workingBell = np.random.randint(2,9)

forceMethodChange = False
for opt, arg in opts:
	if opt in ("-m", "--methods"):
		methodsString = re.split('(?=[A-Z])', arg)
	if opt in ("-b", "--workingBell`"):
		workingBell = int(arg)
	if opt in ("-t", "--touchOptions"):
		touchBias = list(map(int, arg.split(',')))
		if sum(touchBias) != 100:
			print("WARNING: Touch biases must add up to 100 - ignoring input")
		else:
			touchCalls = TouchCallList(touchBias)

touchCalls = TouchCallList(touchBias)
methods = MethodsList(methodsString)
errorCount = 0

# nextSeq = getStartingSeq(workingBell)
nextMethod = methods.selectRandom()

# Tell user the starting bell and method
print('Starting Bell: ' + str(workingBell))
print('Starting Method: ' + nextMethod.name)
methodCall = nextMethod.name if nextMethod != nextMethod else None
touchCall = touchCalls.selectRandom()
nextSeq = nextMethod.startingSeq(workingBell)
lead = Lead(nextMethod, nextSeq, touchCall, methodCall)

while True:
	method = nextMethod
	seq = nextSeq
	nextMethod = methods.selectRandom()
	methodCall = nextMethod.name if method != nextMethod else None
	touchCall = touchCalls.selectRandom()
	lead = Lead(method, seq, touchCall, methodCall)
	nextSeq = lead.lastRow().seq
	errorCount = lead.practice(errorCount)





