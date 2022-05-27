##################################################################################
## Ronan Phillips Johns 							##
## 19456317 									##
## getEndTime.py 								##
## This function finds the time that an FRB would end in the given frequency    ##
## range, from the given start time. Time is in seconds and frequency is in MHz ##
##################################################################################


##################################################################################
def getEndTime(startTime, dispMeasure, startFreq, endFreq):
	deltaTime = 4.15 * 10**(3) * (endFreq**(-2) - startFreq**(-2)) * dispMeasure
	endTime = startTime + deltaTime
	return endTime
##################################################################################

