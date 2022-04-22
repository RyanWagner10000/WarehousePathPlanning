
import numpy as np
from PIL import Image
import os
import csv
import Agent
import random
import time

def runTSUpdates(queue, ids):
	print("Running Time-Step Updates")

	# Randomly generate new agents
	rnd = random.random()
	if rnd < 0.1:
		# Create a new agent
		print("Creating new agent ", ids)
		queue.append(Agent.Agent(ids))
		ids += 1

	# Run updates on each agent
	for agent in queue:
		agent.update()

	# Update grid-world display here

	time.sleep(0.5)
	return queue, ids

  if __name__ == '__main__':
    print("hello world!")
    agentQueue = []
    agentIDs = 0

  black = (0,0,0)
  blue = (0,0,204)
  yellow = (255,255,0)
  red = (102,204,0)
  white = (255,255,255)

  path = os.getcwd() + "\\map.xlsx"

  results = []
  with open("map.csv") as csvfile:
      reader = csv.reader(csvfile) # change contents to floats
      for row in reader: # each row is a list
          results.append(row)

  map = []

  for r in range(0,len(results)):
      row = []
      for c in range(0,len(results[0])):
          if results[r][c] == '':
              row.append(white)
          elif results[r][c] == 'x':
              row.append(black)
          elif results[r][c] == 's':
              row.append(blue)
          elif results[r][c] == 'g':
              row.append(yellow)
          else:
              print("No color detected")
      map.append(row)

  map_array = np.array(map, dtype=np.uint8)
  map_image = Image.fromarray(map_array)
  map_image = map_image.resize((500, 500), resample=Image.NEAREST)
  map_image.save("map.png")
  map_image.show()

	# Main simulation loop, runs once per time-step
	while True:
		agentQueue, agentIDs = runTSUpdates(agentQueue, agentIDs)
