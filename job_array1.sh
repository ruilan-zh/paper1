#!/bin/bash -l

#SBATCH --ntasks 28 #number of cores
#SBATCH -J shuffle_ps# job name
#SBATCH --array=0 #Run 
#SBATCH -o tmp/standard_output_file.%A.%a.out
#SBATCH -e tmp/standard_error_file.%A.%a.err
#SBATCH -p cosma7-rp
#SBATCH -A dp004 #project
#SBATCH --exclusive
#SBATCH -t 00:10:00
#SBATCH --mail-type=END,FAIL #notifications for job done & fail
#SBATCH --mail-user=zhang-ruilan@g.ecc.u-tokyo.ac.jp

module purge
#module load rockport-settings
module load gnu_comp/11.1.0
module load openmpi/4.1.1
#module load gnu_comp
#module load openmpi
#module load intel_comp/2018
#module load intel_mpi/2018
module load fftw/3.3.9cosma7
#module load fftw
module load gsl/2.5
module load armforge/22.0.2
module load python/3.6.5

#istart=6
#iend=8
#mpirun -n $SLURM_NTASKS python3 big_ps.py $SLURM_NTASKS $istart
#mpirun -n $SLURM_NTASKS python3 big_ps_2d.py $SLURM_NTASKS $istart
#mpirun -n $SLURM_NTASKS $RP_OPENMPI_ARGS python3 big_ps.py $SLURM_NTASKS  $istart

istart=${SLURM_ARRAY_TASK_ID}
iend=$((SLURM_ARRAY_TASK_ID+1))
#logM_name="logM11-13.8"
#logM_name="logM12.5-13"
logM_name=None
logMmin="0"
logMmax="15"
#split_name="dlogM1/split_nan/msat_sum_split4"
#split_name="msat_sum_split8"
#split_name="split_nan/dMdyn_split4/conc_proxy_split4"
#split_name="split_nan/msat_sum_split4"
#split_name="split_nan/conc_proxy_split4"
#split_name="split_nan/msat_sum_split8/conc_proxy_split2"
#split_name="split_nan/test_split4"
split_name=None

#object2shuffle="sat"
#object2shuffle="cent"
object2shuffle="cent"
#object2shuffle=None
ps_type="group"

dlogM=0.1


#mpirun -n $SLURM_NTASKS $RP_OPENMPI_ARGS python3 big_ps_for_loop1.py $SLURM_NTASKS  $istart
mpirun -np $SLURM_NTASKS python3 big_ps_for_loop1.py $SLURM_NTASKS $istart $logM_name $split_name $object2shuffle $logMmin $logMmax $ps_type $dlogM
#mpirun -np $SLURM_NTASKS python3 big_ps_for_loop1_7shm.py $SLURM_NTASKS $istart $logM_name $split_name $object2shuffle $logMmin $logMmax $ps_type
#mpirun -np $SLURM_NTASKS python3 log_ps.py $SLURM_NTASKS $istart $logM_name $split_name $object2shuffle $logMmin $logMmax $ps_type
