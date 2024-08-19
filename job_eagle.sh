#!/bin/bash -l

#SBATCH --ntasks 128 #number of cores
#SBATCH -J shuffle_ps# job name
#SBATCH --array=0 #Run 
#SBATCH -o tmp/standard_output_file.%A.%a.out
#SBATCH -e tmp/standard_error_file.%A.%a.err
#SBATCH -p cosma8
#SBATCH -A dp004 #project
#SBATCH --exclusive
#SBATCH -t 0:10:00
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
#mpirun -n $SLURM_NTASKS $RP_OPENMPI_ARGS python3 big_ps_for_loop1.py $SLURM_NTASKS  $istart
mpirun -np $SLURM_NTASKS python3 big_ps_eagle.py $SLURM_NTASKS 
