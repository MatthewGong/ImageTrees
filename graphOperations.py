import numpy as np


def triangulation_to_CSRMatrix(points, simplices):
	edges = 0
	def distance(point_a, point_b):

		# find the euclidean distance between two points
		# for our purposes we can leave them squared to preserve integersT
		# and further penalize long lines

		del_x = (point_a[0] - point_b[0]) **2
		del_y = (point_a[1] - point_b[1]) **2

		distance = del_x + del_y

		return distance

	N = len(points)

	# instantiate an empty adjacency matrix the size of the number of nodes
	weight_adjacency     = np.zeros((N,N))
	unweighted_adjacency = np.zeros_like(weight_adjacency)

	# iterate the triangulation and find all of the edges, fill in the adjacency matricies
	for simplex in simplices:
		#
		for i in xrange(len(simplex)):
			a = i
			b = (i+1)%3
			#print points[simplex[a]], points[simplex[b]]
			#print simplex[a],simplex[b]

			# compute the length between nodes
			length = distance(points[simplex[a]], points[simplex[b]])

			# make the matricies symmetric
			weight_adjacency[simplex[a],simplex[b]] = length
			#weight_adjacency[simplex[b],simplex[a]] = length

			unweighted_adjacency[simplex[a],simplex[b]] = 1
			#unweighted_adjacency[simplex[b],simplex[a] = 1
			edges += 1
	print edges
	return weight_adjacency, unweighted_adjacency

def triangulation_to_urquhart(points, simplices):
	edges = 0

	def distance(point_a, point_b):

		# find the euclidean distance between two points
		# for our purposes we can leave them squared to preserve integers
		# and further penalize long lines

		del_x = (point_a[0] - point_b[0]) **2
		del_y = (point_a[1] - point_b[1]) **2

		distance = del_x + del_y

		return distance

	# def min_angle(point_a, point_b, point_c):
	# 	angles = []

	# 	angles_a
	# 	angles_b

	# 	return min(angles)

	N = len(points)

	# instantiate an empty adjacency matrix the size of the number of nodes
	weight_adjacency     = np.zeros((N,N))
	unweighted_adjacency = np.zeros_like(weight_adjacency)

	# iterate the triangulation and find all of the edges, fill in the adjacency matricies
	for simplex in simplices:

		longest = 0
		shortest = np.inf
		shortest_index = 0
		longest_index = 0

		lengths = []

		# find the longest edge and remove it
		for i in xrange(len(simplex)):
			a = i
			b = (i+1)%3

			# compute the length between node_size
			length = distance(points[simplex[a]], points[simplex[b]])
			lengths.append(length)
			#check if the node is the longest
			if length > longest:
				longest = length
				longest_index = i
			if length < shortest:
				shortest = length
				shortest_index = i

		for j in xrange(len(simplex)):
			a = j
			b = (j+1)%3

			"""
			if lengths[j] < min_len:
				min_len = lengths[j]
			"""
			# if it isn't the longest line add it to the adjacency matrix

			# not the longest
			#if j != longest_index:

			# not the shortest
			#if j != shortest_index:

			# not the middle
			#if j == longest_index or j == shortest_index:

			# only the shortest
			#if j == longest_index:

			# only the shortest
			#if j == shortest_index:

			# only the middle
			if j != longest_index and j != shortest_index:

				# make the matricies symmetric
				weight_adjacency[simplex[a],simplex[b]] = lengths[j]
				#weight_adjacency[simplex[b],simplex[a]] = length

				unweighted_adjacency[simplex[a],simplex[b]] = 1
				#unweighted_adjacency[simplex[b],simplex[a] = 1
				edges += 1

	return weight_adjacency, unweighted_adjacency
