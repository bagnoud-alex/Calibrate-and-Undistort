import numpy as np
import cv2
import os

# https://github.com/niconielsen32?tab=repositories

# INPUTS HERE
# ======================================================
vid_folder = os.getcwd() + "/CheckerboardVideo/"
vid_name = vid_folder + "movie.mov" 
checkerboard_dim = (9,6) # dimensions of the checkerboard array
take_sample_every_x_seconds_from_video = 1 # as the name says :) (to save computing power)
# ======================================================
# checkerboard_squarelen = 0.42 # in meters
path_checkers = vid_folder + "checkerboards/"
if not os.path.isdir(path_checkers):
    os.mkdir(path_checkers)


# Loading video and saving some parameters
vidcap = cv2.VideoCapture(vid_name)
nbFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) # number of frames
fps = vidcap.get(cv2.CAP_PROP_FPS) # frames per second
jump = int(fps * take_sample_every_x_seconds_from_video) # every 'jump' frames will be used
width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)) # width of video
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # height of video
# Printing results
print("Video length is %ds from which %d samples are taken, one every %.1f seconds"
 % (nbFrames/fps, int(nbFrames/jump), take_sample_every_x_seconds_from_video))


# Preparing vectors that will hold the each frame results
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((checkerboard_dim[0] * checkerboard_dim[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:checkerboard_dim[0], 0:checkerboard_dim[1]].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objPoints = [] # 3d point in real world space
imgPoints = [] # 2d points in image plane.


# Looping over each 'jump' frames
count = 0
for frame in range(0, nbFrames, jump):
    print("Finding Corners %d%%" % (frame*100/nbFrames), end="\r")

    # Going to the correct frame
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
    success, image = vidcap.read() # reading frame

    # If frame can be read
    if success:
        # Converts image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners (3x3)
        ret, corners = cv2.findChessboardCorners(gray, checkerboard_dim, None)

        # if corners could be found
        if ret:
            # Adding results
            objPoints.append(objp)
            # Refining corner detectino precision and adding results
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgPoints.append(corners2)
            # Saving frame
            image = cv2.drawChessboardCorners(image, checkerboard_dim, corners2, ret)
            cv2.imwrite(path_checkers + "/checker%d.jpg" % count, image)


    count += 1


# Print finish
print("Found %d/%d valid images for calibration" % (len(objPoints), int(nbFrames/jump)))


# Getting the camera calibration matrix over the saved frames 
_, cameraMatrix, dist, _, _ = cv2.calibrateCamera(objPoints, imgPoints, (width, height), None, None)

# Saving into Parameters.py
parameters = open("parameters.py", "w")
parameters.write("import numpy as np \n")
parameters.write("from numpy import float32 \n\n")

parameters.write("# ==== DISTORTION PARAMETER ==== \n")
parameters.write("%s = np.%s\n" % ("cameraMatrix", repr(cameraMatrix)))
parameters.write("%s = np.%s\n" % ("dist", repr(dist)))
parameters.write("%s = %s\n" % ("width", repr(width)))
parameters.write("%s = %s\n" % ("height", repr(height)))
parameters.write("%s = 1\n" % "zoom")
parameters.write("\n# ==== CHECKERBOARDS COORDINATES for /CheckerboardVideo/checkerboards images ==== \n")
parameters.write("%s = %s\n" % ("check_dim", repr(checkerboard_dim)))
parameters.write("%s = np.%s\n" % ("imgPoints", repr(imgPoints[0])))


print("The parameters of the calibration are saved in 'parameters.py'")
#cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))







