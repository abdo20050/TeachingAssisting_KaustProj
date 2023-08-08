#!/bin/sh
rm ./jupy_run/slurm*
sbatch ./jupy_run/jupyter_notebook.slurm
cat slurm*
