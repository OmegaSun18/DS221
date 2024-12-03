#!/bin/bash

# Function to run the main executable and log the output, time, and memory usage
#Example file name is exp6/subexp1/hash8customer.csv, exp6/subexp1/hash8product.csv, exp6/subexp1/hash8newhashtags.csv, exp6/subexp1/hash8output.csv, exp6/subexp1/hash8output_groups.csv, exp6/subexp1/hash8output.log, etc.
run_and_log() {
    local exp=$1
    local subexp=$2
    local hash=$3
    local log_file="${exp}/subexp${subexp}/hash${hash}output.log"

    #./main ${exp}/subexp${subexp}/hash${hash}product.csv \
    #    ${exp}/subexp${subexp}/hash${hash}customer.csv \
    #    tests_Q2/input_price.csv tests_Q2/input_groups.csv \
    #    ${exp}/subexp${subexp}/hash${hash}output.csv \
    #    tests_Q2/output_price.csv ${exp}/subexp${subexp}/hash${hash} \
    #    ${exp}/subexp${subexp}/hash${hash}newhashtags.csv

    /usr/bin/time -v ./main ${exp}/subexp${subexp}/hash${hash}product.csv \
        ${exp}/subexp${subexp}/hash${hash}customer.csv \
        tests_Q2/input_price.csv tests_Q2/input_groups.csv \
        ${exp}/subexp${subexp}/hash${hash}output.csv \
        tests_Q2/output_price.csv ${exp}/subexp${subexp}/hash${hash} \
        ${exp}/subexp${subexp}/hash${hash}newhashtags.csv &> ${log_file}
}

# exp6 with 4 subexperiments
for i in {1..4}; do
    for j in 8 16 32; do
        run_and_log "exp6" $i $j
    done
done
