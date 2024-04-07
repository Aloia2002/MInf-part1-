def social_welfare(allocations, valuations, agents):
    welfare = 0
    for agent in agents:
        for item in allocations[agent]:
            welfare += valuations[agent][item]
    return welfare

def max_social_welfare (valuations, agents, items):
    welfare = 0
    allocations = {}
    for agent in agents:
        allocations[agent] = []
    for item in items:
        value_item = -1
        for agent in agents: 
            if valuations[agent][item] > value_item:
                chosen_agent = agent
                value_item = valuations[agent][item]
        welfare += value_item
        allocations[chosen_agent].append(item) 

    return welfare, allocations


def price_of_fairness(allocations, valuations, agents, items):
    optimal_welfare, opt_allocations = max_social_welfare(valuations, agents, items)
    alg_werlfare = social_welfare(allocations, valuations, agents)
    return optimal_welfare/alg_werlfare
