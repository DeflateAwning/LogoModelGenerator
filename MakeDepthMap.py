#!/usr/bin/env python3

import cv2
import numpy as np
import os, sys, time

from tkinter import Tk
from tkinter.filedialog import askopenfilename

DEBUG = True
colorTolerance = 10 # must be within +- this many RGB values (out of 256), otherwise considered background (i.e. the first color selected)
scadTemplateFile = "LogoSCADTemplate.scad"
rescaleImageLength = 800
s3dScriptLine = '{REPLACE "\\n; layer !!, Z = " "; layer !!\\nG28 Y0 X0\\nM300\\nM25\\nG92 E0\\nG28 Y0 X0\\n; layer !! "}'
s3dLayerThickness = 0.3

print("Welcome to the 3D Printing Logo Model Generator.")
print("To begin, select an image to use as the logo (ideally landscape).")

Tk().withdraw()
inputFilename = askopenfilename(initialdir=os.getcwd(), title="Select the logo image file.")

print("You've selected the following file: " + inputFilename)

# Ask some questions
settings = {}
try:
	settings["finalLength"] = int(input("What is the final length of the model, in mm (default: 160): "))
except ValueError:
	settings["finalLength"] = 160
	print("Default width of 160mm chosen.")

try:
	settings["baseDepth"] = float(input("What is the base depth of the model, in mm (default: 8.1): "))
except ValueError:
	settings["baseDepth"] = 8.1
	print("Default depth of 8.1mm chosen.")

try:
	settings["incrementalDepth"] = float(input("What is the depth between each color in the model (default: 1.5mm): "))
except ValueError:
	settings["incrementalDepth"] = 1.5
	print("Default incremental depth of 1.5mm chosen.")

# Read the image
img = cv2.imread(inputFilename)
img = cv2.resize(img, (rescaleImageLength, int(round(rescaleImageLength * img.shape[0] / img.shape[1]))))
settings["origWidth"] = img.shape[0]
settings["origLength"] = img.shape[1]

# Show the image to get the correct colors
print("Click on each color in the image being shown, starting with the background color, moving to the colors you'd like to be shown the highest (generally from most area to least area).")
print("Press any key when you have selected all the colors.")

selectedColors = [] # Note: these colors are tuples in BGR or BGRA

def selectPointClick(event, x, y, flags, param):
	global selectedColors
	if event == cv2.EVENT_LBUTTONDOWN:
		# mouse clicked on a color
		selectedColors.append(list(img[y][x]))

		print("Selected color (B G R): " + str(img[y][x]))

windowName = "Image Color Selection"
cv2.namedWindow(windowName)
cv2.imshow(windowName, img)
cv2.setMouseCallback(windowName, selectPointClick)

key = 0
while not key:
	cv2.imshow(windowName, img)
	key = cv2.waitKey(0)

cv2.destroyAllWindows()

if DEBUG:
	print("Selected colors: " + str(selectedColors))

if len(selectedColors) >= 2:
	print("Good job! You selected {} colors.".format(len(selectedColors)))
else:
	print("You only selected {} colors, which isn't enough. Try again from the start.".format(selectedColors))
	sys.exit()

print("Hold on a second while the output file is generated.")
startTime = time.time()

# Determine the output file names
outputName = os.path.basename(inputFilename)
outputName = ".".join(outputName.split(".")[:-1]) # remove the extension
settings["scadFilename"] = outputName + ".scad"
settings["textFilename"] = outputName + ".txt"

# Generate the text file
selectedColors.reverse()
outputList = []
for i in img:
	thisRow = []
	for j in i:
		thisBGR = list(j)

		# Determine which depth to use
		for targetColor in selectedColors: # reverse so that the background (default) color is last
			thisColorMatchCount = 0
			for colorElementIndex in range(0, 3):
				if (targetColor[colorElementIndex] - colorTolerance <= thisBGR[colorElementIndex] <= targetColor[colorElementIndex] + colorTolerance):
					# this color element matches
					thisColorMatchCount += 1
			if thisColorMatchCount == 3:
				# this color matches
				break

		# targetColor is now the correct color, figure out which depth it's at
		thisDepth = settings["baseDepth"] + settings["incrementalDepth"] * (len(selectedColors) - selectedColors.index(targetColor))
		thisRow.append(thisDepth)

	outputList.append(thisRow)

# Write out the text file
with open(settings["textFilename"], "w") as f:
	for row in outputList:
		f.write(" ".join([str(i) for i in row]))
		f.write("\n")

# Read in template SCAD file
with open(scadTemplateFile) as f:
	scadOut = f.read()

# Replace all the settings into the SCAD file
for key in settings.keys():
	scadOut = scadOut.replace("!{}!".format(key), str(settings[key]))

# Write out the new scad file
with open(settings["scadFilename"], 'w') as f:
	f.write(scadOut)

# Print the all done message, with next steps
print("All done generating the files in {:.2f} seconds.".format(time.time()-startTime))

# Figure out where the layer pauses should be
layerPauseDepths = []
for i in range(len(selectedColors)):
	thisPauseDepth = settings["baseDepth"] + settings["incrementalDepth"] * (i + 0.5)
	layerPauseDepths.append(thisPauseDepth)

print("Pause the layers at: " + ", ".join([str(i) for i in layerPauseDepths]))

print("Use the following Simplify 3D Script to add pausing on the correct layers, assuming {}mm layers.".format(s3dLayerThickness))
for i in layerPauseDepths:
	print(s3dScriptLine.replace('!!', str(int(round(i/s3dLayerThickness)))))

print("All done.")
