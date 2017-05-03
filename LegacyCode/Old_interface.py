import QuadtreeChannels as qt
#import Quadtree as qt
import cv2 as cv 
import numpy as np
import time
import triangulation as trg
from scipy.spatial import Delaunay
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import ConvexHull

import matplotlib.pyplot as plt


#path = r"C:\Users\Matth\Documents\seniorcoding\Project\Videos\SteeringWheel\raw\SteeringWheel_0001.jpg"
path = r"C:\Users\Matth\Documents\seniorcoding\Project\Videos\TropicalFish\raw\TropicalFish_0021.jpg"
#path = "C:\\Users\\Matth\\Documents\\seniorcoding\\Project\\Videos\\Catherdral\\raw\\cathedral_0001.jpg"
#path = r"C:\Users\Matth\Documents\seniorcoding\Project\Videos\cathedral\raw\cathedral_0001.jpg"
##path = r"C:\Users\Matth\Pictures\four.jpg"
#path = r"C:\Users\Matth\Documents\seniorcoding\Project\four.jpg"
#path = r"C:\Users\Matth\Documents\seniorcoding\Project\maybe.jpg"
#path = r"C:\Users\Matth\Documents\seniorcoding\Project\bigger.jpg"


print path
image = cv.imread(path)

print image.shape
#cv.imshow("Image",image)
#cv.waitKey()

start = time.time()
quad = qt.Quadtree(image,12,'Manhattan','quad')
end = time.time()-start

print quad.nodecount(), end

output = quad.toimage(quad.RootNode, mode = "smooth")

cv.imwrite("output.jpg",output)

start = time.time()
quad2 = qt.Quadtree(image,800,'Variance','quad')
end = time.time()-start

print quad2.nodecount(), end

output2 = quad2.toimage(quad2.RootNode,mode = "smooth")

cv.imwrite("output2.jpg",output2)

"""
if quad2.toMatrix():
	print quad2.Matrix
"""

cv.imwrite('mask.jpg',quad2.Matrix)
cv.imwrite('mask2.jpg',quad2.Opening)


cv.imwrite('canny.jpg',cv.Canny(image, 100, 250))


points = quad2.getPoints()
print 'check point a'

tri = Delaunay(points)
plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
plt.plot(points[:,0], points[:,1], 'o')
plt.show()


points2 = np.array(quad2.Edges)
print tri.simplices.copy()

tri2 = Delaunay(points2)
plt.triplot(points2[:,0], points2[:,1], tri2.simplices.copy())
plt.plot(points2[:,0], points2[:,1], 'o')
plt.show()


pointsA = quad2.getPoints()
print 'check point a'

vor = Voronoi(points)
voronoi_plot_2d(vor)
plt.show()


pointsa = np.array(quad2.Centers)
print 'check point pwwer'

vor2 = Voronoi(pointsa)
print 'checkpoint 2342'
voronoi_plot_2d(vor2)
plt.show()


"""
start = time.time()
quad3 = qt.Quadtree(image,16,'Manhattan','shift_center')
end = time.time()-start

print quad3.nodecount(), end

output = quad3.toimage(quad3.RootNode, mode = "smooth")

#cv.imshow("Image",output)
cv.imwrite("output3.jpg",output)
"""
