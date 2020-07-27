#!/usr/bin/env python
from datetime import datetime as dt
import glob
import os
import shutil
import argparse

# NOTES
# - There are two lists 'data/set1/{0,1}.txt' that contains labelled DOIs.
# - The output of an ML algorithm are IDs what are the DOIs in our case.
# - When we want to change the labelling manually, we only need to 
#    edit the 'data/set1/{0,1}.txt' files accordingly.
# - There is no need to move JSON files between {0,1,unlabelled} manually.
#     This script will do that for you!

if __name__ == "__main__":
    # process input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--DATASETPATH", type=str, default="data/set1",
        help="path to the dataset.")
    args = parser.parse_args()

    # create dataset folder if necessary
    os.makedirs(os.path.join(args.DATASETPATH, "unlabelled"), exist_ok=True)
    os.makedirs(os.path.join(args.DATASETPATH, "0"), exist_ok=True)
    os.makedirs(os.path.join(args.DATASETPATH, "1"), exist_ok=True)

    # find all documents that exist in the dataset path    
    set_filepaths = glob.glob(args.DATASETPATH + "/*/*.json")
    set_filenames = [os.path.basename(s) for s in set_filepaths]

    # read all 0-label DOIs
    with open(os.path.join(args.DATASETPATH, "0.txt"), "r") as fptr:
        doi0 = fptr.readlines()
        files0 = [s.strip().replace("/", "-") + ".json" for s in doi0]

    # read all 1-label DOIs
    with open(os.path.join(args.DATASETPATH, "1.txt"), "r") as fptr:
        doi1 = fptr.readlines()
        files1 = [s.strip().replace("/", "-") + ".json" for s in doi1]

    # move files to correct folder
    cnt = 0
    for i, FILENAME in enumerate(set_filenames):
        # set the new destination
        if FILENAME in files1:
            DST = os.path.join(args.DATASETPATH, "1", FILENAME)
        elif FILENAME in files0:
            DST = os.path.join(args.DATASETPATH, "0", FILENAME)
        else:
            DST = os.path.join(args.DATASETPATH, "unlabelled", FILENAME)
        # move file
        if set_filepaths[i] != DST:
            shutil.move(set_filepaths[i], DST)
            cnt += 1
    print(f"[INFO] {dt.now()}: '{cnt}' files moved.")
