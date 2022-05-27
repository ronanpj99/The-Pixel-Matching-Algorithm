##################################################################################
## Ronan Phillips Johns 							##
## 19456317									##
## main.py									##
## This program has the role of finding the average chi-square value across a   ##
## whole FITS file. It uses an initial start time at pixel 0, and iterates      ##
## through the whole file, allowing each pixel to be the starting pixel. The    ##
## chi-square values are then averaged, and this average can be used to find a  ##
## limiting chi-square value that can hopefully allow us to determine whether   ##
## a candidate is an FRB. To use the program, a text file must contain the 	##
## names of all the candidate files, and a corresponding text file for each of  ##
## the file names which holds the list of candidates for the file. This text    ##
## file is provided by FREDDA, and should contain the DM, SNR, and start time   ##
## for each candidate. The text file wih the list of candidates must have the   ##
## same name as the FITS file, but with 'norm_sorted.cand' instead of 		##
## 'out_t.fits'.								##
##################################################################################


##################################################################################
# Imports needed for program 
import astropy
import astropy.io.fits as fits
import numpy
import matplotlib.pyplot as plt
import statistics
import glob, os
import csv
import pandas as pd
import getEndTime
import getPixels
import getStats
import getExpectedArray
import removePixels
import getChiSquare
##################################################################################


