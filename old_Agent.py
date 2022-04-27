import random


class Agent:
	# Class constructor. id is agent ID, x,y are agents initial position on grid
	def __init__(self, id, x=0, y=0):
		self.ID = id
		# Starting position of agent
		self.X = x
		self.Y = y

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
		if rnd < 0.1:
			self.updatePosition(1, 0)
		elif rnd < 0.2:
			self.updatePosition(-1, 0)
		elif rnd < 0.3:
			self.updatePosition(0, 1)
		elif rnd < 0.4:
			self.updatePosition(0, -1)
