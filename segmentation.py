import numpy as np
import jig
import QuadtreeChannels as qt
import node_drafts as nd

from scipy.spatial import Delaunay


class Segmentation:
	"""

	Attributes:

		Segmentation :  Set of Jigs,
			set of Jigs(regions that represent things in frame) in the image

		Quadtree     : 	Quadtree of an image,
			The decomposed image

		Image 		 :  NxMxC numpy array,
			The image that the tree is decomposing

		Adjacency 	 : KxK numpy array,
			The csr Matrix of the triangulation

		Cores 		 : collection of Nodes,
			The cores of the Quadtree

		Edges 		 : collection of Nodes,
			The edges of the Quadtree

		Locus 		 : collection of Coordinate pairs
			The centers of the jigs

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

	Segmentation = []
	Quadtree 	 = None
	Image 		 = None

	Adjacency 	 = None
	Cores 		 = {}
	Edges 		 = {}
	Locus		 = []
	IDs 		 = []

	Unclaimed 	 = []


	def __init__(self, image, tol, mode, partition):
		"""

		Initializes a segmentation based on provided data 

		"""
		# store image
		self.Image = image


		# build quadtree from parameters
		self.Quadtree = qt.Quadtree(image,tol,mode,partition)


		# build the cores and edges from the quadtree
		points = self.Quadtree.getPoints()

		#self.Unclaimed = set(points)

		self.Edges = self.Quadtree.Edges
		self.Cores = self.Quadtree.Cores


		# build the CSR Matrix from the triangualtion
		triangualtion = Delaunay(points)

		self.Adjacency, unweighted, self.IDs = nd.triangualtion_to_CSRMAtrix(triangulation.points, triangualtion.simplicies)

		# Locuses will be build later


	def sortNodes(self, mode = "depth"):
		"""
		Sorts the nodes based on some mode


		Inputs:
			mode: string
				determines which axis to sort the cores by.

		Methods:

		"""
		"""
		N = len(self.Cores)
		# determine where things were sorted to
		base_locs = range(N)
		keys = range(N)
		"""
	

		proto_list = [core.Depth for core in self.Cores]

		ordering = zip(proto_list,self.IDs[0,len(self.Cores)])

		ordering.sort(keys = lambda x : x[0])
		print ordering


	def modifiedBFS(self):
		"""
		Breaks image into its component jigs

		Inputs:


		Outputs:
			Returns true/false if search completes successfully or doesn't complete at all


		"""

		#self.IDs
		ordered = sortNodes()
		visited = np.zeros_like(ordered)
		cnt = 0

		def build_jig(self, jig, origin_nodeID, current_nodeID):

			def compareNode(current_nodeID, origin_nodeID):

			

			#Make sure Node has not been visited
			if visited[cnt] == 0:
			
				current_node = #properly assign node from an ID 


				#If it's an Edge we add it
				if current_node is in self.Edges:
					jig.Edges.append(current_nodeID)


				#If it's a Core make sure it's similar enough, 
				elif current_node is in self.Cores:


					#Check if this is a new jig

					# check
					if origin_nodeID is not None:
						compareNode(origin_nodeID, current_nodeID)


					#If it is new, add the Core then find neighbors
					else:

						# add the node to the jig
						jig.Cores.append(current_nodeID)
						visited[current_nodeID] = 1
						indices = npy.nonzero(self.Adjacency[current_nodeID])

						# find the neighbors and recurse through them
						for index in indices:
							build_jig(jig, current_nodeID,index)

				else
					raise ValueError("What the h3ll did you do man")
			

			#Skip it
			elif visited[cnt] == 1:
				pass
			else:
				raise ValueError("What the h3ll did you do man?")			

		while cnt < len(visited):

			if visited[cnt] == 0:
				temp_jig = jig.jig()
				build_jig(temp_jig, None, ordered[cnt])
				self.Segmentation.append(temp)				
			elif visited[cnt] == 1:
				cnt += 1
			else:
				raise ValueError("What the h3ll did you do man?")		
			





