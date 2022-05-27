##################################################################################
## Ronan Phillips Johns 							##
## 19456317 									##
## getStats.py 									##
## This function finds, from a given array of pixels, the mean pixel intensity  ##
## as well as the standard deviation of the intensities				##
##################################################################################


##################################################################################
def getStats(pixelArray):
	
	# First we find the total number of values contained in the array #
	number = pixelArray.shape[0] * pixelArray.shape[1]
	
	# Next we find the total sum value of all the pixels contained in the array #
	# To do this we use two nested loops #
	# Initialise variables first #
	i = 0
	j = 0
	totalValue = 0

	while i < pixelArray.shape[0]:
		while j < pixelArray.shape[1]:
			totalValue = totalValue + pixelArray[i][j]
			j = j + 1
		i = i + 1
		j = 0

	# We can now calculate the mean value of all the pixels #	
	if number == 0:
		number = 1
	mean = totalValue / number

	# From the mean we can calculate the standard deviation #
	# To do this we must once again loop through all the pixels in the array #
	# Again initialise variables #
	i = 0
	j = 0 
	meanTotal = 0

	while i < pixelArray.shape[0]:
		while j < pixelArray.shape[1]:
			if pixelArray.shape[0] > 1 and pixelArray.shape[1] > 1:
				meanTotal = meanTotal + (pixelArray[i][j] - mean)**2
			j = j + 1
		i = i + 1
		j = 0
	
	# Now, using the mean total, we can calculate the standard deviation #
	sigma = (meanTotal / number)**(1/2)

	# We want to export the mean and the standard deviation #
	return mean, sigma
##################################################################################
