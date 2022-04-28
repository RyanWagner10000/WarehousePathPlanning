from Map import WHMap
import Agent
import random
import time


def runTSUpdates(queue, ids, whMap):
	print("Running Time-Step Updates")
	# Randomly generate new agents
	rnd = random.random()
	if rnd < 0.25:
	# Create a new agent
		print("Creating new agent ", ids)
		queue.append(Agent.Agent(ids, whMap, random.choice(whMap.startNodes),
		                         	random.choice(whMap.targetNodes),
		                         	random.choice(whMap.goalNodes)))
		ids += 1

	# Run updates on each agent
	for agent in queue:
		if agent.update():
			queue.remove(agent)

	# Update grid-world display
	whMap.updateMap(queue)

	time.sleep(0.1)
	return queue, ids


if __name__ == '__main__':
	print("hello world!")
	agentQueue = []
	agentIDs = 0
	whMap = WHMap()

	# Main simulation loop, runs once per time-step
	for i in range(0, 200):
		while len(agentQueue) < 40:
			agentQueue, agentIDs = runTSUpdates(agentQueue, agentIDs, whMap)
