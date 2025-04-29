#!/bin/bash

# Run the log to Excel converter
# This script runs the log_to_excel.py script

# Change to the project root directory
cd "$(dirname "$0")/.." || exit

# Make sure the necessary directories exist
mkdir -p logs
mkdir -p data

# Run the converter
echo "Starting Log to Excel Converter..."
python scripts/log_to_excel.py 