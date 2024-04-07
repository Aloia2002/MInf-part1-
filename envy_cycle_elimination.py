import copy
import numpy as np
import random
import envy_free_check as ef
from itertools import chain
import time

# Outputs envy_agents: a dictionary where the key is the jealous agent and the value is the agent that is envied
def find_agents_with_envy(agents, valuations, allocations):
    not_envied_agents = copy.deepcopy(agents)
    envy_agents={} 
    for agent in agents:
        for agent2 in agents:
            if agent != agent2:
                # Checks if any agent envies agent2
                if ef.valuation_allocation(agent, valuations, allocations[agent]) < ef.valuation_allocation(agent, valuations, allocations[agent2]):
                    # Update the lists knowing that agent envies agent2
                    if agent2 in not_envied_agents:
                        not_envied_agents.remove(agent2)
                    if agent in envy_agents:
                        envy_agents[agent].append(agent2)
                    else:
                        envy_agents[agent] = []
                        envy_agents[agent].append(agent2)
    return envy_agents, not_envied_agents


def check_cycle_util(node, visited, in_stack, agents, path):
    keys = list(agents.keys())
    index = keys.index(node)
    if in_stack[index]:
        cycle_start_index = path.index(node)
        return path[cycle_start_index:]  # Return the cycle starting from the current node
    if visited[index]:
        return False
    
    visited[index] = True
    in_stack[index] = True
    path.append(node)  # Add the current node to the path

    if node in agents:
        for vertex in agents[node]:
            if vertex in agents:
                result = check_cycle_util(vertex, visited, in_stack, agents, path)
                if result:  # A cycle was found
                    return result

    path.pop()  # Remove the current node from the path as we backtrack
    in_stack[index] = False
    return False

def check_cycle(agents):
    visited = [False] * len(agents)
    in_stack = [False] * len(agents)
    keys = list(agents.keys())
    for i in range(len(agents)):
        if not visited[i]:
            path = []  # Initialize an empty path for each new DFS
            nodes_cycle = check_cycle_util(keys[i], visited, in_stack, agents, path)
            if nodes_cycle:  # If a cycle is found, return it along with True
                return True, nodes_cycle
    return False, None  # Return False and None if no cycle is found


def solve_cycle(nodes_of_cycle, envy_agents, allocations):
    new_allocations = copy.deepcopy(allocations)
    
    # Special case for a two-agent cycle
    if len(nodes_of_cycle) == 2:
        agent1, agent2 = nodes_of_cycle
        new_allocations[agent1], new_allocations[agent2] = allocations[agent2], allocations[agent1]
    else:
        # Rotate the bundles of the agents in the cycle for cycles larger than two
        for i in range(len(nodes_of_cycle)):
            giver_index = (i + 1) % len(nodes_of_cycle)  # Use modular arithmetic to loop back to the start
            giver = nodes_of_cycle[giver_index]
            receiver = nodes_of_cycle[i]
            new_allocations[receiver] = allocations[giver][:]  # Use slicing to avoid reference copying
    
    return new_allocations

def check_unique_values(my_dict):
    # Step 1: Collect all values from the dictionary
    flat_values = [item for sublist in my_dict.values() for item in sublist]
    
    # Convert the flattened list of values into a set to remove duplicates
    unique_values = set(flat_values)
    
    # Compare the length of the set with the length of the flattened list of values
    return len(flat_values) == len(unique_values)


def envy_cycle_elimination(agents, items, valuations):
    start_time = time.time()
    items_copy = copy.deepcopy(items)
    allocations = {}
    updated_valuations = copy.deepcopy(valuations)
    #  Initialise allocations
    for agent in agents:
        allocations[agent] = []
    # All items need to be allocated
    while (items_copy != []):
        envy_agents, not_envied_agents = find_agents_with_envy(agents, valuations, allocations)
        # If there are no envy agents, we search for cycles
        if (not_envied_agents == []):
            cycle, nodes_of_cycle = check_cycle(envy_agents)
            if (cycle == True):
                allocations = solve_cycle(nodes_of_cycle,envy_agents, allocations)
        else:
            #  Choosing agent
            print(not_envied_agents)
            i = random.choice(not_envied_agents)
            values = list(updated_valuations[i].values())
            # Choosing item to asign to agent
            g = np.argmax(values)
            allocations[i].append(items_copy[g])
            # Updating the items and valuations so the just assigned item is not considered
            for agent in agents:
                updated_valuations[agent].pop(items_copy[g])
            items_copy.remove(items_copy[g])

    envy_agents, not_envied_agents = find_agents_with_envy(agents, valuations, allocations)
    cycle, nodes_of_cycle = check_cycle(envy_agents)
    if(cycle == True):
        allocations = solve_cycle(nodes_of_cycle,envy_agents, allocations)
    end_time = time.time()  # Record the end time
    runtime = end_time - start_time  # Calculate the runtime
    
    if check_unique_values(allocations) == False:
        print("chosen random agent: ", i)
    return (allocations), runtime


