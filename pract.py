
import os
import sys, getopt
from practicenight import *

os.system('') 

# look for input arguments
# try:
# 	opts, args = getopt.getopt(sys.argv[1:],"m:b:t:o:",["methods=","workingBell=","touchOptions=","options="])
# except getopt.GetoptError:
# 	print('practice.py -m <methods> -b <workingBell> -t <touchOptions> -o <options>')
# 	sys.exit(2)
 
# workingBell = np.random.randint(2,9)

# for opt, arg in opts:
# 	if opt in ("-m", "--methods"):
# 		methodsString = arg
# 	if opt in ("-b", "--workingBell`"):
# 		workingBell = int(arg)
# 	if opt in ("-t", "--touchOptions"):
# 		touchBias = list(map(int, arg.split(',')))
# 		if sum(touchBias) != 100:
# 			print("WARNING: Touch biases must add up to 100 - ignoring input")
# 		# else:
# 			# touchList = CallList(touchBias)


ms = input('Enter method(s): ')
methodsList = MethodsList(ms)

wb = input('Enter starting bell [random]: ')
if wb != '':
	workingBell = methodsList.validateWorkingBell(wb)
else:
	workingBell = methodsList.randomWorkingBell()

tb = input('Enter touch calls [plain course]: ')
touchList = CallList(tb)

options.showTreble = input('Show treble [No]: ') in ('y', 'Y')
options.showLeadend = input('Show leadend [No]: ') in ('y', 'Y')
options.showCourseBells = False
options.printOneRow = input('Show one row only [No]: ') in ('y', 'Y')


# touchList = CallList(touchBias)
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





