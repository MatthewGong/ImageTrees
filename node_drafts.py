import QuadtreeChannels as qt
import cv2 as cv
import numpy as np
import time
import networkx as nx

from scipy.spatial import Delaunay, ConvexHull
from scipy.spatial import Voronoi, voronoi_plot_2d

from scipy.sparse.csgraph import minimum_spanning_tree

import matplotlib.pyplot as plt
"""
path = r"C:\Users\Matth\Documents\seniorcoding\Project\Videos\SteeringWheel\raw\SteeringWheel_0001.jpg"#pass in an image
image = cv.imread(path)


start = time.time()
quad = qt.Quadtree(image,12,'Manhattan','quad')
end = time.time()-start

print "Compress: " +  str(quad.nodecount()/float(image.shape[0]*image.shape[1]))
print "Run time: " +  str(end)

output = quad.toImage(quad.RootNode, mode = "smooth")

start = time.time()
quad2 = qt.Quadtree(image,600,'Variance','quad')
end = time.time()-start

print "Compress: " +  str(quad2.nodecount()/float(image.shape[0]*image.shape[1]))
print "Run time: " +  str(end)

if quad2.toMatrix():
	pass
	plt.imshow(quad2.Matrix, cmap= 'gray')
	plt.title('Matrix Representation')
	plt.show()


points = quad2.getPoints()
tri = Delaunay(points)
plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
plt.plot(points[:,0], points[:,1], 'o')
plt.ylim(-1080,0)
plt.xlim(0,1920)
plt.title('Delanauy Triangulation')
plt.show()


points2 = np.array(quad2.Edges)


tri2 = Delaunay(points2)
plt.triplot(points2[:,0], points2[:,1], tri2.simplices.copy())
plt.plot(points2[:,0], points2[:,1], 'o')
plt.ylim(-1080,0)
plt.xlim(0,1920)
plt.title('Refined Delanauy Triangulation')
plt.show()


"""
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
	print edges
	return weight_adjacency, unweighted_adjacency
"""
weighted, unweighted = triangulation_to_CSRMatrix(tri2.points, tri2.simplices)

G_w = nx.from_numpy_matrix(weighted)
G_u = nx.from_numpy_matrix(unweighted)

plt.title('Full')
nx.draw(G_u, tri2.points, node_size = 2)
plt.show()

minimal = minimum_spanning_tree(weighted)


min_graph = nx.from_numpy_matrix(minimal.toarray().astype(int))

plt.title('Minimal Spanning')
nx.draw(min_graph, tri2.points, node_size = 2)
plt.show()

weighted2, unweighted2 = triangulation_to_urquhart(tri2.points, tri2.simplices)
print np.sum(weighted)-np.sum(weighted2)
print np.sum(unweighted)-np.sum(unweighted2)

print unweighted2
G_w2 = nx.from_numpy_matrix(weighted2)
G_u2 = nx.from_numpy_matrix(unweighted2)

plt.title('Urquhart')
nx.draw(G_w2, tri2.points, node_size = 2)
plt.show()

minimal2 = minimum_spanning_tree(weighted2)
#print minimal2

plt.title('Min from urquhart')
min_graph = nx.from_numpy_matrix(minimal2.toarray().astype(int))
nx.draw(min_graph, tri2.points, node_size = 2)
plt.show()"""
