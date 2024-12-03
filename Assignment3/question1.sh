#!/bin/bash

# Define the number of threads and array sizes
threads=(1 2 4 8 16 32 64)
array_sizes=(10000 20000 30000)

# Log file to save the results
log_file="results1.log"

# Clear the log file if it exists
> $log_file

# Compile the program
g++ -fopenmp -o main main.cpp

# Iterate over the number of threads and array sizes
for num_threads in "${threads[@]}"; do
    for array_size in "${array_sizes[@]}"; do
        for run in {1..5}; do
            echo "Run $run: Running with $num_threads threads and array size $array_size" | tee -a $log_file
            ./main $num_threads $array_size | tee -a $log_file
            echo "" | tee -a $log_file
        done
    done
done