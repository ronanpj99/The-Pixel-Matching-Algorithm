##################################################################################
## Ronan Phillips Johns 							##
## 19456317 									##
## getExpectedArray.py 								##
## This function finds the pixels that an FRB would occupy, given an initial    ##
## time and frequency. As stated below, a value of 1 indicates that the FRB     ##
## would occupy this pixel, and a value of 0 does not 				##
##################################################################################


##################################################################################
import numpy

def getExpectedArray(startTime, endTime, startFreq, startFreqValue, endFreqValue, deltaFreq, dispMeasure):
	
	# First we create the array which will hold the expected path of the FRB #
	# A value of zero means the FRB isn't expected to be there #
	# A value of one means the FRB is expected to be there #
	expectedArray = numpy.zeros([startFreq + 1, endTime - startTime + 1])
	# We are going to iterate through each time step of the data, and match the expected frequency of the next pixel to the corresponding location in the array #
	# First allow freq1 to equal the initial frequency of the FRB path # 
	# Initialise the loop variable i #
	# The variable 'time' is used to determine which pixel on the time axis of the array the expected FRB path lies # 
	freq1 = startFreqValue
	i = 0	
	time = 0
	expectedArray[startFreq][0] = 1
	expectedArray[0][endTime - startTime] = 1
	# We can now create two nested loops to iterate through the array #
	while i < expectedArray.shape[0] - 1:

		# Allow the frequency to change from the maximum frequency to the minimum frequency #
		freq2 = freq1 - deltaFreq

		# Now use the dispersion measure equation given in the Handbook of Pulsar Astronomy (*Note - need to reference*) #
		deltaTime = 4.15 * 10**(5) * dispMeasure * (freq2**(-2) - freq1**(-2))
		freq1 = freq2
		time = time + deltaTime
		# Change this pixel to equal 1, so that it reflects the expected FRB path #
		expectedArray[startFreq - i][round(time)] = 1
		i = i + 1
	
	# Export only the expected array #
	return expectedArray
##################################################################################
