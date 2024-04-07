import csv
import matplotlib.pyplot as plt
import numpy as np
import envy_free_check as efc
import ast
import round_robin as rr
import envy_cycle_elimination as ece


items = [20, 100, 500, 1000]

# Round-robin Runtimes
# round_robin_runtimes = [7.97e-05, 0.00059, 0.00831, 0.0276]
# [3.45e-05, 7.05e-05, 0.000556, 0.0078, 0.0281]
# [1.0347, 1.0177, 1.0045, 1.0009, 1.0005]
# [1.0788, 1.0196, 1.0046, 1.0024]

# ECE Runtimes
# ece_runtimes = [0.00113, 0.00804, 0.141, 0.532]
# [9.41e-05, 0.000191, 0.00138, 0.0226, 0.085]
# [1.0485, 1.0276, 1.0089, 1.0019, 1.0009]
# [1.0874, 1.0272, 1.0078, 1.0043]

# Min POF Runtimes
# min_pof_runtimes = [0.000806, 0.00878, 0.15, 0.566]
# [0.000221, 0.00151, 0.162, 62.04, 162.87]
# [1.0259, 1.0158, 1.0180, 1.0164, 1.0160]
# [1.0936, 1.0394, 1.0106, 1.0056]

# round_robin_percentages_ef = [98.0, 100, 100, 100, 100]
# ece_percentages_ef = [87.6, 96.1, 100, 100, 100]
# min_por_percentages_ef = [41.9, 43.3, 35.6, 32.3, 32.1]

# round_robin_percentages_ef = [99.5, 100, 100, 100, 100]
# ece_percentages_ef = [95.5, 98.0, 100, 100, 100]
# min_por_percentages_ef = [53.3, 48.5, 36.3, 32.3, 32.3]

round_robin_percentages_ef_10ag = [6.3, 100, 100, 100]
ece_percentages_ef_10ag = [0.8, 53.8, 99.5, 100.0]
min_por_percentages_ef_10ag = [0.4, 51.4, 99.9, 100.0]

# round_robin_percentages_efx_10ag = [94.8, 100, 100, 100]
# ece_percentages_efx_10ag = [43.2, 64.5, 99.5, 100.0]
# min_por_percentages_efx_10ag = [41.1, 60.4, 99.9, 100.0]

# Plotting
plt.figure(figsize=(10, 6))

dark_red = (0.8, 0, 0)
plt.plot(items, round_robin_percentages_ef_10ag, marker='o', color = 'blue', label='Round-robin')
plt.plot(items, ece_percentages_ef_10ag, marker='o', color = 'green',label='ECE')
plt.plot(items, min_por_percentages_ef_10ag, marker='o', color=dark_red,label='Min-POF')

plt.xlabel('Number of Items', fontsize=14)
plt.ylabel('% of EF allocations', fontsize=14)
plt.xscale('log')  # Log scale for better visualization of large values
# plt.yscale('log')  # Log scale for better visualization of small values
plt.xticks(items, items)
plt.tick_params(axis='both', which='major', labelsize=12)
plt.tick_params(axis='both', which='minor', labelsize=12)
plt.grid(True, which="major", ls="--", linewidth=0.5, alpha=0.5)

plt.legend(fontsize=16)
plt.tight_layout()
plt.show()




