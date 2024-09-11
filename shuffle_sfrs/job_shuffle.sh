#!/bin/bash -l

#SBATCH --ntasks 28 #number of cores
#SBATCH -J shuffle# job name
#SBATCH -o tmp/standard_output_file.%A.%a.out
#SBATCH -e tmp/standard_error_file.%A.%a.err
#SBATCH -p cosma7
#SBATCH -A dp004 #project
#SBATCH --exclusive
#SBATCH -t 03:00:00
#SBATCH --mail-type=END,FAIL #notifications for job done & fail
#SBATCH --mail-user=zhang-ruilan@g.ecc.u-tokyo.ac.jp

module purge
module load rockport-settings
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

istart=10
iend=20
logMmin="12.5"
logMmax="13"
Nsplit=1
Nsplit2=1
#istart=${SLURM_ARRAY_TASK_ID}
#iend=$((SLURM_ARRAY_TASK_ID+1))
python3 run_shuffle.py $istart $iend $logMmin $logMmax $Nsplit $Nsplit2
#python3 run_shuffle1.py $istart $iend $logMmin $logMmax $Nsplit $Nsplit2
