import numpy as np
import cv2 as cv
#import tree_node as treeNode
import treeNode
from matplotlib import pyplot as plt

#Global variables
BOX_SIZE  = 2
DEPTH_LIMIT = 10
#test at 7


class Quadtree:
	"""

	Attributes:
         
		RootNode :  Node,
			Head of the tree, all nodes will be descendants of this node

		Grid     : 	NxM numpy arry,
			The image that the tree is decomposing

		Count 	 :  int,
			The number of leaf nodes in the tree,

		Depth 	 :	int,
			The number of layers in the tree

		Cores	 :	Set of nodes,
			A subset of the nodes representing large areas of the tree

		Edges 	 : 	Set of nodes,
			A subset of the nodes representing the edge components of the image

		Matrix 	 : 	NxM numpy array,
			A sparsely populated array built from the toMatrix method()

		Opening	 :	NxM numpy array,
			A sparsely populated array build from the toMatrix method()
				built from running the Opening Morphological transformation
				on self.Matrix

		Partition:	String,
			A way to distinguish which partition to use to build the tree


	Method:

		Overview of the methods in the class.

		detailed documentation provided below

		__init__ 	:  return None
				Instantiate a tree based on a provided image

		toMatrix 	: returns boolean on success
				Build a matrix representation from a quadtree

		getPoints	: returns (N,2) numpy array of point coordinates
				Recursively traverse the tree and collect all leaf nodes

		toImage 	:  return NxM numpy array
				Rebuild the image representation of the tree


	"""

	def __init__(self,grid,tol,mode,partition):

		# The partitions are how we divide up the space and using a mixture of partitions
		# or a naturally varying partition gives us more robust edge detection

		acceptable_partitions= {'quad', 'shift_center', 'golden'}

		if partition not in acceptable_partitions:

			raise ValueError('Invalid Mode: please choose a valid mode {}'.format(acceptable_partitions.keys()))


		#determine how large the image is
		height, width, channels = grid.shape
		#Channels are equal to depth

		# starts with the whole image
		self.RootNode = treeNode.Node(None,0,0,height, width, grid, tol, 0, mode, partition)

		# save the image for later use
		self.Grid = grid

		self.Partition = partition

		self.Matrix = np.zeros((height,width))

		# add in the other three corners
		#self.Edges.append([width,  0])
		#self.Edges.append([width, -height])
		#self.Edges.append([0, -height])
		self.Cores		= []
		self.Edges		= [] #starts with the corners included

		self.Count = 0




	#Create a sparse matrix from the nodes
	def toMatrix(self,mode = "corners"):
		"""
		Builds a matrix representation from a Quadtree.


		Methods:
			tree traversal,
				startin with the root node, recursively spider down the tree
				check if a node is terminal(leaf) and adding it to our matrix
				otherwise check the nodes children

		"""

		height, width = self.Matrix.shape

		# create an edge mask using the corners of the boxes as little 2x2s
		# based on the BOX_SIZE
		def traverse_matrix(node,):

			# if the node is a leaf set the corners of its region to TRUE
			if node.isleaf():

				y, x, temp_h, temp_w, color = node.render()

				h = temp_h
				w = temp_w

				#if the node is in a sufficiently small region add it to the SET of edges
				if h < 10 or w < 10:
					self.Edges.append(node)

					if mode == 'corners':

						left 	= x
						right 	= x+w
						up 		= y
						down 	= y+h

						#prevents wrap around errors
						if down >= height:
							down = height-1

						if up < 0:
							up   = 0

						if left < 0:
							left = 0

						if right >= width:
							right = width - 1

						# upper left corner
						self.Matrix[up:up+BOX_SIZE,left:left+BOX_SIZE] = 255

						# uper right corner
						self.Matrix[up:up+BOX_SIZE,right-BOX_SIZE:right] = 255

						# lower left corner
						self.Matrix[down-BOX_SIZE:down,left:left+BOX_SIZE] = 255

						# lower right corner
						self.Matrix[down-BOX_SIZE:down,right-BOX_SIZE:right] = 255

					elif mode == 'centers':

						# lower right corner
						self.Matrix[y-BOX_SIZE:y+BOX_SIZE,x-BOX_SIZE:x+BOX_SIZE] = 255

				else:
					self.Cores.append(node)

			else:
				for child in node.Children:
					traverse_matrix(child)


		traverse_matrix(self.RootNode)

		# Traverses the image and fills in an array

		kernel = np.ones((3,3),np.uint8)
		self.Opening = cv.morphologyEx(self.Matrix, cv.MORPH_OPEN, kernel)
		self.Opening = cv.dilate(self.Opening, kernel, iterations = 15	)
		return True

	# Creates an array of the all the point representation of the leaf nodes
	def getPoints(self):
		height, width = self.Matrix.shape
		# create an edge mask using the corners of the boxes as little 2x2s

		core_points = []
		edge_points = []
		def traverse_points(node):
			# if the node is a leaf set the corners of its region to TRUE
			if node.isleaf():

				y, x, temp_h, temp_w, color = node.render()


				if temp_h < 10 or temp_w < 10:
					self.Edges.append(node)
					edge_points.append(node.pos())
				else:
					self.Cores.append(node)
					core_points.append(node.pos())


			else:
				for child in node.Children:
					traverse_points(child)


		traverse_points(self.RootNode)

		points = core_points + edge_points 
		print points
		return np.array(points)



	# Display the image of the compressed tree
	def toImage(self, mode = "boxes"):

		image = np.zeros_like(self.Grid)
		height, width, channels = self.Grid.shape
#		image = np.zeros((2*height,2*width,channels))

		def traverse_img(node,mode):

			if node.isleaf():
				y, x, temp_h, temp_w, color = node.render()
				print node.render()

				if mode == "boxes":
					temp_h += 2
					temp_w += 2
				else:
					temp_h += 2
					temp_w += 2

				left 	= x
				right 	= x+temp_w
				up 		= y
				down 	= y+temp_h


				#check that the boundaries are 	

				if down >= height:
					down = height-1

				if up < 0:
					up   = 0

				if left < 0:
					left = 0

				if right >= width:
					right = width - 1
				"""		
				plt.imshow(self.Grid[up:down, left:right, :])
				plt.show()"""
				print node.render()
				print left, right, up, down
				#set the region equal to it's components
				for channel in range(channels):
					image[up:down, left:right, channel] = color[channel]


			else:

				for child in node.Children:
					traverse_img(child,mode)

	# Traverses the tree and fills in the image

		traverse_img(self.RootNode,mode)

		return image

	# Counts all the leaf nodes in the tree and updates self.Count
	def nodecount(self):

		def traverse_count(node):
			if node.isleaf():
				self.Count += 1
				####print node
			else:
				#####print "ping"

				for child in node.Children:
					traverse_count(child)

		# traverses the tree and counts the number of leaves
		traverse_count(self.RootNode)
		return self.Count


