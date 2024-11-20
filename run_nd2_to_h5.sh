#!/bin/bash
#SBATCH --job-name=nd2_to_h5
#SBATCH --output=nd2_to_h5_%j.out
#SBATCH --error=nd2_to_h5_%j.err
#SBATCH --time=1:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8
#SBATCH -n 1

# file paths --- CHANGE AS NEEDED 
INPUT_PATH="/om2/user/kirjner/WormWork/adult_1070.nd2"
OUTPUT_DIR="/nese/mit/group/boydenlab/Konstantinos/h5_files"
OUTPUT_FNAME="adult_1070_07102024_2" #WITHOUT EXTENSION (i.e. no .h5)

# cropping + aligning
Y_MIN=200
Y_MAX=750

X_MIN=300
X_MAX=850

START_IDX=20 # starting frame number
FPV=40 # frames per volume

# DoG filtering 
SIG1=0.5
SIG2=4

# number of neurons (for targettrack)
N_NEURONS=20

# Run the Python script
python nd2_to_h5.py \
    "$INPUT_PATH" \
    "$OUTPUT_DIR" \
    "$OUTPUT_FNAME" \
    --y_min "$Y_MIN" \
    --y_max "$Y_MAX" \
    --x_min "$X_MIN" \
    --x_max "$X_MAX" \
    --start_idx "$START_IDX" \
    --fpv "$FPV" \
    --sig1 "$SIG1" \
    --sig2 "$SIG2" \
    --n_neurons "$N_NEURONS"