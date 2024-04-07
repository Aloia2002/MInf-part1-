import generate_data as gen
import round_robin as rr
import price_fairness_check as pfc
import envy_free_check as efc
import envy_cycle_elimination as ece
import min_price_of_fairness as mpof
import pandas as pd
import os
import min_price_fairness_n_agents as pof_n
import csv

def read_file(file_path):
    file = pd.read_excel(file_path, header=None)

    valuations = []
    for index, row in file.iterrows():
        agent_valuations = {i+1: row[i] for i in range(len(row))}
        valuations.append(agent_valuations)
    return valuations


# 2309 files

def check_unique_values(my_dict):
    # Step 1: Collect all values from the dictionary
    flat_values = [item for sublist in my_dict.values() for item in sublist]
    
    # Convert the flattened list of values into a set to remove duplicates
    unique_values = set(flat_values)
    
    # Compare the length of the set with the length of the flattened list of values
    return len(flat_values) == len(unique_values)
    
def execute_experiment(n_iterations, file, agents, items, valuations, path, index):
    # all_valuations = []
    for i in range(n_iterations):

        # valuations = gen.generate_data(n_agents, n_items, distribution)
        # all_valuations.append(valuations)
        # allocations, runtime = rr.round_robin(agents, items, valuations)
        allocations, runtime = ece.envy_cycle_elimination(agents, items, valuations)
        # allocations, runtime = mpof.min_price_of_fairness(agents, items, valuations)
        # allocations, runtime = pof_n.ef1_high(agents, items, valuations)
        if check_unique_values(allocations) == False:
            print("allocations with repeated items: ",allocations)
            print(path)
        # gen.save_data(valuations, n_items, allocations)
        sw = pfc.social_welfare(allocations, valuations, agents)
        pf = pfc.price_of_fairness(allocations, valuations, agents, items)
        ef = efc.check_EF(allocations, agents, valuations)
        ef1 = efc.check_EF1(allocations, agents, valuations)
        if ef1 == False:
            print("allocations: ",allocations)
            print("agents: ", agents)
            print("valuations: ", valuations)
            print("items: ", items)
            print ("path: ", path)
            print("index: ", index)
            print("ef1: ", ef1)
        efx = efc.check_EFX(allocations, agents, valuations)
        gen.save_results(len(agents), len(items), sw, pf, runtime, ef, ef1, efx, valuations, allocations, file)

    return None
    
directory_path = '/Users/aloiaiglesiasroman/Desktop/4th_year/Dissertation/spliddit/'
excel_files = [f for f in os.listdir(directory_path) if f.endswith('.xlsx')]
index = 0
for file in excel_files:
    file_path = os.path.join(directory_path, file)
    valuations = read_file(file_path)
    index += 1
    # print(file_path)
    items_set = set()
    for valuation in valuations:
        items_set.update(valuation.keys())
    items = sorted(items_set)
    agents = list(range(len(valuations)))
    execute_experiment(1, 'spliddit_data_ece_with_allocations_results.csv', agents, items, valuations, file_path, index)


new_path = '/Users/aloiaiglesiasroman/Desktop/4th_year/Dissertation/spliddit/Instance_960.xlsx'
valuations = read_file(new_path)
items_set = set()
for valuation in valuations:
    items_set.update(valuation.keys())
items = sorted(items_set)
agents = list(range(len(valuations)))
allocations, runtime = pof_n.ef1_high(agents, items, valuations)
print(len(items))
print(len(agents))
print(runtime)
print(efc.check_EF1(allocations, agents, valuations))
    

n_agents = 2
n_items = 1000
items = list(range(1, n_items+1))
agents = list(range(0, n_agents))
n_iterations = 1000
with open('val_2ag_1000it_ef1_rr.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    # next(reader)  # Skip the first row (header)
    valuations_all_experiments = []  # List to store all experiments

    # Read two rows at a time to process data for each experiment
    for row1, row2 in zip(reader, reader):
        experiment = []  # List to store the valuations for this experiment

        # Create dictionaries for agent 1 and agent 2
        for row in [row1, row2]:
            if row is not None: 
                valuation_dict = {}
                for key, value in row.items():
                    if key and key != 'Agent':
                        split_key = key.split('_')
                        if len(split_key) == 2 and split_key[1].isdigit():
                            valuation_dict[int(split_key[1])] = float(value)
                experiment.append(valuation_dict)

        # Add this experiment to the list of all experiments
        valuations_all_experiments.append(experiment)

for i in range(n_iterations):
        valuations = valuations_all_experiments[i]
        # allocations, runtime = rr.round_robin(agents, items, valuations)
        # allocations, runtime = ece.envy_cycle_elimination(agents, items, valuations)
        # allocations, runtime = pof_n.ef1_high(agents, items, valuations)
        allocations, runtime = mpof.min_price_of_fairness(agents, items, valuations)
        if check_unique_values(allocations) == False:
            print("allocations with repeated items: ",allocations)
        sw = pfc.social_welfare(allocations, valuations, agents)
        pf = pfc.price_of_fairness(allocations, valuations, agents, items)
        ef = efc.check_EF(allocations, agents, valuations)
        ef1 = efc.check_EF1(allocations, agents, valuations)
        if ef1 == False:
            print("allocations: ",allocations)
            print("agents: ", agents)
            print("valuations: ", valuations)
            print("items: ", items)
            print("ef1: ", ef1)
        efx = efc.check_EFX(allocations, agents, valuations)
        gen.save_results(len(agents), len(items), sw, pf, runtime, ef, ef1, efx, valuations, allocations, 'results_ef1_minpof_2ag_1000it_normal_def.csv')
