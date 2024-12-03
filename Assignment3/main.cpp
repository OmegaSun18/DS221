#include <iostream>
#include <omp.h>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <chrono>

void prefix_sum(const std::vector<int>& A, std::vector<int>& B, int num_threads) {
    int n = A.size();
    B.resize(n);

    int chunk_size = (n + num_threads - 1) / num_threads;

    // Step 1: Compute local prefix sums in parallel
    #pragma omp parallel num_threads(num_threads)
    {
        int tid = omp_get_thread_num();
        int start = tid * chunk_size;
        int end = std::min(start + chunk_size, n);

        if (start < n) {
            B[start] = A[start];
            for (int i = start + 1; i < end; ++i) {
                B[i] = B[i - 1] + A[i];
            }
        }
    }

    // Step 2: Compute the offsets for each chunk
    std::vector<int> offsets(num_threads, 0);
    for (int i = 1; i < num_threads; ++i) {
        offsets[i] = offsets[i - 1] + B[i * chunk_size - 1];
    }

    // Step 3: Add the offsets to each chunk in parallel
    #pragma omp parallel num_threads(num_threads)
    {
        int tid = omp_get_thread_num();
        int start = tid * chunk_size;
        int end = std::min(start + chunk_size, n);

        if (tid > 0 && start < n) {
            for (int i = start; i < end; ++i) {
                B[i] += offsets[tid];
            }
        }
    }
}

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <num_threads> <array_size>" << std::endl;
        return 1;
    }

    int num_threads = std::atoi(argv[1]);
    int n = std::atoi(argv[2]);

    std::srand(std::time(0)); // Seed for random number generation
    std::vector<int> A(n);
    for (int i = 0; i < n; ++i) {
        A[i] = std::rand() % 10001; // Random integers between 0 and 10000
    }

    std::vector<int> B;

    auto start_time = std::chrono::high_resolution_clock::now(); // Start time

    prefix_sum(A, B, num_threads);

    auto end_time = std::chrono::high_resolution_clock::now(); // End time

    // Print the first 10 elements of the result for verification
    //for (int i = 0; i < 10; ++i) {
    //    std::cout << B[i] << " ";
    //}
    //std::cout << std::endl;
    //Print the array size
    //std::cout << "Array size: " << n << std::endl;
    // Print the number of threads
    //std::cout << "Number of threads: " << num_threads << std::endl;

    // Print the execution time
    std::chrono::duration<double> execution_time = end_time - start_time;
    std::cout << "Execution time: " << execution_time.count() << " seconds" << std::endl;

    return 0;
}