import numpy as np
import time
import copy 
import matplotlib.pyplot as plt


def round_robin(agents, items, valuations):
    valuations_copy = copy.deepcopy(valuations)
    items_copy = copy.deepcopy(items)
    start_time = time.time()
    allocations = {}
    # Initialise allocations
    for agent in agents:
        allocations[agent] = []
    for l in range (1, len(items_copy) +1):
        # Choosing agent
        i = l % len(agents)
        values = list(valuations_copy[i].values())
        # Choosing item to asign to agent
        g = np.argmax(values)
        allocations[i].append(items_copy[g])
        # Updating the items and valuations so the just assigned item is not considered
        for agent in agents:
            valuations_copy[agent].pop(items_copy[g])
        items_copy.remove(items_copy[g])
    end_time = time.time()
    runtime = end_time - start_time
    return allocations, runtime

def round_robin_heuristic(agents, items, valuations, indeces):
    valuations_copy = copy.deepcopy(valuations)
    items_copy = copy.deepcopy(items)
    start_time = time.time()
    allocations = {}
    # Initialise allocations
    for agent in agents:
        allocations[agent] = []

    counter = 0
    for l in range (1, len(items_copy) +1):
        # Choosing agent
        if counter < len(indeces):
            i = agents[indeces[counter]]
        else:
            index = (l - 1) // len(indeces)
            i = agents[(indeces[counter % len(indeces)] + index) % len(agents)]
        counter += 1
        values = list(valuations_copy[i].values())
        # Choosing item to asign to agent     
        g = np.argmax(values)
        allocations[i].append(items_copy[g])
        # Updating the items and valuations so the just assigned item is not considered
        for agent in agents:
            valuations_copy[agent].pop(items_copy[g])
        items_copy.remove(items_copy[g])

        if counter == len(agents) * len(indeces):
            counter = 0
    end_time = time.time()
    runtime = end_time - start_time
    return allocations, runtime

