from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import os
import csv


BLACK = (0, 0, 0)
BLUE = (0, 0, 204)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


class WHMap:
	# Class constructor
	def __init__(self):
		path = os.getcwd() + "\\map.xlsx"
		self.results = []
		with open("map.csv") as csvfile:
			reader = csv.reader(csvfile)  # change contents to floats
			for row in reader:  # each row is a list
				self.results.append(row)

		self.ox = []
		self.oy = []
		self.gx = []
		self.gy = []
		self.x = []
		self.y = []
		self.map = []
		for i in range(len(self.results)):
			self.one_map = []
			for j in range(len(self.results[0])):
				if self.results[i][j] == '':
					self.one_map.append(0)
				elif self.results[i][j] == 'x':
					self.one_map.append(1)
					self.ox.append(i)
					self.oy.append(j)
				elif self.results[i][j] == 's':
					self.one_map.append(2)
					self.x.append(i)
					self.y.append(j)
				else:
					self.one_map.append(3)
					self.gx.append(i)
					self.gy.append(j)
			self.map.append(self.one_map)

	def updateMap(self, agentQueue):
		whMap = []
		for r in range(0, len(self.results)):
			row = []
			for c in range(0, len(self.results[0])):
				if self.results[r][c] == '':
					row.append(WHITE)
				elif self.results[r][c] == 'x':
					row.append(BLACK)
				elif self.results[r][c] == 's':
					row.append(BLUE)
				elif self.results[r][c] == 'g':
					row.append(YELLOW)
				else:
					print("No color detected")
			whMap.append(row)

		# Add robots to map
		for agent in agentQueue:
			whMap[agent.X][agent.Y] = RED

		map_array = np.array(whMap, dtype=np.uint8)
		plt.imshow(map_array, interpolation='nearest')
		plt.pause(0.05)

