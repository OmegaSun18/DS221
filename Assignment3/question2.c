#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int array_size = 1000000;
    int* A = (int*)malloc(array_size * sizeof(int));

    if (rank == 0) {
        // Seed the random number generator with a combination of current time and rank
        srand(time(0) + rank + clock());
        // Generate random integers between 1 and 5000000
        for (int i = 0; i < array_size; ++i) {
            A[i] = rand() % 5000000 + 1;
        }
    }

    double start_time = MPI_Wtime(); // Start time

    // Broadcast the array from process 0 to all other processes
    MPI_Bcast(A, array_size, MPI_INT, 0, MPI_COMM_WORLD);

    int n = array_size;

    // Generate a random element to search for
    int element_to_find;
    if (rank == 0) {
        srand(time(0) + clock()); // Reseed the random number generator
        element_to_find = rand() % 5000000 + 1;
    }

    // Broadcast the element to find to all processes
    MPI_Bcast(&element_to_find, 1, MPI_INT, 0, MPI_COMM_WORLD);

    int chunk_size = (n + size - 1) / size;
    int start = rank * chunk_size;
    int end = (start + chunk_size < n) ? start + chunk_size : n;

    int found = 0;
    int local_index = -1;

    // Each process searches in its subarray
    for (int i = start; i < end; ++i) {
        if (A[i] == element_to_find) {
            found = 1;
            local_index = i;
            break;
        }
    }

    // Share the found status among all processes
    int global_found;
    MPI_Allreduce(&found, &global_found, 1, MPI_INT, MPI_LOR, MPI_COMM_WORLD);

    // If any process found the element, update the global index
    int global_index = -1;
    if (global_found) {
        MPI_Reduce(&local_index, &global_index, 1, MPI_INT, MPI_MAX, 0, MPI_COMM_WORLD);
    }

    // Process 0 prints the result
    if (rank == 0) {
        printf("Element to find: %d\n", element_to_find);
        if (global_index != -1) {
            printf("Global index of element %d is: %d\n", element_to_find, global_index);
        } else {
            printf("Element %d not found in the array.\n", element_to_find);
        }
    }

    double end_time = MPI_Wtime(); // End time

    // Process 0 prints the execution time
    if (rank == 0) {
        double execution_time = end_time - start_time;
        printf("Execution time: %f seconds\n", execution_time);
    }

    free(A);
    MPI_Finalize();
    return 0;
}