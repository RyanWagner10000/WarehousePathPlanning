from matplotlib import pyplot as plt
import numpy as np
import csv
import defines


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
UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'


def oppositeMove(moveA, moveB):
	test1 = (moveA == DOWN and moveB == UP)
	test2 = (moveA == UP and moveB == DOWN)
	test3 = (moveA == LEFT and moveB == RIGHT)
	test4 = (moveA == RIGHT and moveB == LEFT)
	return test1 or test2 or test3 or test4


def emptyTypeNode(nodeType):
	return nodeType == UP or nodeType == DOWN or nodeType == LEFT or nodeType == RIGHT


class Node(object):
	def __init__(self, id):
		self.id = id
		self.neighbors = []
		self.type = None
		self.occupied = False


class WHMap:
	# Class constructor
	def __init__(self):
		results = []
		# Read map from .csv
		with open(defines.FILE) as csvfile:
			reader = csv.reader(csvfile)  # change contents to floats
			for row in reader:  # each row is a list
				results.append(row)
		self.rows = len(results)
		self.columns = len(results[0])
		self.startNodes = []
		self.goalNodes = []
		self.targetNodes = []
		self.topNodes = []
		self.bottomNodes = []
		self.leftNodes = []
		self.rightNodes = []
		self.oneWayMap = False
		# Create node map
		self.nodeMap = [None] * self.rows * self.columns
		for r in range(0, self.rows):
			for c in range(0, self.columns):
				# Set node ID
				id = r * self.columns + c
				node = Node(id)
				# Set node type
				node.type = results[r][c]
				if node.type == UP or node.type == DOWN or node.type == LEFT or node.type == RIGHT:
					self.oneWayMap = True
				# Add node to list
				self.nodeMap[id] = node
				# Check if this is a start node
				if node.type == START:
					# Add node to start node list
					self.startNodes.append(id)
				# Check if this is a goal node
				if node.type == GOAL:
					# Add node to goal node list
					self.goalNodes.append(id)
		# If using one-ways map, create special neighbors list
		if self.oneWayMap:
			for r in range(0, self.rows):
				for c in range(0, self.columns):
					id = r * self.columns + c
					# Verify this isn't a shelf
					if not self.nodeMap[id].type == SHELF:
						# Check each neighbor
						if r - 1 >= 0:
							ngID = (r-1) * self.columns + c
							if not self.nodeMap[ngID].type == SHELF and not self.nodeMap[ngID].type == DOWN and \
									not self.nodeMap[id].type == DOWN and \
									not oppositeMove(self.nodeMap[id].type, self.nodeMap[ngID].type):
								self.nodeMap[id].neighbors.append(ngID)
						if c + 1 < self.columns:
							ngID = r * self.columns + (c+1)
							if not self.nodeMap[ngID].type == SHELF and not self.nodeMap[ngID].type == LEFT and \
									not self.nodeMap[id].type == LEFT and \
									not oppositeMove(self.nodeMap[id].type, self.nodeMap[ngID].type):
								self.nodeMap[id].neighbors.append(ngID)
							elif emptyTypeNode(self.nodeMap[id].type):
								self.targetNodes.append(id)
						if r + 1 < self.rows:
							ngID = (r+1) * self.columns + c
							if not self.nodeMap[ngID].type == SHELF and not self.nodeMap[ngID].type == UP and \
									not self.nodeMap[id].type == UP and \
									not oppositeMove(self.nodeMap[id].type, self.nodeMap[ngID].type):
								self.nodeMap[id].neighbors.append(ngID)
						if c - 1 >= 0:
							ngID = r * self.columns + (c-1)
							if not self.nodeMap[ngID].type == SHELF and not self.nodeMap[ngID].type == RIGHT and \
									not self.nodeMap[id].type == RIGHT and \
									not oppositeMove(self.nodeMap[id].type, self.nodeMap[ngID].type):
								self.nodeMap[id].neighbors.append(ngID)
							elif emptyTypeNode(self.nodeMap[id].type):
								self.targetNodes.append(id)
		else:
			# Create regular neighbors list for each node
			for r in range(0, self.rows):
				for c in range(0, self.columns):
					id = r * self.columns + c
					# Verify this isn't a shelf
					if not self.nodeMap[id].type == SHELF:
						# Check each neighbor
						if r - 1 >= 0:
							ngID = (r-1) * self.columns + c
							if not self.nodeMap[ngID].type == SHELF:
								self.nodeMap[id].neighbors.append(ngID)
						if c + 1 < self.columns:
							ngID = r * self.columns + (c+1)
							if not self.nodeMap[ngID].type == SHELF:
								self.nodeMap[id].neighbors.append(ngID)
							elif self.nodeMap[id].type == EMPTY:
								self.targetNodes.append(id)
						if r + 1 < self.rows:
							ngID = (r+1) * self.columns + c
							if not self.nodeMap[ngID].type == SHELF:
								self.nodeMap[id].neighbors.append(ngID)
						if c - 1 >= 0:
							ngID = r * self.columns + (c-1)
							if not self.nodeMap[ngID].type == SHELF:
								self.nodeMap[id].neighbors.append(ngID)
							elif self.nodeMap[id].type == EMPTY:
								self.targetNodes.append(id)
						# Check if this is a good node to return to when stuck
						if r == 0:
							self.topNodes.append(id)
						if r == self.rows - 1:
							self.bottomNodes.append(id)
						if c == 0:
							self.leftNodes.append(id)
						if c == self.columns - 1:
							self.rightNodes.append(id)
		# Sanity prints
		for n in self.nodeMap:
			print(n.id, " : ", n.neighbors)

	def idToRC(self, id):
		r = id // self.columns
		c = id - (self.columns * r)
		return r, c

	def updateMap(self, agentQueue):
		# Create current warehouse map
		whMap = []
		for r in range(0, self.rows):
			row = []
			for c in range(0, self.columns):
				# Determine what color this node should be
				id = r * self.columns + c
				if self.nodeMap[id].type == EMPTY or self.nodeMap[id].type == UP or self.nodeMap[id].type == DOWN or \
						self.nodeMap[id].type == LEFT or self.nodeMap[id].type == RIGHT:
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
			R, C = self.idToRC(agent.nodeLocationID)
			red = list(RED)
			red[2] = (agent.ID * 35) % 255
			red[1] = (agent.ID * 10) % 150
			whMap[R][C] = tuple(red)

		# Display map
		map_array = np.array(whMap, dtype=np.uint8)
		plt.imshow(map_array, interpolation='nearest')
		plt.pause(0.01)

	def biDir_BFS(self, startID, endID):
		# print("Find path: ", startID, endID)
		root = [None] * self.rows * self.columns
		for r in range(0, len(root)):
			root[r] = -1

		queue = []
		root[startID] = startID
		queue.append(startID)

		while queue:
			n = queue.pop(0)
			# print(n, ":")

			for nbr in self.nodeMap[n].neighbors:
				# print(nbr, end=" ")
				if root[nbr] == -1:
					root[nbr] = n
					queue.append(nbr)
					if nbr == endID:
						# Found node!
						# print("Found node!")
						queue = []
						break
			# print("")

		# Determine resulting tour
		result = []
		crNode = endID
		result.append(crNode)
		# print("Resulting tour:")
		# print(" ", crNode, end=" ")
		while not crNode == startID:
			crNode = root[crNode]
			result.insert(0, crNode)
			# print(crNode, end=" ")

		# print("")
		# print(result)
		return result