alpha_values_rr =[0.97, 0.5, 0.43, 0.7, 0.75, 0.85, 0.92, 0.04, 0.92, 0.92, 0.78, 0.47, 0.59, 0.97, 0.93, 0.5, 0.75, 0.41, 0.01, 0.82, 0.42, 0.68, 0.3, 0.98, 0.37, 0.89, 0.61, 0.42, 0.61, 0.41, 0.99, 0.41, 0.1, 0.06, 0.08, 0.22, 0.83, 0.92, 0.81, 0.97, 0.82, 0.26, 0.99, 0.24, 0.81, 0.82, 0.33, 0.43, 0.93, 0.59, 0.36, 0.59, 0.95, 0.37, 0.33, 0.64, 0.42, 0.53, 0.43, 0.48, 0.6, 0.46, 0.96, 0.33, 0.87, 0.63, 0.28, 0.99, 0.78, 0.06, 0.55, 0.55, 0.53, 0.57, 0.92, 0.75, 0.53, 0.68, 0.67, 0.68, 0.84, 0.69, 0.94, 1.0, 0.57, 0.33, 0.86, 0.99, 0.59, 0.46, 0.86, 0.83, 0.87, 0.65, 0.73, 0.73, 0.9, 0.24, 0.39, 0.41, 0.21, 0.56, 0.01, 0.9, 0.59, 0.85, 0.88, 0.89, 0.58, 0.26, 0.51, 0.98, 0.04, 0.58, 0.51, 0.97, 0.66, 0.99, 0.78, 0.73, 0.69, 0.91, 0.39, 0.94, 0.95, 0.4, 0.42, 0.93, 0.3, 0.5, 0.85, 0.99, 0.58, 0.85, 0.59, 0.95, 0.26, 0.75, 0.01, 0.46, 0.97, 0.94, 0.65, 0.56, 0.86, 0.2, 0.33, 0.18, 0.79, 0.8, 0.84, 0.42, 0.02, 0.08, 0.69, 0.2, 0.63, 0.92, 1.0, 0.81, 0.98, 0.5, 0.21, 0.44, 0.52, 0.9, 0.51, 0.71, 0.5, 0.37, 1.0, 0.9, 0.16, 0.74, 0.66, 0.96, 0.59, 0.9, 1.0, 0.89, 0.76, 0.2, 0.46, 0.67, 0.56, 0.63, 0.01, 0.6, 0.16, 0.42, 0.43, 0.41, 0.76, 0.57, 0.05, 0.93, 0.65, 0.89, 0.19, 0.77, 0.46, 0.2, 0.91, 0.4, 0.17, 0.25, 0.45, 0.48, 0.01, 0.6, 0.48, 0.02, 0.56, 0.99, 0.96, 0.5, 0.67, 0.67, 0.62, 0.93, 0.95, 0.62, 0.66, 0.96, 0.99, 0.59, 0.99, 0.13, 0.98, 1.0, 0.62, 0.12, 0.95, 0.88, 0.44, 0.68, 0.75, 0.97, 0.79, 0.01, 0.89, 0.81, 0.65, 0.65, 0.13, 0.96, 0.62, 0.76, 0.39, 0.5, 0.69, 0.46, 0.86, 0.9, 0.89, 0.99, 0.79, 0.37, 1.0, 0.99, 0.93, 0.5, 0.97, 0.89, 0.82, 0.56, 0.71, 0.46, 0.45, 1.0, 0.2, 0.69, 0.9, 0.74, 0.33, 1.0, 0.6, 0.6, 0.16, 0.6, 0.64, 0.87, 0.58, 0.12, 0.63, 0.3, 0.72, 0.79, 0.37, 0.01, 0.81, 0.43, 0.83, 0.4, 0.5, 0.09, 0.79, 0.28, 0.82, 0.99, 0.68, 0.33, 0.46, 0.21, 0.33, 0.6, 0.99, 0.49, 0.83, 0.5, 0.52, 0.18, 0.86, 0.6, 0.9, 0.05, 0.62, 0.83, 0.43, 0.78, 0.5, 0.37, 0.63, 0.32, 0.93, 0.4, 0.89, 0.9, 0.66, 0.91, 0.97, 0.4, 0.29, 0.99, 0.9, 0.28, 0.98, 0.79, 0.21, 0.99, 0.82, 0.89, 0.71, 0.86, 0.99, 0.25, 0.58, 0.93, 0.6, 0.66, 0.82, 0.97, 0.25, 0.48, 0.81, 0.8, 0.87, 0.81, 0.5, 0.99, 0.64, 0.33, 0.13, 0.71, 0.01, 0.97, 0.99, 0.7, 0.76, 0.76, 0.43, 0.53, 0.57, 0.01, 0.22, 0.71, 0.8, 0.91, 0.56, 0.42, 0.07, 1.0, 0.27, 0.22, 0.37, 0.53, 0.97, 0.02, 0.12, 0.74, 0.85, 0.9, 0.62, 0.21, 0.33, 0.96, 0.97, 0.4, 0.97, 0.03, 0.83, 0.68, 0.87, 0.3, 0.99, 0.61, 0.66, 0.35, 0.99, 0.27, 0.16, 0.5, 0.7, 0.96, 0.4, 0.27, 0.02, 0.76, 0.41, 0.88, 0.25, 0.87, 0.08, 0.86, 0.74, 0.82, 0.94, 0.85, 0.92, 0.62, 0.44, 0.5, 0.76, 0.21, 0.87, 0.38, 0.52, 0.72, 0.2, 0.95, 0.99, 0.68, 0.16, 0.93, 0.59, 0.97, 0.66, 0.61, 0.03, 1.0, 0.96, 0.89, 0.58, 0.49, 0.61, 0.4, 0.45, 0.63, 0.93, 0.97, 0.1, 0.82, 0.39, 0.16, 0.41, 0.59, 0.64, 0.97, 0.4, 0.52, 0.93, 1.0, 0.88, 0.76, 0.07, 0.2, 0.39, 0.8, 0.96, 0.96, 0.92, 0.64, 0.92, 0.94, 0.71, 0.59, 0.73, 0.95, 0.8, 0.74, 0.77, 0.39, 0.73, 0.62, 0.4, 0.18, 0.55, 0.82, 0.77, 0.78, 0.87, 0.4, 0.83, 0.08, 0.79, 0.93, 0.86, 0.73, 0.99, 0.1, 0.09, 0.08, 0.82, 0.75, 0.89, 0.68, 0.6, 0.83, 0.94, 0.82, 0.78, 0.79, 0.18, 0.92, 0.67, 0.86, 0.05, 0.18, 0.53, 0.83, 0.63, 0.82, 0.54, 0.4, 0.83, 0.63, 0.63, 0.87, 0.02, 0.34, 0.22, 1.0, 0.63, 0.62, 0.73, 0.25, 0.46, 0.31, 0.91, 0.23, 0.65, 0.75, 0.99, 0.95, 0.1, 0.99, 0.76, 0.43, 0.09, 0.74, 0.93, 0.97, 0.48, 0.62, 0.92, 0.83, 0.89, 0.46, 0.66, 0.89, 0.95, 0.33, 0.71, 0.97, 0.63, 0.93, 0.63, 0.94, 0.99, 0.82, 0.2, 0.98, 0.46, 0.72, 0.73, 0.82, 0.88, 0.68, 0.53, 0.07]
alpha_values_ece = [0.9, 1.0, 0.86, 1.0, 1.0, 1.0, 0.72, 0.97, 1.0, 1.0, 0.76, 0.56, 0.94, 1.0, 0.66, 0.76, 0.69, 1.0, 1.0, 0.93, 0.88, 1.0, 0.93, 0.93, 0.82, 0.89, 0.91, 0.5, 1.0, 0.7, 0.85, 0.86, 1.0, 0.79, 0.95, 1.0, 0.8, 0.97, 0.9, 0.7, 0.86, 0.76, 1.0, 0.5, 0.72, 1.0, 0.62, 0.98, 0.95, 1.0, 0.8, 1.0, 0.76, 0.73, 0.77, 0.81, 0.77, 0.98, 1.0, 0.82, 0.5, 1.0, 1.0, 0.82, 0.7, 0.76, 0.9, 0.73, 0.87, 0.91, 0.66, 0.65, 0.5, 1.0, 0.9, 0.78, 1.0, 1.0, 0.89, 0.96, 0.92, 0.92, 0.96, 0.82, 0.99, 0.22, 1.0, 0.8, 0.97, 0.85, 0.85, 0.92, 0.75, 0.69, 0.7, 0.98, 0.89, 0.4, 0.98, 0.9, 0.54, 0.88, 0.98, 1.0, 0.98, 1.0, 0.94, 0.85, 0.83, 1.0, 0.81, 0.96, 1.0, 0.96, 0.88, 0.96, 0.88, 0.78, 0.89, 1.0, 0.98, 0.74, 0.74, 1.0, 0.82, 1.0, 0.5, 0.84, 0.89, 0.69, 0.88, 0.69, 0.68, 0.99, 1.0, 0.75, 0.87, 1.0, 0.79, 0.83, 0.92, 0.8, 0.93, 0.57, 0.55, 1.0, 0.01, 1.0, 0.81, 0.81, 1.0, 1.0, 0.99, 1.0, 0.59, 0.97, 1.0, 0.72, 0.68, 1.0, 1.0, 1.0, 0.69, 0.58, 1.0, 0.91, 0.76, 0.5, 1.0, 0.9, 0.62, 0.87, 0.78, 0.91, 0.55, 0.97, 0.71, 0.8, 0.92, 0.98, 1.0, 0.68, 0.77, 0.8, 1.0, 0.97, 0.58, 1.0, 0.81, 0.7, 1.0, 0.5, 0.57, 0.9, 0.87, 1.0, 0.73, 0.8, 0.71, 0.5, 0.99, 0.9, 0.5, 0.7, 0.91, 1.0, 1.0, 0.98, 0.98, 0.93, 0.87, 0.5, 0.35, 1.0, 1.0, 0.77, 0.59, 1.0, 0.66, 0.7, 0.84, 0.71, 0.53, 0.64, 0.99, 0.89, 1.0, 1.0, 0.84, 1.0, 0.83, 1.0, 0.17, 1.0, 0.99, 1.0, 0.67, 1.0, 1.0, 0.62, 0.7, 0.5, 1.0, 0.66, 1.0, 0.62, 0.93, 1.0, 0.43, 0.79, 0.99, 0.75, 0.2, 1.0, 0.95, 0.88, 0.84, 1.0, 0.78, 1.0, 0.97, 0.87, 0.68, 0.91, 1.0, 0.83, 0.64, 0.77, 1.0, 0.99, 0.83, 1.0, 1.0, 0.72, 1.0, 1.0, 1.0, 0.59, 1.0, 0.76, 0.71, 0.93, 0.55, 1.0, 0.75, 0.95, 0.77, 0.66, 0.87, 0.05, 1.0, 0.28, 0.99, 0.36, 0.54, 1.0, 1.0, 0.83, 0.72, 0.92, 0.79, 1.0, 0.87, 1.0, 0.89, 0.42, 0.78, 1.0, 1.0, 0.95, 0.95, 0.95, 0.85, 0.63, 0.99, 0.89, 0.69, 0.89, 0.6, 1.0, 0.86, 0.73, 0.99, 1.0, 1.0, 0.97, 0.86, 0.79, 0.95, 1.0, 1.0, 1.0, 0.87, 0.94, 1.0, 0.94, 0.69, 1.0]

