'''
Simply display the contents of the webcam with optional mirroring using OpenCV
via the new Pythonic cv2 interface.  Press <esc> to quit.
'''

import cv2
import QuadtreeChannels as qt
import networkx as nx
import node_drafts as node
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import time

def show_webcam(mirror=False):
  	cam = cv2.VideoCapture(0)

	while True:
		start_all = time.time()

		#start = time.time()
		ret_val, img = cam.read()
		#end = time.time() - start
		#print end, "image read"

		start = time.time()
		quad = qt.Quadtree(img, 800, 'Variance','quad')
		end = time.time() - start
		print end, "quad"



		"""
		points = quad.getPoints()
		tri = Delaunay(quad.Edges)
		full_u, full_w = node.triangulation_to_CSRMatrix(tri.points, tri.simplices)
		G_w = nx.from_numpy_matrix(full_w)

		nx.draw(G_w, tri.points, node_size = 2)
		plt.savefig("Graph.png", format="PNG")

		img = cv2.imread('Graph.png')
		"""


		"""
		start = time.time()
		if quad.toMatrix(mode = 'corners'):
			img = quad.Matrix
		end = time.time() - start
		print end, "matrix"
		"""

		start = time.time()
		img = quad.toImage(quad.RootNode, mode = "smooth")
		end = time.time() - start
		print end, "images"
		

		if mirror:
			img = cv2.flip(img, 1)

		cv2.imshow('my webcam', img)
		if cv2.waitKey(1) == 27:
			break  # esc to quit

		print time.time() - start_all, "total"
	cv2.destroyAllWindows()

def main():
	show_webcam(mirror=True)

if __name__ == '__main__':
	main()
