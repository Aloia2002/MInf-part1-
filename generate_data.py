import numpy as np
import csv


def generate_data(n_agents, n_items, distribution):
    valuations = []
    if distribution == 'uniform':
    # Uniform distribution (all outcomes are equally likely)
        for i in range(n_agents):
            x = np.random.uniform(0, 1, n_items)
            # x = np.random.randint(1, 11, n_items)  --> if we want to generate integers
            agent_valuations = {}
            for j in range(n_items):
                agent_valuations[j+1] = x[j]
            #valuations.append(dict(zip(items, x)))   --> this if we want the item next to the valuations
            valuations.append(agent_valuations)

    if distribution == 'beta':
    # Beta distribution (probability distribution set on the interval [0, 1]) (special case of Dirichlet distribution)
        for i in range(n_agents):
            x = np.random.beta(0.05, 0.1, n_items) # if we put a =1 and b = 1 we get a uniform distribution for (0,1)
            agent_valuations = {}
            for j in range(n_items):
                agent_valuations[j+1] = x[j]
            valuations.append(agent_valuations)
        

    if distribution == 'dirichlet':
    # Dirichlet distribution (contains values that are bounded [0,1]∈ℝ and sum to  1)
        x = np.random.dirichlet(np.ones(n_items),size=n_agents) # we draw the data differently because the values of the dirichlet distribution have to sum to 1
        for valuation in x:
            #add valuations to the list
            valuations.append(valuation)

    if distribution == 'normal':
    # Normal distribution (probability distribution that is symmetric about the mean)
        lower_bound = 0
        upper_bound = 1
        for i in range(n_agents):
            x = np.random.normal(0.5, 0.5, n_items)
            agent_valuations = {}
            for j, value in enumerate(x):
                if value < lower_bound or value > upper_bound:
                    value = 1 / (1 + np.exp(-value))# we squash the values to be between 0 and 1 with the sigmoid function because the normal distribution is defined over the whole real line
                agent_valuations[j+1] = value
            valuations.append(agent_valuations)

    return valuations


def save_data(valuations, n_items, allocations):
    file_path = '/Users/aloiaiglesiasroman/Desktop/4th_year/Dissertation/val_3ag_5it_ef1_rr_spliddit.csv'
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:  # Check if file is empty
            writer.writerow(['Agent'] + [f'Item_{i}' for i in range(1, n_items + 1)] + ['Allocation'])
        for i, agent_valuations in enumerate(valuations):
            agent_allocation = allocations[i]
            writer.writerow([f'Agent_{i+1}'] + list(agent_valuations.values()) + agent_allocation)
            


def save_results(n_agents, n_items, social_welfare, price_of_fairness, run_time, ef, ef1, efx, valuations, allocations, file):
    # file_path = '/Users/aloiaiglesiasroman/Desktop/4th_year/Dissertation/results_rr.csv'
    file_path = '/Users/aloiaiglesiasroman/Desktop/4th_year/Dissertation/' + file
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:  # Check if file is empty
            writer.writerow(['Number of agents'] + ['Number of items'] + ['Social welfare'] + ['Price of fairness'] + ['Run time'] + ['is EF'] + ['is EF1'] + ['is EFX'] + ['Valuations'] + ['Allocations'])
        writer.writerow([n_agents, n_items, social_welfare, price_of_fairness, run_time, ef, ef1, efx, valuations, allocations])




                
    


