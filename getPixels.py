##################################################################################
## Ronan Phillips Johns 							##
## 19456317 									##
## getPixels.py 								##
## This function simply finds and stores the pixels that are within a given     ##
## time and frequency range							##
##################################################################################


##################################################################################
import numpy

def getPixels(startTime, endTime, startFreq, data):
	
	# Create an array to hold all the pixel values #
	pixelArray = numpy.empty([startFreq, endTime - startTime])
	
	# Initialise the variables for the loops #
	i = 0
	j = 0
	
	# Create two nested loops to get the value of each pixel in the desired area #
	# We start grabbing data from the bottom of the frequency axis - opposite to where the FRB starts # 
	while i < pixelArray.shape[0]:
		while j < pixelArray.shape[1]:
			if i < data.shape[0] and (startTime + j) < data.shape[1]:
				pixelArray[i][j] = data[i][startTime + j]
			j = j + 1
		i = i + 1
		j = 0

	# Export the array only #
	return pixelArray			
##################################################################################
