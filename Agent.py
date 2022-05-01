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
		self.dynReplan = defines.DYNAMIC_REPLAN
		self.contReplan = defines.CONTINUOUS_REPLAN
		self.lifeTime = 0
		# print(self.tour)

	# Well-defined position update
	def updatePosition(self, dx, dy):
		if self.X + dx >= 0:
			self.X += dx
		if self.Y + dy >= 0:
			self.Y += dy

	def update(self):
		print("Updating agent position!")
		self.lifeTime = self.lifeTime + 1
		if self.tour:
			if self.contReplan and self.lifeTime % 3 == 0:
				# Replan again
				if not self.foundTarget:
					segment1 = self.nMap.biDir_BFS(self.nodeLocationID, self.targetID, True)
					segment2 = self.nMap.biDir_BFS(self.targetID, self.goalID, True)
					if not segment1 == [] and not segment2 == []:
						segment1.pop(0)
						self.tour = segment1 + segment2
					else:
						self.backTracking = True
				else:
					seg = self.nMap.biDir_BFS(self.nodeLocationID, self.goalID, True)
					if not seg == []:
						seg.pop(0)
						self.tour = seg
					else:
						self.backTracking = True
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
					# print("Re-routing old route: ", self.tour)
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
						# print("Random node isn't working...", curR, curC, nxtR, nxtC)
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
					# print(" new route: ", self.tour)
					# Check to see if we are actually in dynamic re-planning
					if self.dynReplan or self.contReplan:
						# Don't continue to back-track
						self.backTracking = False
			elif self.nMap.nodeMap[nextNode].occupied and self.dynReplan:
				if not self.waiting:
					self.waiting = True
				else:
					rndNum = random.random()
					if rndNum <= 0.5:
						# Got tired of waiting... Plan a new route
						# print("** Re-routing old route: ", self.tour)
						if not self.foundTarget:
							# Route to target, then to goal
							# print(" Plan location -> target -> goal")
							segment1 = self.nMap.biDir_BFS(self.nodeLocationID, self.targetID, True)
							segment2 = self.nMap.biDir_BFS(self.targetID, self.goalID, True)
							if not segment1 == [] and not segment2 == []:
								self.tour = segment1 + segment2
							else:
								self.backTracking = True
						else:
							# Route to goal
							# print(" Plan location -> goal")
							segment = self.nMap.biDir_BFS(self.nodeLocationID, self.goalID, True)
							if not segment == []:
								self.tour = segment
							else:
								self.backTracking = True
		elif self.nodeLocationID == self.goalID:
			self.nMap.nodeMap[self.nodeLocationID].occupied = False
			return True
		return False
