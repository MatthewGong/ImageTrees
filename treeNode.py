import numpy as np

#Global variables
BOX_SIZE  = 2
DEPTH_LIMIT = 10
#test at 7


class Node:
	"""

	Attributes:
		Parent  :  Node,
			The parent node

		Children:  List of nodes,
			Descendants of the node

		X	 	:  int,
			The x index of the node in the tree,

		Y	 	:  int,
			The y index of the nodes in the tree,

		Color 	: tuple,
			The RGB values, but can be used with other color basis (CMYK etc)

		Height 	: int,
			The height of the region represented by the node

		Width 	: int,
			The width of the region represented by the node

		Grid     : 	NxM numpy arry,
			The portion of the image that the node is decomposing

		Depth 	 :	int,
			The depth of the node in the tree

		Centers	 :	Set of nodes,
			A subset of the nodes representing large areas of the tree

	Method:

		Overview of the methods in the class.

		detailed documentation provided below

		__init__ 	:  return None
				Recursively split the node until the tree is built

		__str__ 	:  return string
				the string representation of the node in list form

		pos 	 	:  returns list
				a list containing the x,y coordinates of the node

		isleaf 		:  return Boolean
				true/false if the node is/isn't a leaf

		render		: returns int, int, int, int, int
				turns a node into a region of the image

		procreate 	: 	return None
				creates children of the current node.

	"""

	Parent   	= None
	Children 	= None   	# defaults to bachelor/spinster
	X 			= 0			# defaults to top left corner
	Y 			= 0 		# defaults to top left corner
	Color    	= None	 	# defaults to None
	Width    	= 0			# defaults to empty
	Height	 	= 0			# defaults to empty

	Grid 		= None		# defaults to None
	Depth 		= 0			# sets the current depth

	def __init__(self,parent,x,y,height,width,grid,tol, depth, mode, partition):
		"""

		"""

		self.Parent = parent

		# variables to shift the center to the middle of the block and not the corner
		h = height/2
		w = width/2

		self.X 			= x + w
		self.Y 			= y + h


		self.Width 		= width
		self.Height 	= height
		self.Grid  		= np.copy(grid)

		self.Depth 		= depth
		self.Leaf 		= False

		self.tol 		= tol
		self.Mode 		= mode

		# If the subgrid is above the tolerance then split it into subgrids
		# Assume the tree will always split on the first NUMBER of iterations
		if self.Depth < 3:

			self.procreate(self.Width, self.Height, partition)

		elif MeasureDetail(self.Grid, mode, split_tol = tol, area = height*width) or (self.Width <= 8) or (self.Height <= 8) or (self.Depth > DEPTH_LIMIT):

			###print self.Grid[:w,:h,:].shape, self.X,self.Y
			#cv.imshow("Image",self.Grid)
			#cv.waitKey()

			#fill in the node color with the average
			channels = Channels(grid)
			self.Color = Average(channels)
			self.Leaf = True
			####print "leaf on the wind"

		else:

			self.procreate(self.Width,self.Height,partition)
			#cv.imshow("Image",self.Grid)
			#cv.waitKey()

			# split into four child nodes

			# Upper left

	def pos(self):

		return [self.X, -self.Y]


	def isleaf(self):
		#checks if a node is a leaf
		return self.Leaf

	# turns a node object into an image segment
	def render(self):

		return self.X, self.Y, self.Height, self.Width, self.Color

	def procreate(self, width, height, partition):

		def quad(width,height):
			h,w = self.Height/2 , self.Width/2

			x , y    = self.X-w , self.Y-h
			x_R, y_L = self.X, self.Y
			height_U = h
			height_L = height - h
			width_R  = w
			width_L  = width - w

			return x, y, x_R, y_L, height_U, height_L, width_R, width_L

		def golden(width,height):
			h,w = self.Height/2 , self.Width/2
			x , y    = self.X-w , self.Y-h
			x_R, y_L = self.X, self.Y
			height_U = h
			height_L = height - h
			width_R  = w
			width_L  = width - w

			return x, y, x_R, y_L, height_U, height_L, width_R, width_L

		def shift_center(width,height):
			h,w = self.Height/3 , self.Width/3

			x , y    = self.X-w , self.Y-h
			x_R, y_L = self.X, self.Y
			height_U = h
			height_L = height - h
			width_R  = w
			width_L  = width - w

			return x, y, x_R, y_L, height_U, height_L, width_R, width_L


		Partitions = {'quad' 		: quad(width,height),
 				 'shift_center' : shift_center(width,height),
				 'golden'		: golden(width,height)
				 }


		# make a holder for future children
		self.Children = []

		x , y, x_R, y_L, height_U, height_L, width_R, width_L = Partitions[partition]

		# Upper Left
		self.Children.append(Node(self,x, y, height_U, width_R, self.Grid[:height_U,:width_R,:], self.tol, self.Depth+1,self.Mode,partition))

		# Upper right
		self.Children.append(Node(self,x, y_L, height_U, width_L, self.Grid[height_U:,:width_L,:], self.tol, self.Depth+1,self.Mode,partition))

		# Lower left
		self.Children.append(Node(self,x_R, y, height_L, width_R, self.Grid[:height_L, width_R:, :], self.tol, self.Depth+1,self.Mode,partition))

		# Lower right
		self.Children.append(Node(self,x_R, y_L, height_L, width_L,  self.Grid[height_L:, width_L:, :], self.tol, self.Depth+1,self.Mode,partition))



	def __str__(self):

		return str([self.X, self.Y, self.Height, self.Width, self.Color])



