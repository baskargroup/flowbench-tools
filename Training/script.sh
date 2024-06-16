#!/bin/bash
#SBATCH --time=15:00:00   # walltime limit (HH:MM:SS)
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=8       # number of cores
#SBATCH --mem=200G   # maximum memory per node
#SBATCH --gres=gpu:a100:1
#SBATCH --job-name="bubble_MPS4to1CNO"
#SBATCH --mail-user=au2216@nyu.edu   # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --output="neurips2024-fno.out" # job standard output file (%j replaced by job id)
#SBATCH --error="neurips2024-fno.err" # job standard error file (%j replaced by job id)

source /work/mech-ai/abhisek/projects/flowbench/bin/activate
python -m codes.train
