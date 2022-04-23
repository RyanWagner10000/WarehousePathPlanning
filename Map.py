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

		# map_array = np.array(self.whMap, dtype=np.uint8)
		#
		# plt.imshow(map_array, interpolation='nearest')
		# plt.show()
		#
		# self.map_image = Image.fromarray(map_array)
		# self.map_image = self.map_image.resize((500, 500), resample=Image.NEAREST)

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
		# plt.show6()
		# # Add robots here!
		# map_array = np.array(currentMap, dtype=np.uint8)
		# self.map_image = Image.fromarray(map_array)
		# self.map_image = self.map_image.resize((500, 500), resample=Image.NEAREST)
		# # self.map_image.save("map.png")
		# self.map_image.show()
