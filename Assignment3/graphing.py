import re
import matplotlib.pyplot as plt

# Initialize data structures
threads = []
execution_times = {10000: {}, 20000: {}, 30000: {}}

# Read the log file
with open('results1.log', 'r') as file:
    lines = file.readlines()

# Parse the log file
current_array_size = None
for line in lines:
    thread_match = re.search(r'Running with (\d+) threads and array size (\d+)', line)
    time_match = re.search(r'Execution time: ([\d\.e-]+) seconds', line)
    
    if thread_match:
        num_threads = int(thread_match.group(1))
        array_size = int(thread_match.group(2))
        current_array_size = array_size
        if num_threads not in threads:
            threads.append(num_threads)
        if num_threads not in execution_times[array_size]:
            execution_times[array_size][num_threads] = []
    elif time_match and current_array_size is not None:
        exec_time = float(time_match.group(1))
        execution_times[current_array_size][num_threads].append(exec_time)

# Calculate average execution times
avg_execution_times = {size: {num_threads: sum(times) / len(times) for num_threads, times in execution_times[size].items()} for size in execution_times}

# Calculate speedups
speedups = {size: {num_threads: avg_execution_times[size][1] / avg_execution_times[size][num_threads] for num_threads in avg_execution_times[size]} for size in avg_execution_times}

# Sort the threads for plotting
threads.sort()

# Plot the results for each array size
for array_size in [10000, 20000, 30000]:
    plt.figure(figsize=(10, 6))
    plt.plot(threads, [avg_execution_times[array_size][thread] for thread in threads], marker='o')
    plt.xlabel('Number of Threads')
    plt.ylabel('Average Execution Time (seconds)')
    plt.title(f'Average Execution Time vs Number of Threads (Array Size {array_size})')
    plt.grid(True)
    plt.savefig(f'execution_time_vs_threads_{array_size}.png')
    plt.show()

# Plot the speedups for each array size
for array_size in [10000, 20000, 30000]:
    plt.figure(figsize=(10, 6))
    plt.plot(threads, [speedups[array_size][thread] for thread in threads], marker='o')
    plt.xlabel('Number of Threads')
    plt.ylabel('Speedup')
    plt.title(f'Speedup vs Number of Threads (Array Size {array_size})')
    plt.grid(True)
    plt.savefig(f'speedup_vs_threads_{array_size}.png')
    plt.show()

#print the execution times and the speedups for each array size and number of threads
for array_size in [10000, 20000, 30000]:
    print(f'Array Size: {array_size}')
    print('Execution Times:')
    for num_threads in threads:
        print(f'{num_threads} threads: {avg_execution_times[array_size][num_threads]} seconds')
    print('Speedups:')
    for num_threads in threads:
        print(f'{num_threads} threads: {speedups[array_size][num_threads]}')
    print()
