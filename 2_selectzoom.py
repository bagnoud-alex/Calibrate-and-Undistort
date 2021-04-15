import numpy as np
import cv2
import os

print("---------------------------------------------------------------------")

# Loading parameters from parameters.py
import parameters
cameraMatrix = parameters.cameraMatrix
dist = parameters.dist
width = parameters.width
height = parameters.height
# imgPoints = parameters.imgPoints
print("Parameters have been loaded from parameters.py")

path_checkerboards = os.getcwd() + "/CheckerboardVideo/checkerboards/"
first_image = path_checkerboards + os.listdir(path_checkerboards)[0]


# Image window
cv2.namedWindow("Choose Zoom", cv2.WINDOW_NORMAL)


# Incorporate choice on zoom (and size ??)

size = (width, height)
resize = (int(width/2), int(height/2))

# See if cv2.resize(to any given size stills) 
def nothing(a):
	pass

def savezoom(a):
	zoom = (cv2.getTrackbarPos("zoom", "Parameters")-50)/10
	lines = open("parameters.py", 'r').readlines()
	for l in range(len(lines)):
		if lines[l].startswith("zoom ="):
			lines[l] = ("zoom = %d \n" %zoom)
	out = open("parameters.py", 'w')
	out.writelines(lines)
	out.close()
	print("saved lol")

cv2.namedWindow("Parameters", cv2.WINDOW_NORMAL)
cv2.createTrackbar("zoom", "Parameters", 50, 100, nothing)
cv2.createTrackbar("Click bar to save zoom parameter", "Parameters", 0, 100, savezoom)
cv2.resizeWindow("Parameters", 400, 100)



while True:

	zoom = (cv2.getTrackbarPos("zoom", "Parameters")-50)/10

	newcameramatrix, _ = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, size, zoom, size)



	#video_path = os.getcwd() + "/CheckerboardVideo/movie.mov"

	#vidcap = cv2.VideoCapture(video_path)
	# ret, frame = vidcap.read()

	# Maybe show checkerboards


	checker = cv2.imread(first_image)

	#checker = cv2.resize(checker, resize)
	imgDist = cv2.undistort(checker, cameraMatrix, dist, None, newcameramatrix)




	cv2.imshow("Choose Zoom", imgDist)
	#cv2.resizeWindow("Choose Zoom", imgDist.shape[1], imgDist.shape[0])
	if cv2.waitKey(1) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break

cv2.imwrite(os.getcwd() + "/CheckerboardVideo/"+ "checker0_unFisheyed.jpg" , imgDist)
#vidcap.release() # closes webcam
cv2.destroyAllWindows()




