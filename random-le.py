# import os
# import sys, getopt
# import numpy as np
# import re
# #from practicenight import style, beep, pnStrToArr, getStartingSeq
# from practicenight import *


# # look for input arguments
# try:
# 	opts, args = getopt.getopt(sys.argv[1:],"m:b:t:f:",["methods="])
# except getopt.GetoptError:
# 	print('practice.py -m <methods>')
# 	sys.exit(2)

# forceMethodChange = False
# for opt, arg in opts:
# 	if opt in ("-m", "--methods"):
# 		methods = re.split('(?=[A-Z])', arg)

# activeMethods = getActiveMethods(methods)

# while True:
	
# 	# Select Method and place bell
# 	method = activeMethods[np.random.randint(0,len(activeMethods))]
# 	pb = np.random.randint(2,9)
# 	p = method.nextPB(pb, 'plain')
# 	b = method.nextPB(pb, 'bob')
# 	s = method.nextPB(pb, 'single')
# 	ans = str(p) + str(b) + str(s)
	
# 	while True:
# 		inp = input(str(pb) + "PB " + method.name.upper() + ": ")
# 		if len(inp) != 3:
# 			print("ERROR: Expected 3-character string")
# 		elif inp != ans:
# 			beep()
# 			print("Incorrect")
# 		else:
# 			break
# 	#else:



import os
import sys, getopt
import numpy as np
from practicenight import *

os.system('') 

# look for input arguments
try:
	opts, args = getopt.getopt(sys.argv[1:],"m:",["methods="])
except getopt.GetoptError:
	print('practice.py -m <methods>')
	sys.exit(2)

for opt, arg in opts:
	if opt in ("-m", "--methods"):
		methodsString = arg

methodsList = MethodsList(methodsString)
errors = ErrorCounter()
isFirstLead = True

while True:

	method = methodsList.selectRandom()
	bell = np.random.randint(2, method.nBells + 1)
	seq = method.startingSeq(bell)  
 
	lead = Lead(m = method, s = seq)
	print('========================                   ')
	print(str(bell) + 'pb ' + method.name)
	pb = input('Enter pb at end of lead: ')
	epb = lead.endPlaceBell
	if int(pb) != int(epb):
		beep()
		print(str(bell) + 'pb ' + method.name + ' ends in ' + str(epb) + ' pb')
	print('========================                   ')
 
	
	lead.practice(errors, isFirstLead)	


