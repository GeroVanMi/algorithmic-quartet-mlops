#!/bin/bash

# Stop on error 
set -e

# Navigate to the proper directory
cd /teamspace/studios/this_studio/algorithmic-quartet-mlops/

# Test the pipeline on the CPU
python training/pipeline.py

# Switch to a GPU 
python ci/switch_machine.py

# Run the pipeline on a GPU
python training/pipeline.py -t
