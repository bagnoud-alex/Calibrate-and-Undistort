import numpy as np
import cv2
import os

"""
This script is used to get the necessary parameters to undistort any image/video.
The parameters that are printed in parameters.py are unique to the camera.
The calibration parameters are also dependent to the resizing, if the resizing 
has to be changed, this script has to be run again
"""

# INPUTS HERE
# ======================================================
vid_folder = os.getcwd() + "/Calibration_Video/"
vid_name = vid_folder + "calibration_video_name.avi" 
checkerboard_dim = (9,6) # dimensions of the checkerboard array
take_sample_every_x_seconds_from_video = 1 # as the name says :) (to save computing power)

# Resizing of the video, if True, the aspect ratio will be preserved
resize = False # Resize video ? False = no resizing. True = resizing
ratio_if_resize_true = 0.625 # 1 == original size
# ======================================================



print("---------------------------------------------------------------------")
# Creating path where the calibration checkerboards are saved
path_checkers = vid_folder + "checkerboards/"
if not os.path.isdir(path_checkers):
    os.mkdir(path_checkers)



# === LOADING CALIBRATION VIDEO ===
vidcap = cv2.VideoCapture(vid_name)
if not vidcap.isOpened():
    exit("Video was not loaded. Verify inputs in 1_calibrate.py:\n%s" % vid_name)

# Getting info from input video
nbFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) # number of frames
fps = vidcap.get(cv2.CAP_PROP_FPS) # frames per second
jump = int(fps * take_sample_every_x_seconds_from_video) # every 'jump' frames will be used
width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)) # width of video
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # height of video
# Printing info
print("Video length is %ds from which %d samples are taken, one every %.1f seconds"
 % (nbFrames/fps, int(nbFrames/jump), take_sample_every_x_seconds_from_video))
print("Around 50 samples or more is recommended, the more the better (but slower)!")

# Resizing video ?
if resize == True:
    print("RESIZING VIDEO :")
    print("  - Original size: %dx%d" %(width, height))
    width = int(width * ratio_if_resize_true)
    height = int(height * ratio_if_resize_true)
    print("  - New size: %dx%d" %(width, height))



# === PREPARATION OF CALIBRATION PARAMS + OUTPUTS ====
# criteria to refine location of checkerboard corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((checkerboard_dim[0] * checkerboard_dim[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:checkerboard_dim[0], 0:checkerboard_dim[1]].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objPoints = [] # 3d point in real world space
imgPoints = [] # 2d points in image plane.



# === Looping over each 'jump' frames ====
count = 0
for frame in range(0, nbFrames, jump):
    # Printing progress
    print("Finding Corners %d%%" % (frame*100/nbFrames), end="\r")

    # Going to the correct frame
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
    success, image = vidcap.read() # reading frame
    if resize: image = cv2.resize(image, (width,height)) # Resize image if resize==true

    # If frame can be read
    if success:
        # Converts image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners (3x3)
        foundgrid, corners = cv2.findChessboardCorners(gray, checkerboard_dim, None)

        # if checkerboard grid could be found
        if foundgrid:
            # Adding results
            objPoints.append(objp)
            # Refining precision of corner location and adding results
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgPoints.append(corners2)
            # Saving frame with drawn checkerboard
            image = cv2.drawChessboardCorners(image, checkerboard_dim, corners2, foundgrid)
            cv2.imwrite(path_checkers + "/checker%d.jpg" % count, image)

    count += 1

# Print finish
print("Found %d/%d valid images for calibration" % (len(objPoints), int(nbFrames/jump)))



# === CALIBRATING CAMERA ===
_, cameraMatrix, dist, _, _ = cv2.calibrateCamera(objPoints, imgPoints, (width, height), None, None)



# === Saving calibration in parameters.py ===
parameters = open("parameters.py", "w") # open file
# Some imports
parameters.write("import numpy as np \n")
parameters.write("from numpy import float32 \n\n")
# parameters
parameters.write("# ==== DISTORTION PARAMETER ==== \n")
parameters.write("%s = np.%s\n" % ("cameraMatrix", repr(cameraMatrix)))
parameters.write("%s = np.%s\n" % ("dist", repr(dist)))
parameters.write("%s = %s\n" % ("resize", repr(resize)))
parameters.write("%s = %s\n" % ("width", repr(width)))
parameters.write("%s = %s\n" % ("height", repr(height)))
parameters.write("%s = 1\n" % "zoom")

print("The parameters of the calibration are saved in 'parameters.py'")
print("---------------------------------------------------------------------")








