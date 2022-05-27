import numpy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm 
import astropy.io.fits as fits


fileName = '1322310160_20211130122222_ch143_02_out_t_genfrb0057.fits'
data = fits.open(fileName)
intensity = data[0].data
print(data.info())

plt.figure()
plt.imshow(intensity)
plt.show()


# Description of variables used in pixel search #
# realPath is the array holding the values of intensity in each pixel of the FRB's Path #
# x represents the pixel number in the x direction #
# y represents the pixel number in the y direction #
# Stop is used to stop the search. This occurs when the search reaches the edge of the dynamic spectrum, or when the value of the intensity drops to the point where it can be assumed the FRB has stopped #
# previousPath is used to stop the search from using a pixel twice, to ensure it continues searching new pixels. A value of zero means the pixel has not been used. The array is set to the same size as the array holding the fits file data #
# value holds the highest intensity value of the current search #
# xTemp is a temporary value for the x dimension of the highest intensity pixel of the search #
# yTemp is a temporary value for the y dimension of the highest intensity pixel of the search #

intensity = numpy.transpose(intensity)
realPath = numpy.zeros(0)
previousPath = numpy.zeros((intensity.shape[0],intensity.shape[1]))
x = 6532
y = 127
stop = 0

while stop == 0:
	value = 0
	xTemp = 0
	yTemp = 0
	

	# Search the pixel [x + 1][y] #
	if (x + 1) < intensity.shape[0] and (x + 1) >= 0 and (y) < intensity.shape[1] and (y) >= 0 and previousPath[x + 1][y] == 0:
		if intensity[x+1][y] > value:
			value = intensity[x+1][y]
			xTemp = x + 1
			yTemp = y

	# Search the pixel [x + 1][y - 1] #
	if (x + 1) < intensity.shape[0] and (x + 1) >= 0 and (y - 1) < intensity.shape[1] and (y - 1) >= 0 and previousPath[x + 1][y - 1] == 0:
                if intensity[x+1][y-1] > value:
                        value = intensity[x+1][y-1]
                        xTemp = x + 1
                        yTemp = y - 1

	# Search the pixel [x][y - 1] #
	if (x) < intensity.shape[0] and (x) >= 0 and (y - 1) < intensity.shape[1] and (y - 1) >= 0 and previousPath[x][y - 1] == 0:
                if intensity[x][y-1] > value:
                        value = intensity[x][y-1]
                        xTemp = x
                        yTemp = y - 1

	# Search the pixel [x - 1][y - 1] #
	if (x - 1) < intensity.shape[0] and (x - 1) >= 0 and (y - 1) < intensity.shape[1] and (y - 1) >= 0 and previousPath[x - 1][y - 1] == 0:
                if intensity[x - 1][y-1] > value:
                        value = intensity[x - 1][y-1]
                        xTemp = x - 1
                        yTemp = y - 1

	# Search the pixel [x - 1][y] #
	if (x - 1) < intensity.shape[0] and (x - 1) >= 0 and (y) < intensity.shape[1] and (y) >= 0 and previousPath[x - 1][y] == 0:    
            if intensity[x - 1][y] > value:
                        value = intensity[x - 1][y]
                        xTemp = x - 1
                        yTemp = y

	# Search the pixel [x - 1][y + 1] #
	if (x - 1) < intensity.shape[0] and (x - 1) >= 0 and (y + 1) < intensity.shape[1] and (y + 1) >= 0 and previousPath[x - 1][y + 1] == 0:
                if intensity[x - 1][y + 1] > value:
                        value = intensity[x - 1][y + 1]
                        xTemp = x - 1
                        yTemp = y + 1
	
	# Search the pixel [x][y + 1] #
	if (x) < intensity.shape[0] and (x) >= 0 and (y + 1) < intensity.shape[1] and (y + 1) >= 0 and previousPath[x][y + 1] == 0:
                if intensity[x][y + 1] > value:
                        value = intensity[x][y + 1]
                        yTemp = y + 1
                        xTemp = x

	# Search the pixel [x + 1][y + 1] #
	if (x + 1) < intensity.shape[0] and (x + 1) >= 0 and (y + 1) < intensity.shape[1] and (y + 1) >= 0 and previousPath[x + 1][y + 1] == 0:
                if intensity[x + 1][y + 1] > value:
                        value = intensity[x + 1][y + 1]
                        xTemp = x + 1
                        yTemp = y + 1

	if (xTemp == 0 or yTemp == 0):
		# Stop the search #
		stop = 1

	else:
		x = xTemp
		y = yTemp

		# Add the pixel to the path #
		previousPath[x][y] = 1

		print("")
		print("Pixel added is: [" + str(x) + "] [" + str(y) + "]")
		print("Intensity of this pixel is: " + str(value))
		realPath = numpy.append(realPath,value)

print(realPath)
	
