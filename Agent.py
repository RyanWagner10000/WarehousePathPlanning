import random
import defines


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
		self.waiting = False
		self.foundTarget = False
		self.backTracking = defines.BACK_TRACKING
		# print(self.tour)

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
				self.waiting = False
				if self.nodeLocationID == self.targetID:
					self.foundTarget = True
			elif nextNode == self.nodeLocationID:
				self.tour.pop(0)
			elif self.nMap.nodeMap[nextNode].occupied and self.backTracking:
				if not self.waiting:
					self.waiting = True
				else:
					# Got tired of waiting... Plan a new route
					print("Re-routing old route: ", self.tour)
					curR, curC = self.nMap.idToRC(self.nodeLocationID)
					nxtR, nxtC = self.nMap.idToRC(nextNode)
					rndNode = -1
					if curR - nxtR == -1:
						rndNode = random.choice(self.nMap.topNodes)
					elif curR - nxtR == 1:
						rndNode = random.choice(self.nMap.bottomNodes)
					if curC - nxtC == -1:
						rndNode = random.choice(self.nMap.leftNodes)
					if curC - nxtC == 1:
						rndNode = random.choice(self.nMap.rightNodes)
					if rndNode == -1:
						print("Random node isn't working...", curR, curC, nxtR, nxtC)
						rndNode = random.choice(self.nMap.leftNodes)

					if not self.foundTarget:
						# Route to target
						frntTour = self.nMap.biDir_BFS(self.nodeLocationID, rndNode)
						bckTour = self.nMap.biDir_BFS(rndNode, self.targetID)
						segment1 = frntTour + bckTour
						# route to goal
						segment2 = self.nMap.biDir_BFS(self.targetID, self.goalID)
					else:
						# Route to goal
						segment1 = self.nMap.biDir_BFS(self.nodeLocationID, rndNode)
						segment2 = self.nMap.biDir_BFS(rndNode, self.goalID)
					self.tour = segment1 + segment2
					print(" new route: ", self.tour)
		elif self.nodeLocationID == self.goalID:
			self.nMap.nodeMap[self.nodeLocationID].occupied = False
			return True
		return False
