
import os
import sys, getopt
import numpy as np
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
		methodsString = arg
	if opt in ("-b", "--workingBell`"):
		workingBell = int(arg)
	if opt in ("-t", "--touchOptions"):
		touchBias = list(map(int, arg.split(',')))
		if sum(touchBias) != 100:
			print("WARNING: Touch biases must add up to 100 - ignoring input")
		else:
			touchList = CallList(touchBias)

touchList = CallList(touchBias)
methodsList = MethodsList(methodsString)
errors = ErrorCounter()
isFirstLead = True

while True:

	if isFirstLead:
		method = methodsList.selectRandom()
		seq = method.startingSeq(workingBell)  
		print('========================')
		print('Selected Methods: ' + methodsList.outputString)
		print('Starting Method: ' + method.name)
		print('Bell: ' + str(workingBell))
		print('========================')
  
	lead = Lead(m = method, s = seq, tl = touchList, ml = methodsList)
	lead.practice(errors, isFirstLead)	

	seq = lead.lastSeq
	method = lead.nextMethod
	isFirstLead = False