def envy_cycle_elimination_heuristic(agents, items, valuations):
    start_time = time.time()
    items_copy = copy.deepcopy(items)
    allocations = {}
    updated_valuations = copy.deepcopy(valuations)
    #  Initialise allocations
    for agent in agents:
        allocations[agent] = []
    # All items need to be allocated
    while (items_copy != []):
        envy_agents, not_envied_agents = find_agents_with_envy(agents, valuations, allocations)
        # If there are no envy agents, we search for cycles
        if (not_envied_agents == []):
            cycle, nodes_of_cycle = check_cycle(envy_agents)
            if (cycle == True):
                allocations = solve_cycle(nodes_of_cycle,envy_agents, allocations)

        else:
            #  Choosing agent
            i = random.choice(not_envied_agents)
            values = list(updated_valuations[i].values())
            # Choosing item to asign to agent
            g = np.argmax(values)
            allocations[i].append(items_copy[g])
            # Updating the items and valuations so the just assigned item is not considered
            for agent in agents:
                updated_valuations[agent].pop(items_copy[g])
            items_copy.remove(items_copy[g])

    envy_agents, not_envied_agents = find_agents_with_envy(agents, valuations, allocations)
    cycle, nodes_of_cycle = check_cycle(envy_agents)
    if(cycle == True):
        allocations = solve_cycle(nodes_of_cycle,envy_agents, allocations)
    end_time = time.time()  # Record the end time
    runtime = end_time - start_time  # Calculate the runtime
    
    if check_unique_values(allocations) == False:
        print("chosen random agent: ", i)
    return (allocations), runtime

def envy_cycle_elimination_half_EFX(agents, items, valuations):
    allocations = {}
    updated_valuations = copy.deepcopy(valuations)
    #  Initialise allocations
    for agent in agents:
        allocations[agent] = []
    # All items need to be allocated
    while (items != []):
        envy_agents, not_envied_agents = find_agents_with_envy(agents, valuations, allocations)
        # If there are no envy agents, we search for cycles
        if (not_envied_agents == []):
            cycle, nodes_of_cycle = check_cycle(envy_agents)
            if (cycle == True):
                allocations = solve_cycle(nodes_of_cycle,envy_agents, allocations)
        else:
            #  Choosing agent
            i = None
            for agent in not_envied_agents:
                if (allocations[agent] == []):
                    i = agent
                    break
            if (i == None):
                    i = random.choice(not_envied_agents)
            values = list(updated_valuations[i].values())
            # Choosing item to asign to agent
            g = np.argmax(values)
            allocations[i].append(items[g])
            # Updating the items and valuations so the just assigned item is not considered
            for agent in agents:
                updated_valuations[agent].pop(items[g])
            items.remove(items[g])
    return (allocations)

def is_list_of_lists(variable):
    if isinstance(variable, list):
        # Check if any element in the list is also a list
        return any(isinstance(item, list) for item in variable)
    return False

def envy_cycle_elimination_partial_allocation (agents, available_items, items, valuations, partial_allocations):
    updated_valuations = copy.deepcopy(valuations)
    for item in items:
        if item not in available_items:
            for agent in agents:
                updated_valuations[agent].pop(item)
  
    # All items need to be allocated
    while (available_items != []):
        envy_agents, not_envied_agents = find_agents_with_envy(agents, valuations, partial_allocations)
        # If there are no envy agents, we search for cycles
        if (not_envied_agents == []):
            cycle, nodes_of_cycle = check_cycle(envy_agents)
            if (cycle == True):
                partial_allocations = solve_cycle(nodes_of_cycle,envy_agents, partial_allocations)
        else:
            #  Choosing agent
            i = random.choice(not_envied_agents)
            values = list(updated_valuations[i].values())
            g = np.argmax(values)
            partial_allocations[i].append(available_items[g])
            # Updating the items and valuations so the just assigned item is not considered
            for agent in agents:
                updated_valuations[agent].pop(available_items[g])
            available_items.remove(available_items[g])

    envy_agents, not_envied_agents = find_agents_with_envy(agents, valuations, partial_allocations)
    cycle, nodes_of_cycle = check_cycle(envy_agents)
    if(cycle == True):
        partial_allocations = solve_cycle(nodes_of_cycle,envy_agents, partial_allocations)

    return partial_allocations


def envy_cycle_elimination_heuristic(agents, items, valuations, indeces):
    counter = 0
    allocations = {}
    updated_valuations = copy.deepcopy(valuations)
    #  Initialise allocations
    for agent in agents:
        allocations[agent] = []
    # All items need to be allocated
    while (items != []):
        envy_agents, not_envied_agents = find_agents_with_envy(agents, valuations, allocations)
        # If there are no envy agents, we search for cycles
        if (not_envied_agents == []):
            cycle, nodes_of_cycle = check_cycle(envy_agents)
            if (cycle == True):
                allocations = solve_cycle(nodes_of_cycle,envy_agents, allocations)
        else:

            if counter < len(indeces):
                i = agents[indeces[counter]]
                counter += 1
            else:
            #  Choosing agent
                i = None
                for agent in not_envied_agents:
                    if (allocations[agent] == []):
                        i = agent
                        break
                if (i == None):
                        i = random.choice(not_envied_agents)
            values = list(updated_valuations[i].values())
            # Choosing item to asign to agent
            g = np.argmax(values)
            allocations[i].append(items[g])
            # Updating the items and valuations so the just assigned item is not considered
            for agent in agents:
                updated_valuations[agent].pop(items[g])
            items.remove(items[g])
    return (allocations)




                
    


