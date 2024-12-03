#!/bin/bash

# Define the number of processes
processes=(1 2 4 8 16 32 64)

# Log file to save the results
log_file="mpi_results.log"

# Clear the log file if it exists
> $log_file

# Set the LD_LIBRARY_PATH to include the MPI library path
export LD_LIBRARY_PATH=/usr/mpi/gcc/openmpi-4.1.5rc2/lib64/:$LD_LIBRARY_PATH

# Compile the program
mpicc -o question2 question2.c

# Iterate over the number of processes
for num_procs in "${processes[@]}"; do
    for run in {1..20}; do
        echo "Run $run: Running with $num_procs processes" | tee -a $log_file
        mpiexec --oversubscribe -n $num_procs ./question2 2>&1 | tee -a $log_file
        echo "" | tee -a $log_file
    done
done