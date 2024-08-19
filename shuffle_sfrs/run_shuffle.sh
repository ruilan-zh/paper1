#!/bin/sh

today=`date '+%Y-%m-%d'`

seed_i=0
seed_f=100
logMmin="13"
logMmax="13.5"
Nsplit=8
Nsplit2=1
nohup python3 run_shuffle.py $seed_i $seed_f $logMmin $logMmax $Nsplit $Nsplit2 > ./tmp/out_shuffle_${today}_${seed_i}_${seed_f}.log 2> ./tmp/err_shuffle_${today}_${seed_i}_${seed_f}.log & 

