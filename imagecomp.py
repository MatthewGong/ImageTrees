import QuadtreeChannels as qt
#import Quadtree as qt
import cv2 as cv 
import numpy as np
import time


#path = r"C:\Users\Matth\Documents\seniorcoding\Project\Videos\SteeringWheel\raw\SteeringWheel_0001.jpg"
path = r"C:\Users\Matth\Documents\seniorcoding\Project\Videos\TropicalFish\raw\TropicalFish_0021.jpg"

#path = r"C:\Users\Matth\Pictures\test.jpg"
#path = r"C:\Users\Matth\Pictures\four.jpg"
#path = r"C:\Users\Matth\Documents\seniorcoding\Project\four.jpg"
#path = r"C:\Users\Matth\Documents\seniorcoding\Project\maybe.jpg"
#path = r"C:\Users\Matth\Documents\seniorcoding\Project\bigger.jpg"


print path
image = cv.imread(path)

print image.shape
#cv.imshow("Image",image)
#cv.waitKey()

start = time.time()
quad = qt.Quadtree(image,10,'Manhattan')
end = time.time()-start

print quad.nodecount(), end

output = quad.toimage(quad.RootNode, mode = "smooth")

#cv.imshow("Image",output)
cv.imwrite("output.jpg",output)

#cv.imshow("Image",output)
#cv.waitKey()

start = time.time()
quad2 = qt.Quadtree(image,450,'Variance')
end = time.time()-start

print quad2.nodecount(), end

output2 = quad2.toimage(quad2.RootNode,mode = "smooth")

cv.imwrite("output2.jpg",output2)

