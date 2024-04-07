import price_fairness_check as pfc
import copy 
import numpy as np
import envy_free_check as ef
import random
import envy_cycle_elimination as ece
import time

def check_unique_values(my_dict):
    # Step 1: Collect all values from the dictionary
    flat_values = [item for sublist in my_dict.values() for item in sublist]
    
    # Convert the flattened list of values into a set to remove duplicates
    unique_values = set(flat_values)
    
    # Compare the length of the set with the length of the flattened list of values
    return len(flat_values) == len(unique_values)

def ef1_high(agents, items, valuations):
    start_time = time.time()
    max_welfare, allocations = pfc.max_social_welfare(valuations, agents, items)
    graph_items = []

    #re-index the goods so each Wi forms a connected graph
    for allocation in allocations.values():
        if allocation != []:
            for item in allocation:
                graph_items.append(item)

    partial_allocation = {}
    control = False
    # For each agent that received an item, we get the item that they value the most and set P(allocation) of the agent as that item
    # For each agent that did not receive any item, we set P(allocation) of that agent as the empty set
    for agent, allocation in allocations.items():
        if allocation != []:
            values = []
            for item in allocation:
                values.append(valuations[agent][item])
            g = np.argmax(values)
            partial_allocation[agent] = [allocation[g]]
            if control == False:
                graph_items = remove_item_graph(graph_items, allocation[g])
                control = True
            else:
                graph_items = remove_item_from_sublist(graph_items, allocation[g])
        else: 
            partial_allocation[agent] = []

    # while there is an agent that values more a component U of U(Pt) than their own allocation, do:   
    while envy_condition(agents, valuations, partial_allocation, graph_items) != (False, None):
        x, component_u = envy_condition(agents, valuations, partial_allocation, graph_items)
        agents_condition = get_agents_condition(agents, valuations, partial_allocation, component_u)
        chosen_agent = random.choice(agents_condition)
        for sublist in graph_items:
            if type(sublist) == int:
                if sublist == component_u[0]:
                    graph_items.remove(sublist)
            else:
                for i in range (len(component_u)):
                    if component_u[i] in sublist:
                        sublist.remove(component_u[i])
        partial_allocation[chosen_agent] = component_u
    elements_to_remove = set(item for sublist in partial_allocation.values() for item in sublist)
    available_items = [item for item in items if item not in elements_to_remove]
    if available_items == []:
        final_allocations = partial_allocation
    else:
        final_allocations = ece.envy_cycle_elimination_partial_allocation(agents, available_items, items, valuations, partial_allocation)
        
    if check_unique_values(final_allocations) == False:
        print("max welfare alloations: ", allocations)
        print("partial allocation: ", partial_allocation)
    end_time = time.time()
    runtime = end_time - start_time
    return final_allocations, runtime
    
def get_agents_condition(agents, valuations, partial_allocation, component):
    agents_condition = []
    for agent in agents:
        if partial_allocation[agent] == []:
            agents_condition.append(agent)
        else:
            if valuations[agent][partial_allocation[agent][0]] < ef.valuation_allocation(agent, valuations, component):
                agents_condition.append(agent)
    return agents_condition

def envy_condition(agents, valuations, partial_allocation, graph_items):
    for component_u in graph_items:
        for combination in connected_components(component_u):
            for agent in agents:
                if partial_allocation[agent] == []:
                    return True, combination
                elif valuations[agent][partial_allocation[agent][0]] < ef.valuation_allocation(agent, valuations, combination):
                    return True, combination
    return False, None


def connected_components (component_u):
    possible_components = []
    if type(component_u) == int:
        component_u = [component_u]
    for i in range (1, len(component_u) + 1):
        component = component_u[:i]
        possible_components.append(component)
    return possible_components

def remove_item_graph(graph, element):
    index = graph.index(element)
    if index == 0:
        graph = graph[1:]
    elif index == len(graph) - 1:
        graph = graph[:-1]
    else:
        graph = [graph[:index], graph[index+1:]]
    return graph

def remove_item_from_sublist(graph, element):
    new_graph = []  # Create a new list to hold the modified sublists
    for sublist in graph:
        if type(sublist) == int:
            new_graph = remove_item_graph(graph, element)
            return new_graph
        if element in sublist:
            index = sublist.index(element)
            # If the element is at the beginning or end of the sublist, remove it directly
            if index == 0:
                new_graph.append(sublist[1:])
            elif index == len(sublist) - 1:
                new_graph.append(sublist[:-1])
            else:
                # If the element is in the middle, split the sublist into two sublists
                new_graph.append(sublist[:index])
                new_graph.append(sublist[index+1:])
        else:
            new_graph.append(sublist)  # Add the unmodified sublist to the new graph

    # Remove any empty sublists that may have resulted from the removal
    new_graph = [sublist for sublist in new_graph if sublist]
    return new_graph

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

    