alpha_counts = {}
for alpha in alpha_values_rr:
    if alpha in alpha_counts:
        alpha_counts[alpha] += 1
    else:
        alpha_counts[alpha] = 1

# print(alpha_counts)
# Sort alpha values for plotting
sorted_alphas = sorted(alpha_counts.keys())
counts = [alpha_counts[alpha] for alpha in sorted_alphas]

dark_red = (0.8, 0, 0)
# Plotting
plt.plot(sorted_alphas, counts, marker='o', linestyle='-', color=dark_red, markersize=3)
plt.xlabel('Alpha Values')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()


algorithms = ['Round-Robin', 'Envy-Cycle Elimination', 'Minimum Price of Fairness']
EF1 = [100, 100, 100]  # Replace with your actual data
EFX = [66.18, 85.30, 89.50]   # Replace with your actual data
EF = [33.42, 26.50, 28.94]    # Replace with your actual data

# Set up the figure and axes
fig, ax = plt.subplots(figsize=(10, 7))

# Set the positions and width for the bars
bar_width = 0.25
index = np.arange(len(algorithms))

dark_red = (0.8, 0, 0)
dark_blue = (0, 0, 0.5)

light_red = (1, 0.6, 0.6)
light_green = (0.6, 1, 0.6)
light_blue = (0.5, 0.5, 1)
# Plot the bars for each type of envy-freeness
bar1 = ax.bar(index, EF1, bar_width, label='EF1', color='#68D4EC', edgecolor='grey')
bar2 = ax.bar(index + bar_width, EFX, bar_width, label='EFX', color=light_green, edgecolor='grey')
bar3 = ax.bar(index + bar_width * 2, EF, bar_width, label='EF', color=light_red, edgecolor='grey')

