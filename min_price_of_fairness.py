import envy_free_check as ef
import copy 
import time

# Algorithm for 2 agents that gives the minimum price of fairness
def min_price_of_fairness(agents, items, valuations):
    start_time = time.time()
    allocations = {}
    # Initialise allocations
    for agent in agents:
        allocations[agent] = []
    ratio = {}
    for item in items:
        ratio[item] = valuations[0][item] / valuations[1][item]
    sorted_ratios = sorted(ratio.items(), key=lambda x: x[1], reverse=True)
    sorted_ratios_2 = copy.deepcopy(sorted_ratios)
    for i in sorted_ratios_2:
        allocations[0].append(i[0])
        sorted_ratios.remove(i)
        for j in sorted_ratios:
            allocations[1].append(j[0])
        if(ef.check_EF1(allocations, agents, valuations)):
            break
        else:
            allocations[1] = []
    end_time = time.time()
    runtime = end_time - start_time
    return allocations, runtime

