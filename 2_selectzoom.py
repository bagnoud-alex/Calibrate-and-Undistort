import numpy as np
import cv2
import os

"""
This script must be run only after 1_calibrate.py has been run and parameters.py exists
This script is made to select the zoom parameter. 
Run this script, select an appropriate zoom and save it by clicking on the save trackbar
Note that the size of the image is not the real image size
"""

# Make sure the checkerboards images from 1_calibrate.py are in this folder
# ==========================================================
calibration_path = os.getcwd() + "/Calibration_Video/"
first_checker_path = calibration_path + "checkerboards/checker0.jpg"
# ==========================================================



print("---------------------------------------------------------------------")
# === LOADING PARAMETERS FROM parameters.py ===
import parameters
cameraMatrix = parameters.cameraMatrix
dist = parameters.dist
resize = parameters.resize
width = parameters.width
height = parameters.height
print("Parameters have been loaded from parameters.py")



# === LOADING IMAGE ===
checker = cv2.imread(first_checker_path)
if not os.path.isfile(first_checker_path):
	print("Error: Check input of this script, 'checker0.jpg' cannot be found at this address:")
	exit(first_checker_path)



# === IMAGE WINDOW ===
# Resizing the window so it is contained in the screen
cv2.namedWindow("Choose Zoom", cv2.WINDOW_AUTOSIZE)
size = (width, height)
ratio = width/height
window_size = (int(450*ratio), 450)



# === TRACKBARS DEFINITION ===
def nothing(a):
	pass

# Function saving selected zoom in parameters.py
def savezoom(a):
	# Saving undistorted image
	cv2.imwrite(calibration_path + "checker0_undistorted.jpg" , imgDist)
	# getting zoom value
	zoom = (cv2.getTrackbarPos("zoom", "Parameters")-50)/10
	# Reading parameters.py and editing zoom line
	lines = open("parameters.py", 'r').readlines()
	for l in range(len(lines)):
		if lines[l].startswith("zoom ="):
			lines[l] = ("zoom = %.1f \n" %zoom)
	out = open("parameters.py", 'w')
	out.writelines(lines)
	out.close()
	print("saved zoom parameter in 'parameter.py'")

# Trackbars
cv2.namedWindow("Parameters", cv2.WINDOW_NORMAL)
cv2.createTrackbar("zoom", "Parameters", 50, 100, nothing)
cv2.createTrackbar("Click bar to save zoom parameter", "Parameters", 0, 100, savezoom)
cv2.resizeWindow("Parameters", 400, 100)



# === REFRESHING TO UPDATE IMAGE WINDOW ===
print("Choose 'zoom' parameter on the slide bar and save on the trackbar")
print("press 'Q' to quit")
while True:

	# Getting new zoom value
	zoom = (cv2.getTrackbarPos("zoom", "Parameters")-50)/10
	# Applying new zoom param and undistorting
	newcameramatrix, _ = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, size, zoom, size)
	imgDist = cv2.undistort(checker, cameraMatrix, dist, None, newcameramatrix)

	# Printing undistorted image	
	imgDist_print = cv2.resize(imgDist, window_size)
	cv2.imshow("Choose Zoom", imgDist_print)
	if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'Q' to quit 
		cv2.destroyAllWindows()
		break

cv2.destroyAllWindows()




