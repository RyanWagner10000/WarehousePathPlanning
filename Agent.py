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
		self.tour = [0,1,2,3,4,5,6,7,8,18,28,38,48]

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
			self.tour = [48,58,68,78,88,98,99]
		elif self.nMap.goalNodes.count(self.nodeLocationID) > 0:
			return True
		return False

		# # For now, just make random moves
		# rnd = random.random()
		# if rnd <= 0.5:
		# 	self.nodeLocationID = random.choice(self.nMap.nodeMap[self.nodeLocationID].neighbors)
