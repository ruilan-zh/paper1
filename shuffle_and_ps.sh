#!/bin/sh

seed_i=20
seed_f=30
nohup python3 shuffle_sfrs/run_shuffle.py $seed_i $seed_f > ./tmp/out_shuffle_${today}_${seed_i}_${seed_f}.log 2> ./tmp/err_shuffle_${today}_${seed_i}_${seed_f}.log & 
BACK_PID=$!
wait $BACK_PID
sbatch job_array.sh
