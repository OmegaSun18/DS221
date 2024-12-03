#!/bin/bash

#SBATCH --nodes=2
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=64
#SBATCH --time=10:00:00

module load openmpi

make
mpiexec -n 32 ./question2