# Set the chart's title and labels
ax.set_xlabel('Algorithm', fontsize=14)
ax.set_ylabel('% of instances', fontsize=14)
ax.set_xticks(index + bar_width)
ax.set_xticklabels(algorithms)
ax.legend()

ax.set_axisbelow(True)
ax.yaxis.grid(True)
ax.xaxis.grid(False)
# Display the graph
plt.show()


with open('spliddit_data_ece_with_allocations_results.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    alpha = 1.00
    row_number = 0
    alphas = []
    counter = 0
    new_alphas = []
    

    for row in reader:
        agents_alpha_zero =[]
        row_number += 1
        agents = list(range(int(row['Number of agents'])))
        items = list(range(1, int(row['Number of items'])+1))
        valuations = ast.literal_eval(row['Valuations'])
        contains_zero = any(0 in v.values() for v in valuations)
        allocations = ast.literal_eval(row['Allocations'])
        if (row['is EFX'] == 'False'):
            for i in np.arange(1.00, -0.01, -0.01):
                i = round(i, 2)
                if efc.check_alpha_EFX(allocations, agents, valuations, i) == True:
                    if i == 0.00:
                        value = 0.01
                        result, agents_alpha_zero = efc.check_alpha_EFX(allocations, agents, valuations, value)
                        new_allocations = ece.envy_cycle_elimination_heuristic(agents, items, valuations, agents_alpha_zero)
                        for n in np.arange(1.00, -0.01, -0.01):
                            n = round(n, 2)
                            if efc.check_alpha_EFX(new_allocations, agents, valuations, n) == True:   
                                alphas.append(n)
                                break
                    if i <= alpha and i != 0.00:
                        alphas.append(i)
                        break
    
print("alphas: ", alphas)
print("len alphas: ",len(alphas))
print("max alpha: ", min(alphas))


import sys

csv.field_size_limit(sys.maxsize)
with open('results_ef1_minpof_10ag_20it_normal_2.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    # pof = 0
    ef1 = 0
    efx = 0
    ef = 0
    n_instances = 0
    for row in reader:
        if n_instances == 1000:
            break
        if row['is EF1'] == 'True':
            ef1 += 1
        if row['is EFX'] == 'True':
            efx += 1
        if row['is EF'] == 'True':
            ef += 1
        n_instances += 1

print("n_instances: ", n_instances)            
print("ef1: ", ef1)
print("efx: ", efx)
print("ef: ", ef)

