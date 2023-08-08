#!/bin/bash --login

# entire script fails if a single command fails
set -e

# create the conda environment
mamba env create --file "$PROJECT_DIR"/environment.yml --force
