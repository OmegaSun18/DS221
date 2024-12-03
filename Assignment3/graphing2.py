import re
import matplotlib.pyplot as plt

# Initialize data structures
processes = [1, 2, 4, 8, 16, 32, 64]
execution_times = {p: [] for p in processes}

# Read the log file
with open('mpi_results.log', 'r') as file:
    lines = file.readlines()

# Parse the log file
current_processes = None
for line in lines:
    process_match = re.search(r'Running with (\d+) processes', line)
    time_match = re.search(r'Execution time: ([\d\.e-]+) seconds', line)
    
    if process_match:
        current_processes = int(process_match.group(1))
    elif time_match and current_processes is not None:
        exec_time = float(time_match.group(1))
        execution_times[current_processes].append(exec_time)

# Calculate average execution times
avg_execution_times = {p: sum(times) / len(times) for p, times in execution_times.items()}

# Calculate speedups
speedups = {p: avg_execution_times[64] / avg_execution_times[p] for p in processes}

# Plot average execution times vs number of processes
plt.figure(figsize=(10, 6))
plt.plot(processes, [avg_execution_times[p] for p in processes], marker='o')
plt.xlabel('Number of Processes')
plt.ylabel('Average Execution Time (seconds)')
plt.title('Average Execution Time vs Number of Processes')
plt.grid(True)
plt.savefig('avg_execution_time_vs_processes.png')
plt.show()

# Plot speedup vs number of processes
plt.figure(figsize=(10, 6))
plt.plot(processes, [speedups[p] for p in processes], marker='o')
plt.xlabel('Number of Processes')
plt.ylabel('Speedup')
plt.title('Speedup vs Number of Processes')
plt.grid(True)
plt.savefig('speedup_vs_processes.png')
plt.show()

# Print speedups and average execution times
print('Speedups:')
for p in processes:
    print(f'{p} processes: {speedups[p]}')
print()
print('Average Execution Times:')
for p in processes:
    print(f'{p} processes: {avg_execution_times[p]} seconds')
