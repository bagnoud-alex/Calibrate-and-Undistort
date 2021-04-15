import numpy as np
import cv2

vidcap = cv2.VideoCapture(0)

while True:
	ret, vid = vidcap.read()
	cv2.imshow("lol", vid)

	# Maybe show checkerboards

	# or maybe show undistorted


	bla = cv2.waitKey(1)
	if bla == 27:
		break

vidcap.release() # closes webcam
cv2.destroyAllWindows()