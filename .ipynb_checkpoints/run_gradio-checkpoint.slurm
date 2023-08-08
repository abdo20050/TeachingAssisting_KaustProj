#!/bin/bash
#SBATCH --time=2:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --partition=debug
#SBATCH --job-name=run-gradio
#SBATCH --mail-type=ALL

# create the conda environment
# Load environment which has Jupyter installed. It can be one of the following:
# - Machine Learning module installed on the system (module load machine_learning)
# - your own conda environment on Ibex
# - a singularity container with python environment (conda or otherwise)  

module load machine_learning 

# get tunneling info 
export XDG_RUNTIME_DIR="" node=$(hostname -s) 
user=$(whoami) 
submit_host=${SLURM_SUBMIT_HOST} 
port=10030
echo $node pinned to port $port 

echo -e " 
To connect to the compute node ${node} on IBEX running your jupyter notebook server, you need to run following two commands in a terminal 1. 
Command to create ssh tunnel from you workstation/laptop to glogin: 

ssh -L ${port}:${node}:${port} ${user}@glogin.ibex.kaust.edu.sa 

Copy the link provided below by jupyter-server and replace the NODENAME with localhost before pasting it in your browser on your workstation/laptop " 

# Run 
conda activate myenv2 

python -m ./App/app.py

echo -e "python has ran"
