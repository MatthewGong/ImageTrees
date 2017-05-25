import QuadtreeChannels as qt
import cv2 as cv
import numpy as np
import time
import os

from scipy.spatial import Delaunay
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import ConvexHull

import matplotlib.pyplot as plt


path = os.path.join(os.path.abspath(os.curdir),"images/SteeringWheel_raw.jpg")#pass in an image
	

image = cv.imread(path)


start = time.time()
quad = qt.Quadtree(image,14,'Manhattan','quad')
end = time.time()-start

print "Compress: " +  str(quad.nodecount()/float(image.shape[0]*image.shape[1]))
print "Run time: " +  str(end)

output = quad.toImage(quad.RootNode, mode = "smooth")

start = time.time()
quad2 = qt.Quadtree(image,900,'Variance','quad')
end = time.time()-start

print "Compress: " +  str(quad2.nodecount()/float(image.shape[0]*image.shape[1]))
print "Run time: " +  str(end)

if quad2.toMatrix():

	plt.imshow(quad2.Matrix, cmap= 'gray')
	plt.title('Matrix Representation')
	plt.show()


points = quad2.getPoints()
tri = Delaunay(points)
plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
plt.plot(points[:,0], points[:,1], 'o')
plt.ylim(-1080,0)
plt.xlim(0,1920)
plt.title('Delanauy Triangulation')
plt.show()


points2 = np.array(quad2.Edges)


tri2 = Delaunay(points2)
plt.triplot(points2[:,0], points2[:,1], tri2.simplices.copy())
plt.plot(points2[:,0], points2[:,1], 'o')
plt.ylim(-1080,0)
plt.xlim(0,1920)
plt.title('Refined Delanauy Triangulation')
plt.show()


print tri2.simplices.size
"""
start = time.time()
quad3 = qt.Quadtree(image,16,'Manhattan','shift_center')
end = time.time()-start

print quad3.nodecount(), end

output = quad3.toimage(quad3.RootNode, mode = "smooth")

#cv.imshow("Image",output)
cv.imwrite("output3.jpg",output)
"""



