import copy

# Gets how much an agent values a given allocation
def valuation_allocation(agent, valuations, allocation):
    valuation = 0
    if len(allocation) == 0:
        return valuation
    # Iterate thorugh the allocation
    for item in allocation:
        # Add the value of the item to the valuation
        valuation = valuation + valuations[agent][item]
    return valuation


def check_EF(allocations, agents, valuations):
    for agent in agents:
        for agent2 in agents:
            if agent != agent2:
                # Checks if any agent envies another agent
                if valuation_allocation(agent, valuations, allocations[agent]) < valuation_allocation(agent, valuations, allocations[agent2]):
                    return False
    return True


def check_EF1(allocations, agents, valuations):
    count_ef1 = 0
    i= -1
    n_envy = 0
    for allocation in allocations.values():
        i = i + 1
        for agent_envy in agents:
            for agent_envied in agents:
                if agent_envy != agent_envied:
                    # Checks if any agent envies another agent
                    if (valuation_allocation(agent_envy, valuations, allocations[agent_envied]) > valuation_allocation(agent_envy, valuations, allocations[agent_envy])):
                        n_envy += 1
                        allocation = [allocation]
                        for item in allocations[agent_envied]:
                            new_bundle = copy.deepcopy(allocations[agent_envied])
                            new_bundle.remove(item)
                            # Checks if the agent is still envious after removing the item
                            if (valuation_allocation(agent_envy, valuations, new_bundle) <= valuation_allocation(agent_envy, valuations, allocations[agent_envy])):
                                count_ef1 += 1
                                break
                    break

    # If the envy of all agents is gone when we remove one item from the bundle, then it is EF1
    if count_ef1 == n_envy:
        return True
    else :
        return False
    
def check_EFX(allocations, agents, valuations):
    n_envy_gone = 0
    my_list = []
    for agent in agents:
        for agent2 in agents:
            if agent != agent2:
                n_envy_gone= 0
                # Checks if any agent envies another agent
                if valuation_allocation(agent, valuations, allocations[agent]) < valuation_allocation(agent, valuations, allocations[agent2]):
                    for item in allocations[agent2]:
                        new_bundle = copy.deepcopy(allocations[agent2])
                        new_bundle.remove(item)
                        # Checks if the agent is still envious after removing the item
                        if (valuation_allocation(agent, valuations, new_bundle) <= valuation_allocation(agent, valuations, allocations[agent])):
                            n_envy_gone += 1
                    #  Checks if the envy of one agent disappears with removing any of the items
                    if n_envy_gone == len(allocations[agent2]):
                        my_list.append(True)
                    else:
                        my_list.append(False)
    # Checks if for all the agents the envy disappears with removing any of the items
    if all(my_list):
        return True
    else:
        # print(my_list)
        return False

def check_alpha_EFX(allocations, agents, valuations, alpha):
    n_envy_gone = 0
    my_list = []
    agents_alpha = []
    for agent in agents:
        for agent2 in agents:
            if agent != agent2:
                n_envy_gone= 0
                # Checks if any agent envies another agent
                if valuation_allocation(agent, valuations, allocations[agent]) < valuation_allocation(agent, valuations, allocations[agent2]):
                    for item in allocations[agent2]:
                        new_bundle = copy.deepcopy(allocations[agent2])
                        new_bundle.remove(item)
                        # Checks if the agent is still envious after removing the item
                        if (alpha * valuation_allocation(agent, valuations, new_bundle)) <= valuation_allocation(agent, valuations, allocations[agent]):
                            n_envy_gone += 1
                    #  Checks if the envy of one agent disappears with removing any of the items
                    if n_envy_gone == len(allocations[agent2]):
                        my_list.append(True)
                    else:
                        my_list.append(False)
                        if agent not in agents_alpha:
                            agents_alpha.append(agent)
    # Checks if for all the agents the envy disappears with removing any of the items
    if all(my_list):
        return True
    else:
        # print(my_list)
        return False, agents_alpha



