import cv2 as cv
import numpy as np
import time
import os

import segmentation as seg



def image_segmentation(path, origin_path, tolerance = 14, mode = "Manhattan", partition = "quad"):
    
    #load the necessary information
    files = os.listdir(origin_path)
    print files
    for f in files:
    	print f
    	if not os.path.isdir(f):

	    	start = time.time()
	        # read in the next image and process it
	        image = cv.imread(path + "\\" + f)

	        # make the segmentation
	        testViewer = seg.Segmentation(image,tolerance, mode, partition)

	      	# save the fractalilzed output
	      	subpath = path + "\\processed\\" + fractal_subfolder
	      	cv.imwrite(subpath+"\\"+f , testViewer.Quadtree.toImage())

	        # save the segmentation
	        subpath = path + "\\processed\\" + segmented_subfolder
	        cv.imwrite(subpath+"\\"+f , testViewer.displaySegments())

	  	    # save the network graphic
	        subpath = path + "\\processed\\" + network_subfolder
	        
	        testViewer.saveNetwork(subpath+"\\"+f)

	        print time.time() - start
	        del testViewer
	        

"""
Example of a path

path = os.path.join(os.path.abspath(os.curdir),"images/SteeringWheel_raw.jpg")#pass in an image

"""
origin = os.curdir
cwd = raw_input("What directory do you want to process? yes, the whole path name \n")


tol = raw_input("What tolerance do you want to use? d defaults to 16 \n")

if tol == "d":
	tol = 16

# kindly do not put the training image set in the repo since space is limited

print cwd
#creates necessary path variables to construct the data and store it for later use
network_subfolder = 'network'
segmented_subfolder = 'segmented'
fractal_subfolder = 'fractal'
subfolders = [network_subfolder, segmented_subfolder, fractal_subfolder]

if not os.path.exists(cwd+"\\" + "processed"):

    os.mkdir(cwd+"\\" +"processed")

    #create a directory for the raw images and return to the main directory
    os.chdir(cwd+"\\" + "processed")
              
    os.mkdir(segmented_subfolder)
    os.mkdir(network_subfolder)
    os.mkdir(fractal_subfolder)
    
    
    #return to the video folder for the next directory
    os.chdir(cwd)
    print "i did it"
else:
	print "these folders already exist for this directory"
#now that we've made the folders or ensured their existence we process the images



image_segmentation(cwd,cwd, tolerance = tol)

os.chdir(origin)
