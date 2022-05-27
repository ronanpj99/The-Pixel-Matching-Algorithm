##################################################################################
## Ronan Phillips Johns 							##
## 19456317 									##
## getChiSquare.py 								##
## This function simply finds the chi-square of the difference between the 	##
## position that high flux pixels lie in, and their expected position if they   ##
## represent an FRB								##
##################################################################################


##################################################################################
def getChiSquare(expectedArray, pixelArray):
	
	# Loop through the arrays and find the chisquare associated with each pixel position relative to the expected position #
	# Create nested loop #
	i = 0
	j = 0
	chiSquare = 0
		
	while i < pixelArray.shape[0]:
		expectedPosition = 0
		check = 0
	
		# Find the expected position of the FRB for this index #
		k = 0
		while k < expectedArray.shape[1]:
			if expectedArray[i][k] == 1:
				expectedPosition = k
			k = k + 1
			if expectedPosition == 0:
				expectedPosition = 1
		
		# Find the actual position of the high flux pixels and compute the chi-square #
		j = 0
		while j < pixelArray.shape[1]:				
			if pixelArray[i][j] == 1:
				chiSquare = chiSquare + (j - expectedPosition)**(2) / expectedPosition			
				check = 1
			j = j + 1

		# If none of the pixels have a significant flux in this index, assume maximum distance from the expected path #
		if check == 0:
			chiSquare = chiSquare + (expectedArray.shape[1])**(2)
		i = i + 1

	# Export the chiSquare value only #
	return chiSquare
##################################################################################
