import random
import time

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
		self.previousPos = []
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
				time.sleep(0.01)
				self.previousPos.append(self.tour.pop(0))
			elif nextNode == self.targetID and self.nodeLocationID == self.targetID:
				self.tour.pop(0)
				self.previousPos.append(self.tour.pop(0))
			elif self.nMap.nodeMap[nextNode].occupied:
				iteration = 0
				if len(self.previousPos) > 2:
					iteration = random.randint(1,int(len(self.previousPos)/2))
				else:
					iteration = 1
				counter = 0
				step_history = []
				while counter < iteration and len(self.previousPos) > 0:
					self.nMap.nodeMap[self.nodeLocationID].occupied = False
					nextNode = self.previousPos.pop(-1)
					self.nodeLocationID = nextNode
					self.nMap.nodeMap[nextNode].occupied = True
					time.sleep(0.01)
					counter = counter + 1
				step_history = self.previousPos[(len(self.previousPos) - iteration) : -1]
				print('this is step history: ', step_history)
				for i in range(len(step_history)):
					self.tour.insert(0,step_history[i])
				print('this is tour: ', self.tour)
		elif self.nodeLocationID == self.goalID:
			self.nMap.nodeMap[self.nodeLocationID].occupied = False
			return True
		return False
