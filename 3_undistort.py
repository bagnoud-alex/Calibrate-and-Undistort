import numpy as np
import cv2
import os

"""
This script reads the camera calibration parameters from parameters.py and undistorts
batches of videos present in the folder 'Videos_in'.
N.B. This script can be run infinitely as long as the parameters.py are in accordance 
to the camera they were computed from.
"""

# ENTER INPUTS HERE
# ======================================================
input_path = os.getcwd() + "/Videos_in/" # folder containing input videos
output_path = os.getcwd() + "/Videos_out/" # folder that will contain output videos
videos_format = '.avi' # format of the videos to be processed
# ======================================================



print("---------------------------------------------------------------------")
# === Getting parameters from parameters.py ===
import parameters
cameraMatrix = parameters.cameraMatrix
dist = parameters.dist
resize = parameters.resize
width = parameters.width
height = parameters.height
zoom = parameters.zoom
print("Parameters have been loaded from parameters.py")



# === Creating output folder if it doesn't exists already === 
if not os.path.isdir(output_path):
    os.mkdir(output_path)



# === Getting the videos names in 'Video_path' ===
Videos = [file for file in os.listdir(input_path) if file.endswith(videos_format)]
if len(Videos) == 0:
    exit("Error: No videos were found in the folder '/Videos_in\n"
    	 "Check 3_undistort.py if the input video format is correct.")
else:
    print("%d Video(s) has/have been found in '/Videos_in'" % len(Videos))



# === PROCESSING OF ONE VIDEO AT THE TIME ===
for i in range(len(Videos)):

    # === PREPARATIONS ===

    # Getting all the names
    print("Processing: ", Videos[i])
    vid_name = Videos[i][0:len(Videos[i])-4] # Name of video without '.avi'
    vid_path = input_path + Videos[i] # Input path of video
    out_path_frame = output_path + vid_name # path to print first frame for verification
    out_path = output_path + vid_name + "_undistorted.avi" # final video output path + name

    # Creating new folder for verification
    if not os.path.isdir(out_path_frame):
        print("Creating Frame folder in '/Videos_out")
        os.mkdir(out_path_frame)

    # Loading video
    vidcap = cv2.VideoCapture(vid_path)
    nbFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Reading first frame and saving
    success, image = vidcap.read()
    if resize: image = cv2.resize(image, (width, height))
    cv2.imwrite(out_path_frame + "/frame0.jpg", image)

    # Initialize distortion coefficient matrix
    newcameramatrix, _ = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (width, height), zoom, (width, height))

    # Printing first processed image for parameters verification
    firstProcessed = cv2.undistort(image, cameraMatrix, dist, None, newcameramatrix)
    cv2.imwrite(out_path_frame + "/frame0_processed.jpg", firstProcessed)

    # Preparing video output specs
    fps = vidcap.get(cv2.CAP_PROP_FPS) # frames per second
    # output of video
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'DIVX'), fps, (width, height))



    # === PROCESSING AND CREATING MOVIE ONE FRAME AT THE TIME ===

    count = 0
    while success:
        # Printing progress
        print("Processing frames %d%%" % (count*100/nbFrames), end="\r")

        # Undistorting frame
        imgDist = cv2.undistort(image, cameraMatrix, dist, None, newcameramatrix)

        # addding last processed frame to video output
        out.write(imgDist)

        # Loads next image and resizes
        success, image = vidcap.read()
        if resize and success: image = cv2.resize(image, (width, height))
        count += 1

    print("Frames Processed.      ")


    # === BUILDING VIDEO === 
    out.release()
    print("Conversion Complete.      ")





