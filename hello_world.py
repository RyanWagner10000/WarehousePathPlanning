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

	# Main simulation loop, runs once per time-step
	while True:
		agentQueue, agentIDs = runTSUpdates(agentQueue, agentIDs)
