import numpy as np
import treeNode as Node

class jig:
	"""
	Attributes:

		Cores : set of Nodes,
			the collection of core nodes in a segment

		Edges : set of Nodes,
			The collection of edge nodes in a segment
		
		Locus :  [int, int],
			The coordinates of the object,
			
		color_profile :  [[colors],float],
			variance and mean color of the the coress
			


	Method:

		Overview of the methods in the class.

		detailed documentation provided below

		__init__ 	:	return None
			Instantiate a tree based on a provided image

		updateColor	:	return boolean:
			changes the color profile based on the new nodes, boolean on success

		updateLocus	:	return boolean
			changes the locus based on the new nodes, boolean on success

	"""

	def __init__(self, ):

		self.Cores_Nodes 	= []
		self.Edges_Nodes 	= []

		self.Locus 	= [0 , 0]
		self.Color 	= None 


	def updateColor(self):
		"""		
		Changes the color profile based on newly added nodes


		Inputs:
			mode: string
				determines which axis to sort the cores by.

		Methods:

		"""
		pass

	def setLocus(self, mode="weighted"):
		"""		
		
		sets the locus of the object based on the nodes in the collection


		Inputs:
			mode: string
				determines which version of Center of Mass(CoM) to find the locus.

				'Weighted'		: use the relative size of a node when determining CoM
				'Unweighted'	: use the only the coordinates in determining the CoM

		Methods:

		"""


		pass

	def display(self, size, color):
		"""

		prints out the jig based on the 
		
		Inputs:

			None

		Methods:

		"""
		image = np.zeros(size[0:2])
		height, width, channels = size

		for node in self.Cores_Nodes:
			x, y, temp_h, temp_w, tempcolor = node.render()

			h = temp_h/2 + 1
			w = temp_w/2 + 1

			
			left 	= x-w
			right 	= x+w
			up 		= y-h
			down 	= y+h


			#check that the boundaries are valid

			if down >= height:
				down = height-1

			if up < 0:
				up   = 0

			if left < 0:
				left = 0

			if right >= width:
				right = width - 1

			#set the region equal to it's components
			#for channel in range(channels):
			#	image[up:down, left:right, channel] = color[channel]
			image[up:down, left:right] = color


		for node in self.Edges_Nodes:
			x, y, temp_h, temp_w, tempcolor = node.render()

			h = temp_h/2 + 1
			w = temp_w/2 + 1
			left 	= x-w
			right 	= x+w
			up 		= y-h
			down 	= y+h


			#check that the boundaries are valid

			if down >= height:
				down = height-1

			if up < 0:
				up   = 0

			if left < 0:
				left = 0

			if right >= width:
				right = width - 1

			#set the region equal to it's components
			#for channel in range(channels):
			#	image[up:down, left:right, channel] = color[channel]
			image[up:down, left:right] = color


		return image
