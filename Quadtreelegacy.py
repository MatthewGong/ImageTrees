import numpy as np
import cv2 as cv


class Quadtree:
	"""

	DOC STRING GOES HERE

	"""	

	RootNode 	= None
	Grid 		= None
	count 		= 0
	Depth 		= 0

	def __init__(self, grid,tol):

		#determine how large the image is
		shape = grid.shape
		height, width, channels = shape[0],shape[1],shape[2]

		# starts with the whole image 
		self.RootNode = Node(0,0,height, width, grid, tol, 0)

		# save the image for later use
		self.Grid = grid


	#Create a sparse matrix from the nodes
	def toMatrix(self):
		pass


	# Display the image of the compressed tree
	def toimage(self,rootnode, mode = "boxes"):

		image = np.zeros_like(self.Grid)

		def traverse_img(node):

			if node.isleaf():
				x, y, temp_h, temp_w, color = node.render()
				h = temp_h/2
				w = temp_w/2
				
				#print "x:" ,x, "y:",y,"radius_x:",temp_w,"radius_y:",temp_h,"color:",color
				
				image[x-w:x+w, y-h:y+h,0] = color[0]
				image[x-w:x+w, y-h:y+h,1] = color[1]
				image[x-w:x+w, y-h:y+h,2] = color[2]
				
				#print image[x-temp_w:x+temp_w, y-temp_h:y+temp_h].shape
				#cv.imshow("Image",image[x-temp_w:x+temp_w, y-temp_h:y+temp_h])
				#cv.waitKey()	
	
			else:

				for child in node.Children:
					traverse_img(child)

	# Traverses the tree and fills in the image 
	
		traverse_img(rootnode)

		return image

	def nodecount(self):

		def traverse_count(node):
			if node.isleaf():
				self.count += 1
				##print node
			else:
				###print "ping"
				
				for child in node.Children:
					traverse_count(child)

		
		traverse_count(self.RootNode)
		return self.count



class Node:
	"""

	DOC STRING GOES HERE

	"""

	Children 	= None   	# defaults to bachelor/spinster
	X 			= 0			# defaults to top left corner
	Y 			= 0 		# defaults to top left corner
	Color    	= None	 	# defaults to None
	Width    	= 0			# defaults to empty
	Height	 	= 0			# defaults to empty
	
	Grid 		= None		# defaults to None
	Depth 		= 0

	def __init__(self,x,y,height,width,grid,tol, depth):

		# variables to shift the center to the middle of the block and not the cornerb
		h = height/2
		w = width/2

		L_x = w/2
		T_y = h/2

		R_x = int(w*1.5)
		B_y = int(h*1.5)

		self.X 			= x + w
		self.Y 			= y + h
		self.Width 		= width
		self.Height 	= height
		self.Grid  		= np.copy(grid)

		self.Depth 		= depth
		self.Leaf 		= False
		
		#print self.X,self.Y

		# If the subgrid is above the tolerance then split it into subgrids
		#print "width", width
		if MeasureDetail(self.Grid, split_tol = tol, area = height*width) or (width <= 5) or (height < 5):

			#print self.Grid[:w,:h,:].shape, self.X,self.Y
			#cv.imshow("Image",self.Grid)
			#cv.waitKey()
			
			#fill in the node color with the average
			self.Color = Average(self.Grid[:,:,0],self.Grid[:,:,1],self.Grid[:,:,2])
			self.Leaf = True
			##print "leaf on the wind"
			
		else:

			self.Children = []
		
			#cv.imshow("Image",self.Grid)
			#cv.waitKey()

			# split into four child nodes
			
			# Upper left
			#print "UL"
			self.Children.append(Node(self.X-w, self.Y-h, h, w, self.Grid[:w,:h,:], tol, self.Depth+1))
			
			# Upper right
			#print "UR"
			self.Children.append(Node(self.X-w, self.Y, h, width-w, self.Grid[:width-w,h:,:], tol, self.Depth+1))

			# Lower left
			#print "BL"
			self.Children.append(Node(self.X, self.Y-h, height-h, w, self.Grid[w:,:height-h,:], tol, self.Depth+1))
			
			# Lower right
			#print "BR"
			self.Children.append(Node(self.X, self.Y, height-h, width-w,  self.Grid[width-w:,height-h:,:], tol, self.Depth+1))
			


	def isleaf(self):
		#checks if a node is a leaf
		return self.Leaf

	# turns a node object into an image segment
	def render(self):

		return self.X, self.Y, self.Height, self.Width, self.Color

	def __str__(self):

		return str([self.X, self.Y, self.Height, self.Width, self.Color])



def Average(red, blue, green):
	"""

	DOC STRING GOES HERE

	Inputs:

			red 	:	flattened red channel from a section of the grid
			blue 	:	flattened blue channel from a section of the grid
			green 	: 	flattened green channel from a section of the grid 

	Outputs:

	"""

	#find the average in the color channels
	redAverage 		= np.nanmean(red)
	blueAverage 	= np.nanmean(blue)
	greenAverage 	= np.nanmean(green)

	##print redAverage, blueAverage, greenAverage
	return redAverage, blueAverage, greenAverage

def Manhattan(red, blue, green,area):
	"""
		Inputs:

				red 	:	flattened red channel from a section of the grid
				blue 	:	flattened blue channel from a section of the grid
				green 	: 	flattened green channel from a section of the grid 

		Outputs:

	"""

	#find the averages
	redAverage, blueAverage, greenAverage = Average(red,blue,green)

	#find the  manhattan distance
	# |x-xbar| + |y-ybar| + |z-zbar|
	total_distance  = np.sum(abs(red - redAverage)) + np.sum(abs(blue - blueAverage)) + np.sum(abs(green - greenAverage))

	return total_distance / (3.*area)


def Variance(red, blue, green):
	"""
		Inputs:

				red 	:	flattened red channel from a section of the grid
				blue 	:	flattened blue channel from a section of the grid
				green 	: 	flattened green channel from a section of the grid 

		Outputs:

	"""

	#find the averages
	redAverage, blueAverage, greenAverage = Average(red,blue,green)

	#find the  manhattan distance
	# |x-xbar| + |y-ybar| + |z-zbar|
	variance  = np.var(red) + np.var(blue) + np.var(green)

	return variance 


def MeasureDetail(grid, mode = 'Manhattan' , split_tol = 1500, area =1 ):
	"""

		DOC STRING GOES HERE

		Inputs:

				grid 		:	array, region of the image array NxMxC, C is the number of color data
				mode		:	string, chooses which splitting criterion we're using. Options are Manhattan, Variance, TBD...
				split_tol	:	float, determines how to split this varies wildly depending on the mode

		Outputs:

	"""

	acceptable_modes = {'Manhattan': Manhattan,'Variance' : Variance}

	if mode not in acceptable_modes:

		raise ValueError('Invalid Mode: please choose a valid mode {}'.format(acceptable_modes.keys))

	red 	= grid[:,:,0]
	blue 	= grid[:,:,1]
	green 	= grid[:,:,2]

	redFlat 	= red.flatten()
	blueFlat	= blue.flatten()
	greenFlat	= green.flatten()


	modes = {'Manhattan': Manhattan(redFlat,blueFlat,greenFlat,area),
			 'Variance' : Variance(redFlat, blueFlat, greenFlat)}

	#print "distance", modes[mode]
	return modes[mode] < split_tol

