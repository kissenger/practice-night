
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
	try:
		pb = input('Enter pb at end of lead: ')
	except:
		beep()

		print("\nSESSION CANCELLED")
		sys.exit()
	epb = lead.endPlaceBell
	if int(pb) != int(epb):
		beep()
		print(str(bell) + 'pb ' + method.name + ' ends in ' + str(epb) + ' pb')
	print('========================                   ')
 
	
	lead.practice(errors, isFirstLead)	


