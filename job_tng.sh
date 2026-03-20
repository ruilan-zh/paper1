#!/bin/bash -l

#SBATCH --ntasks 28 #number of cores
#SBATCH -J toy# job name
#SBATCH --array=0 #Run 
#SBATCH -o tmp/standard_output_file.%A.%a.out
#SBATCH -e tmp/standard_error_file.%A.%a.err
#SBATCH -p cosma7-rp
#SBATCH -A dp004 #project
#SBATCH --exclusive
#SBATCH -t 0:10:00
#SBATCH --mail-type=END,FAIL #notifications for job done & fail
#SBATCH --mail-user=zhang-ruilan@g.ecc.u-tokyo.ac.jp

set -e
module purge
nu_comp/13.1.0 openmpi/4.1.4 parallel_hdf5/1.12.0

source ~/nbodykit_venv/bin/activate

#istart=6
#iend=8
#mpirun -n $SLURM_NTASKS python3 big_ps.py $SLURM_NTASKS $istart
#mpirun -n $SLURM_NTASKS python3 big_ps_2d.py $SLURM_NTASKS $istart
#mpirun -n $SLURM_NTASKS $RP_OPENMPI_ARGS python3 big_ps.py $SLURM_NTASKS  $istart



istart=${SLURM_ARRAY_TASK_ID}
#mpirun -n $SLURM_NTASKS $RP_OPENMPI_ARGS python3 big_ps_for_loop1.py $SLURM_NTASKS  $istart
#mpirun -np $SLURM_NTASKS python3 big_ps_tng.py $SLURM_NTASKS 
#mpirun -np $SLURM_NTASKS python3 big_ps_random.py $SLURM_NTASKS 
#mpirun -np $SLURM_NTASKS $RP_OPENMPI_ARGS python3 big_ps_toy_model.py $SLURM_NTASKS 
mpirun -np $SLURM_NTASKS $RP_OPENMPI_ARGS python3 big_ps_random.py $SLURM_NTASKS 
#mpirun -np $SLURM_NTASKS python3 big_ps_filter.py $SLURM_NTASKS 
#mpirun -np $SLURM_NTASKS python3 big_ps_sat_tests.py $SLURM_NTASKS 
#mpirun -np $SLURM_NTASKS python3 big_ps_sat_redshifts.py $SLURM_NTASKS 
#mpirun -np $SLURM_NTASKS python3 big_ps_ics.py $SLURM_NTASKS 
#mpirun -np $SLURM_NTASKS python3 big_ps_gal_survey.py $SLURM_NTASKS #$istart

deactivate
