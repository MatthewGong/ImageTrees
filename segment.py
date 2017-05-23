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

	Cores 	= None
	Edges 	= None

	Locus 	= [0 , 0]
	Color 	= None 

	def __init__(self, ):

		pass

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