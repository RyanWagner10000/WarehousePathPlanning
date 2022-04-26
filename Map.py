from matplotlib import pyplot as plt
import numpy as np
import csv


# Grid colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 204)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
# Node types
EMPTY = 'E'
START = 'S'
SHELF = 'X'
GOAL = 'G'


class Node(object):
	def __init__(self, id):
		self.id = id
		self.neighbors = []
		self.type = None


class WHMap:
	# Class constructor
	def __init__(self):
		self.results = []
		# Read map from .csv
		with open("map.csv") as csvfile:
			reader = csv.reader(csvfile)  # change contents to floats
			for row in reader:  # each row is a list
				self.results.append(row)
		self.rows = len(self.results)
		self.columns = len(self.results[0])
		# Create node map
		self.nodeMap = [None] * self.rows * self.columns
		for r in range(0, self.rows):
			for c in range(0, self.columns):
				# Set node ID
				id = r * self.columns + c
				node = Node(id)
				# Set node type
				node.type = self.results[r][c]
				# Add node to list
				self.nodeMap[id] = node

		# Create neighbors list for each node
		for r in range(0, self.rows):
			for c in range(0, self.columns):
				id = r * self.columns + c
				# Check each neighbor
				if r - 1 >= 0:
					ngID = (r-1) * self.columns + c
					if not self.nodeMap[ngID].type == SHELF:
						self.nodeMap[id].neighbors.append(ngID)
				if c + 1 < self.columns:
					ngID = r * self.columns + (c+1)
					if not self.nodeMap[ngID].type == SHELF:
						self.nodeMap[id].neighbors.append(ngID)
				if r + 1 < self.rows:
					ngID = (r+1) * self.columns + c
					if not self.nodeMap[ngID].type == SHELF:
						self.nodeMap[id].neighbors.append(ngID)
				if c - 1 >= 0:
					ngID = r * self.columns + (c-1)
					if not self.nodeMap[ngID].type == SHELF:
						self.nodeMap[id].neighbors.append(ngID)

		# Sanity prints
		for n in self.nodeMap:
			print(n.id, " : ", n.neighbors)

	def updateMap(self, agentQueue):
		# Create current warehouse map
		whMap = []
		for r in range(0, self.rows):
			row = []
			for c in range(0, self.columns):
				# Determine what color this node should be
				id = r * self.columns + c
				if self.nodeMap[id].type == EMPTY:
					row.append(WHITE)
				elif self.nodeMap[id].type == SHELF:
					row.append(BLACK)
				elif self.nodeMap[id].type == START:
					row.append(BLUE)
				elif self.nodeMap[id].type == GOAL:
					row.append(YELLOW)
				else:
					print("No color detected")
			whMap.append(row)

		# Add robots to map
		for agent in agentQueue:
			whMap[agent.X][agent.Y] = RED

		# Display map
		map_array = np.array(whMap, dtype=np.uint8)
		plt.imshow(map_array, interpolation='nearest')
		plt.pause(0.01)