def Average(channels):
	"""

	Calculates the average value for all channels

	Inputs:

			Channel	 : 	list of arrays,
				flattened channels from a section of the grid

	Outputs:

			Averages :	list of floats,
				the averages of the channels

	"""

	#find the average in the color channels
	averages = []

	for channel in channels:
		averages.append(np.mean(channel))

	return averages

def Manhattan(channels,area):
	"""
	Calculates the Manhattan metric of a given region

	Inputs:

		Channel	 : 	list of arrays,
			flattened channels from a section of the grid

		Area 	 : int,
			The area of the region

	Outputs:

		total_distance : float,
			the distance normalized by the area

	"""

	#find the averages
	averages = Average(channels)

	#find the  manhattan distance
	# |x-xbar| + |y-ybar| + |z-zbar|
	total_distance  = 0


	for channel in xrange(len(channels)):
		total_distance += np.sum(abs(channels[channel]-averages[channel]))


	return total_distance / (len(channels)*area)


def Variance(channels, area):
	"""
	Calculates the Variance metric of a given region

		Inputs:

			Channel	 : 	list of arrays,
				flattened channels from a section of the grid

			Area 	 : int,
				The area of the region

		Outputs:

			variance : float,
				the variance normalized by the area
	"""

	#find the variance of the channels
	variance = 0

	for channel in channels:
		variance += np.var(channel)

	return variance

def Channels(grid):
	"""
	decompose the region into its component channels

		Inputs:


			grid 	 : NxM numpy array,
				The portion of the image to decompose

		Outputs:

			Channel	 : 	list of arrays,
				flattened channels from a section of the grid

	"""

	channels = []

	counter = 0
	for channel in xrange(grid.shape[2]):
		counter += 1
		#print counter
		channels.append(grid[:,:,channel].flatten())

	return channels


def MeasureDetail(grid, mode = 'Manhattan' , split_tol = 1500, area = 1 ):
	"""

		Determines whether the detail is sufficient to split the node


		Inputs:

				grid 		:	array NxMxC,
					region of the image array NxMxC, C is the number of color data

				mode		:	string,
					chooses which splitting criterion we're using. Options are Manhattan, Variance, TBD...

				split_tol	:	float,
					determines how to split this varies wildly depending on the mode

		Outputs:

				boolean 	: 	True/False,
					the detail was sufficient or insufficient


	"""

	acceptable_modes = {'Manhattan': Manhattan,'Variance' : Variance}


	if mode not in acceptable_modes:

		raise ValueError('Invalid Mode: please choose a valid mode {}'.format(acceptable_modes.keys()))

	channels = Channels(grid)




	modes = {'Manhattan': Manhattan(channels, area),
			 'Variance' : Variance(channels, area)}



	return modes[mode] < split_tol

