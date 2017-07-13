import QuadtreeChannels as qt
import cv2 as cv
import numpy as np
import time
import os

import segmentation as seg

from scipy.spatial import Delaunay
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import ConvexHull

import matplotlib.pyplot as plt


path = os.path.join(os.path.abspath(os.curdir),"images/SteeringWheel_raw.jpg")#pass in an image
	

image = cv.imread(path)


plt.imshow(image)
plt.show()

start = time.time()
quad = qt.Quadtree(image,2000,'Manhattan','shift_center')
end = time.time()-start

print "Compress: " +  str(quad.nodecount()/float(image.shape[0]*image.shape[1]))
print "Run time: " +  str(end)

output = quad.toImage(quad.RootNode)

start = time.time()
quad2 = qt.Quadtree(image,2000,'Variance','shift_center')
end = time.time()-start

print "Compress: " +  str(quad2.nodecount()/float(image.shape[0]*image.shape[1]))
print "Run time: " +  str(end)

if quad2.toMatrix():

	plt.imshow(quad2.Matrix, cmap= 'gray')
	plt.title('Matrix Representation')
	plt.show()


points = quad2.getPoints()
print points
tri = Delaunay(points)
plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
plt.plot(points[:,0], points[:,1], 'o')
plt.ylim(0, 1080)
plt.xlim(0,1920)
plt.title('Delanauy Triangulation')
plt.show()

output = quad2.toImage()

plt.imshow(output, origin="upper")
plt.show()

"""
points2 = quad2.getPoints()


tri2 = Delaunay(points2)
plt.triplot(points2[:,0], points2[:,1], tri2.simplices.copy())
plt.plot(points2[:,0], points2[:,1], 'o')
plt.ylim(-1080,0)
plt.xlim(0,1920)
plt.title('Refined Delanauy Triangulation')
plt.show()


print tri2.simplices.size

start = time.time()
quad3 = qt.Quadtree(image,16,'Manhattan','quad')
end = time.time()-start

print quad3.nodecount(), end

output = quad3.toImage(quad3.RootNode)

plt.imshow(output)
plt.show()
cv.imwrite("output3.jpg",output)

"""
"""
testViewer = seg.Segmentation(image,14,'Manhattan','quad')

testPic = testViewer.displaySegments()


#print len(testPics)
fs = np.zeros_like(testPic)

for pic in testPics:
	fs += pic
	#plt.imshow(pic)

	#plt.show()

print testPic.shape, testPic
plt.imshow(testPic, cmap='nipy_spectral')
plt.show()
"""

