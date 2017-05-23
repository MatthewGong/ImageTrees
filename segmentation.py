import numpy as np
import segment as seg
import QuadtreeChannels as qt

class Segmentation:
	"""

	Attributes:

		Segmentation :  Set of Segments,
			set of segments(regions that represent things in frame) in the image

		Quadtree     : 	Quadtree of an image,
			The decomposed image

		Image 		 :  NxMxC numpy array,
			The image that the tree is decomposing

		Cores 		 : collection of Nodes,
			The cores of the Quadtree

		Edges 		 : collection of Nodes,
			The edges of the Quadtree


	Methods:

		Overview of the methods in the class.

		detailed documentation provided below with the function

		__init__ 	:	return None
			Instantiate a segmentation based on a provided image using the Quadtree

		sortNodes 	: 	retrurn boolean,
			Sorts the core Nodes from the quadtree in the desired order
	
		splitRegion :  return Boolean on success
			Using the Quadtree break the Image into its components, fancy BFS


	"""

