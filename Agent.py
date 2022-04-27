import random


class Agent:
	# Class constructor. id is agent ID, x,y are agents initial position on grid
	def __init__(self, id, nMap, nID=0, targetID=0, goalID=0):
		self.ID = id
		self.nMap = nMap
		# Starting position of agent
		self.nodeLocationID = nID
		# Target location
		self.targetID = targetID
		# Goal location
		self.goalID = goalID
		frntTour = self.nMap.biDir_BFS(nID, targetID)
		bckTour = self.nMap.biDir_BFS(targetID, goalID)
		self.tour = frntTour + bckTour
		print(self.tour)

	# Well-defined position update
	def updatePosition(self, dx, dy):
		if self.X + dx >= 0:
			self.X += dx
		if self.Y + dy >= 0:
			self.Y += dy

	def update(self):
		print("Updating agent position!")
		if self.tour:
			nextNode = self.tour[0]
			if not self.nMap.nodeMap[nextNode].occupied:
				self.nMap.nodeMap[self.nodeLocationID].occupied = False
				self.nodeLocationID = nextNode
				self.nMap.nodeMap[nextNode].occupied = True
				self.tour.pop(0)
			elif nextNode == self.targetID and self.nodeLocationID == self.targetID:
				self.tour.pop(0)
		elif self.nodeLocationID == self.goalID:
			self.nMap.nodeMap[self.nodeLocationID].occupied = False
			return True
		return False
