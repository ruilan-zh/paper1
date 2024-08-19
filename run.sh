#!/bin/sh

ncore=1

istart=0
iend=1
split_name=None

logM_name=None
logMmin="0"
logMmax="15"

object2shuffle=None
ps_type="sum"
python3 big_ps_for_loop1_log.py $ncore $istart $logM_name $split_name $object2shuffle $logMmin $logMmax $ps_type
