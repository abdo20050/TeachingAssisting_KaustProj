#!/bin/sh
rm ./slurm*
sbatch ./jupy_run/jupyter_notebook.slurm
cat slurm*
