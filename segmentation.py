import numpy as np
import jig
import QuadtreeChannels as qt
import node_drafts as nd

from scipy.spatial import Delaunay

GREATER_THRESHOLD = 60
NUM_SKIPPED = 0


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

		self.Nodes = self.Cores + self.Edges


		# build the CSR Matrix from the triangualtion
		triangulation = Delaunay(points)

		self.Adjacency, unweighted = nd.triangulation_to_CSRMatrix(triangulation.points, triangulation.simplices)


		self.IDs = range(0,len(points))

		# Locuses will be build later

		self.modifiedBFS()


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

		ordering = zip(proto_list,self.IDs[0:len(self.Cores)])

		ordering.sort(key = lambda x : x[0])


		return ordering

	def build_jig(self, jig, origin_nodeID, current_nodeID,visited):
		#print len(jig.Cores_Nodes)

		def compareNode(current_nodeID, origin_nodeID):
			"""

			checks if the nodes are "similar" enough

			inputs:

				*_nodeID : the id's of the nodes we want to compare

			return 

				boolean, are they similar enough
			"""
			current_node, origin_node = self.Cores[current_nodeID], self.Cores[origin_nodeID]

			color_current, color_origin =  current_node.Color, origin_node.Color

			distance = 0

			for color in xrange(len(color_current)):
				distance += (color_current[color] - color_origin[color]) **2

			if (distance)**.5 > GREATER_THRESHOLD:
				return False
			else:
				return True 



		#Make sure Node has not been visited
		if visited[current_nodeID] == 0:
			
			current_node = self.Nodes[current_nodeID]#properly assign node from an ID 

			#If it's an Edge we add it
			if current_node in self.Edges: #and current_node not in jig.Edges_Nodes:
				
				#make sure we don't add the same edge repeatedly
				if current_node not in jig.Edges_Nodes:
					jig.Edges_Nodes.append(current_node)

			#If it's a Core make sure it's similar enough, 
			elif current_node in self.Cores:

				#Check if this is a new jig

				# check
				if origin_nodeID is not None:
				#print current_nodeID, "boof"
				# If the node is similar enough add it to visited, and the Jig and recurse
					if compareNode(origin_nodeID, current_nodeID):
						visited[current_nodeID] = 1
						jig.Cores_Nodes.append(current_node)

						# find each node connected to the current_node
						indices = np.nonzero(self.Adjacency[current_nodeID])[0]

						# find the neighbors and recurse through them
						for index in indices:
							self.build_jig(jig, current_nodeID, index, visited)

					else:

						pass

				#If it is new, add the Core then find neighbors
				else:

					# add the node to the jig
					jig.Cores_Nodes.append(current_node)

					# mark the node as visited
					visited[current_nodeID] = 1
					
					# find the neighboring nodes
					indices = np.nonzero(self.Adjacency[current_nodeID])[0]
					#print indices[0]
					# find the neighbors and recurse through them
					
					for index in indices:
						#print index
						self.build_jig(jig, current_nodeID, index,visited)

			else:
				raise ValueError("What the h3ll did you do man")
		

		#Skip it
		elif visited[current_nodeID] == 1:
			pass	
		else:
			#print visited[current_nodeID] , "da fu"
			raise ValueError("What the h3ll did you do man?")			

	def modifiedBFS(self):
		"""
		Breaks image into its component jigs

		Inputs:


		Outputs:
			Returns true/false if search completes successfully or doesn't complete at all


		"""

		ordered = self.sortNodes()
		visited = np.zeros(len(self.Nodes))
		countID = 0

		
		while countID < len(ordered):
			#print countID
			
			#print visited
			if visited[countID] == 0:

				temp_jig = jig.jig()
				self.build_jig(temp_jig, None, ordered[countID][1],visited)
				if len(temp_jig.Cores_Nodes) > 0:
					self.Segmentation.append(temp_jig)	



				countID += 1

			elif visited[countID] == 1:
				
				countID += 1

			else:
				raise ValueError("What the h3ll did you do man?")		
	
	def displaySegments(self):

		shape = self.Image.shape
		print len(self.Segmentation), " segments found"

		toDisplay = []

		for jig in self.Segmentation:
			tempColor = np.random.randint(0,100)#counter #(counter,counter,counter)
			pic = jig.display(shape,tempColor)
			toDisplay.append(pic)		
			



		return toDisplay