##################################################################################
# Loop through each file in the text file, so that each file can be analysed 
# seperately 
i = 0
with open("fileList.txt", 'r') as g:
	files = g.readlines()
	
	for fileName in files:
		fileName = fileName.replace('/\n','_out_t.fits')

		with open(fileName, 'r') as f:
			fileData = fits.open(fileName)
			data = fileData[0].data

			# These lists are used to hold all the high flux density pixels and chi-square   
			# values for each file
			distOnes = numpy.empty(0)
			distChiSquare = numpy.empty(0)


			# Allow the start pixel to be each pixel in the file, so that we can find the 
			# average chi-square across the file
			j = 0
	
			# Initially allow the startime to be zero 
			startTime = 0
			startFreq = int(fileData[0].header['NAXIS2']) - 1

			# Find the change in time and frequency that each pixel represents 
			deltaTime = fileData[0].header['CDELT1']
			deltaFreq = fileData[0].header['CDELT2']
	
			# Find the start frequency, and end frequency for the rectangles of analysis 
			startFreqValue = fileData[0].header['CRVAL2']
			endFreqValue = startFreqValue - startFreq * deltaFreq

			# Dispersion measure - use the average dispersion measure across the text file for
			# calculation of average and mean chi-square
			# Also store the candidate information in 'candidate' for later use
			# candidate[0] -> startTime
			# candidate[1] -> DM
			candidateST = numpy.empty(0)
			candidateDM = numpy.empty(0)
			fileName = fileName.replace('out_t.fits', 'norm_sorted.cand')
			dispMeasure = 0
			dispMeasureAv = 0
			with open(fileName, 'r') as ff:
				lines = ff.readlines()
				k = 0
				while k < len(lines) - 1:
					lineArray = str(lines[k]).split(' ')
					dispMeasure = dispMeasure + float(lineArray[5])
					candidateDM = numpy.append(candidateDM, float(lineArray[5]))
					candidateST = numpy.append(candidateST, float(lineArray[2]))
					k = k + 1
				dispMeasure = dispMeasure / k
				dispMeasureAv = dispMeasure
			ff.close
			
			# Call getEndTime so we can find the size of the time axes of the rectangle 
			timeSize = round(getEndTime.getEndTime(startTime * deltaTime, dispMeasure, startFreqValue, endFreqValue) / deltaTime)

			# We also want to record the total chi-square value for the file, so we can find the mean and STD
			chiSquareTotal = 0
			pixelTotal = 0

			# This loop iterates through the FITS file, allowing each pixel (in the top row)
			# to be the initial pixel	
			while j < (int(fileData[0].header['NAXIS1']) - timeSize + 1):
				startTime = j

				# Call getEndTime, which will return the end time for the rectangle in seconds 
				endTime = round(getEndTime.getEndTime(startTime * deltaTime, dispMeasure, startFreqValue, endFreqValue) / deltaTime)

				# Get the value of each pixel in the rectangle 
				pixelArray = getPixels.getPixels(startTime, endTime, startFreq, data)
			
				# Get the mean and standard deviation of the pixels in pixelArray 
				results = getStats.getStats(pixelArray)
				mean = results[0]
				sigma = results[1]

				# Create the array which holds the expected path of the FRB
				expectedArray = getExpectedArray.getExpectedArray(startTime, endTime, startFreq, startFreqValue, endFreqValue, deltaFreq, dispMeasure)

				# Remove all the pixels in pixelArray with a value less than mean + 3 * sigma 
				results = removePixels.removePixels(pixelArray, mean, sigma)
				pixelArray = results[0]
			
				distOnes = numpy.append(distOnes, results[1])

				# Find the chi-Square
				chiSquare = getChiSquare.getChiSquare(expectedArray, pixelArray)
				
				distChiSquare = numpy.append(distChiSquare, chiSquare)
					
				# Find the total chi-square	
				chiSquareTotal = chiSquareTotal + chiSquare

				# Output processing to screen 
				print("Processing " + fileName + " pixel " + str(j) + " of " + str(int(fileData[0].header['NAXIS1']) - timeSize))
				
				# Increase initial pixel for next loop iteration
				j = j + 1

			# Calculate results of iteration through FITS file 
			chiSquareAv = chiSquareTotal / (int(fileData[0].header['NAXIS1']) - timeSize)
			chiSquareSD = statistics.stdev(distChiSquare)
			limit = chiSquareAv - 3 * chiSquareSD


			# Plot the distribution of number of path pixels, and chi-square values 
			plt.figure(figsize =(16, 9))
			plt.subplot(121)
			plt.title('Total Number of High Flux Density Pixels')
			plt.xlabel('Start Time')
			plt.ylabel('Total')
			plt.grid()
			plt.plot(distOnes, marker = ',')
	
			plt.subplot(122)
			plt.title('Chi-squares')
			plt.xlabel('Start Time')
			plt.ylabel('Total')
			plt.annotate("Chi-square Lower Limit: " + str(limit), xy = (0.1, -0.1), xycoords = 'axes fraction')
			plt.grid()
			plt.plot(distChiSquare, marker = ',')

			
			plt.suptitle(fileName + "\nFunctions with respect to Time across FITS File")
			plt.savefig("/home/ronan/data/install/power/test/" + str(i) + ".png")
			plt.close()
	
			# Create text file to output results of candidate classification 
			with open("/home/ronan/data/install/power/test/results" + str(i) + ".txt", "w+") as ff:

				# Check the candidates and subsequently classify them
				ii = 0
				for ST in candidateST:
					startTime = int(ST)
					if int(candidateDM[ii]) == 0:
						dispMeasure = dispMeasureAv
					else:
						dispMeasure = candidateDM[ii]
					# Call getEndTime, which will return the end time for the rectangle in seconds
					endTime = round(getEndTime.getEndTime(startTime * deltaTime, dispMeasure, startFreqValue, endFreqValue) / deltaTime)

					# Get the value of each pixel in the rectangle
					pixelArray = getPixels.getPixels(startTime, endTime, startFreq, data)

					# Get the mean and standard deviation of the pixels in pixelArray
					results = getStats.getStats(pixelArray)
					mean = results[0]
					sigma = results[1]

					# Create the array which holds the expected path of the FRB
					expectedArray = getExpectedArray.getExpectedArray(startTime, endTime, startFreq, startFreqValue, endFreqValue, deltaFreq, dispMeasure)

					# Remove all the pixels in pixelArray with a value less than mean + 3 * sigma
					results = removePixels.removePixels(pixelArray, mean, sigma)
					pixelArray = results[0]

					# Find the chi-Square
					chiSquare = getChiSquare.getChiSquare(expectedArray, pixelArray)

					# Check the chi-square with the limit found above
					if chiSquare < limit:
						ff.write("\nCand" + str(ii) + " of DM: " + str(candidateDM[ii]) + ", start time: " + str(candidateST[ii]) + " is likely an FRB ")
					else:
						ff.write("\nCand" + str(ii) + " of DM: " + str(candidateDM[ii]) + ", start time: " + str(candidateST[ii]) + " is not likely an FRB ")
					ii = ii + 1	
			ff.close()
		f.close()
		i = i + 1
g.close()
##################################################################################
