#!/bin/bash

# Directory containing run.sh
SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

python3 ${SCRIPT_DIR}/src/h1b_counting.py                                 \
    --input-file              ${SCRIPT_DIR}/input/h1b_input.csv           \
    --occupations-output-file ${SCRIPT_DIR}/output/top_10_occupations.txt \
    --states-output-file      ${SCRIPT_DIR}/output/top_10_states.txt
