from Map import WHMap
import Agent
import random
import time


def runTSUpdates(queue, ids, whMap):
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

	# Update grid-world display
	whMap.updateMap(queue)

	time.sleep(0.5)
	return queue, ids


if __name__ == '__main__':
	print("hello world!")
	agentQueue = []
	agentIDs = 0
	whMap = WHMap()

	# Main simulation loop, runs once per time-step
	while True:
		agentQueue, agentIDs = runTSUpdates(agentQueue, agentIDs, whMap)
