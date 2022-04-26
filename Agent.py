import random


class Agent:
	# Class constructor. id is agent ID, x,y are agents initial position on grid
	def __init__(self, id, nMap, x=0, y=0, nID=0):
		self.ID = id
		self.nMap = nMap
		# Starting position of agent
		self.X = x
		self.Y = y
		self.nodeLocationID = nID

	# Well-defined position update
	def updatePosition(self, dx, dy):
		if self.X + dx >= 0:
			self.X += dx
		if self.Y + dy >= 0:
			self.Y += dy

	def update(self):
		print("Updating agent position!")

		# For now, just make random moves
		rnd = random.random()
		if rnd <= 0.5:
			self.nodeLocationID = random.choice(self.nMap.nodeMap[self.nodeLocationID].neighbors)
