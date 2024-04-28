#!/bin/bash

# Stop on error 
set -e

# Navigate to the proper directory
cd /teamspace/studios/this_studio/algorithmic-quartet-mlops/

# Get the newest code
git pull

# Test the pipeline on the CPU
python training/pipeline.py

# Switch to a GPU 

# Run the pipeline on a GPU

