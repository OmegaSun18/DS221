#!/bin/bash

# Function to run the main executable and log the output, time, and memory usage
run_and_log() {
    local exp=$1
    local subexp=$2
    local customer=$3
    local pur=$4
    local log_file="${exp}/subexp${subexp}/${customer}pur${pur}.log"

    /usr/bin/time -v ./main ${exp}/subexp${subexp}/${customer}pur${pur}product.csv \
        ${exp}/subexp${subexp}/${customer}pur${pur}customer.csv \
        tests_Q2/input_price.csv tests_Q2/input_groups.csv \
        ${exp}/subexp${subexp}/${customer}pur${pur}output.csv \
        tests_Q2/output_price.csv tests_Q2/output_groups.csv \
        tests_Q2/new_hashtags.csv &> ${log_file}
}

# exp1 has a different procedure
for i in {1..4}; do
    for j in 8 32 128 512 2048; do
        ./main exp1/subexp$i/pur${j}product.csv exp1/subexp$i/pur${j}customer.csv tests_Q2/input_price.csv tests_Q2/input_groups.csv exp1/subexp$i/pur${j}output.csv tests_Q2/output_price.csv tests_Q2/output_groups.csv tests_Q2/new_hashtags.csv > exp1/subexp$i/pur$j.log
    done
done

# exp2 with 4 subexperiments
for i in {1..4}; do
    for j in 8 32 128 512 2048; do
        run_and_log "exp2" $i "customer4" $j
        run_and_log "exp2" $i "customer8" $j
        if [ $j -ne 8 ]; then
            run_and_log "exp2" $i "customer16" $j
            run_and_log "exp2" $i "customer32" $j
            if [ $j -ne 32 ]; then
                run_and_log "exp2" $i "customer64" $j
            fi
        fi
    done
done

# exp3, exp4, and exp5 without subexperiments
# exp2 with 4 subexperiments
for i in {1..4}; do
    for j in 8 32 128 512 2048; do
        run_and_log "exp2" $i "customer4" $j
        run_and_log "exp2" $i "customer8" $j
        if [ $j -ne 8 ]; then
            run_and_log "exp2" $i "customer16" $j
            run_and_log "exp2" $i "customer32" $j
            if [ $j -ne 32 ]; then
                run_and_log "exp2" $i "customer64" $j
            fi
        fi
    done
done

# exp3, exp4, and exp5 without subexperiments
# exp3, exp4, and exp5 with 3 subexperiments
for exp in exp3 exp4 exp5; do
    for i in {1..3}; do
        for j in 8 32 128 512 2048; do
            run_and_log $exp $i "customer4" $j
            run_and_log $exp $i "customer8" $j
            if [ $j -ne 8 ]; then
                run_and_log $exp $i "customer16" $j
                run_and_log $exp $i "customer32" $j
                if [ $j -ne 32 ]; then
                    run_and_log $exp $i "customer64" $j
                fi
            fi
        done
    done
done