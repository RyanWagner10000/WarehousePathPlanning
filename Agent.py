import random


class Agent:
	# Class constructor. id is agent ID, x,y are agents initial position on grid
	def __init__(self, id, nMap, nID=0, targetID=0):
		self.ID = id
		self.nMap = nMap
		# Starting position of agent
		self.nodeLocationID = nID
		# Target location
		self.targetID = targetID
		self.tour = self.nMap.biDir_BFS(nID, targetID)
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
			self.nodeLocationID = self.tour[0]
			self.tour.pop(0)
		elif self.nodeLocationID == self.targetID:
			# Find new path to a goal node (the first goal node)
			self.tour = self.nMap.biDir_BFS(self.nodeLocationID, self.nMap.goalNodes[0])
		elif self.nMap.goalNodes.count(self.nodeLocationID) > 0:
			return True
		return False
