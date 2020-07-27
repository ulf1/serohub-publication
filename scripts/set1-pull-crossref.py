#!/usr/bin/env python
from datetime import datetime as dt
import glob
import os
import json
from serohub_publication.utils import unicode_to_ascii, remove_html_tags
import argparse

# NOTES
# - extract from 'data/raw/crossref/*.json' the fields required for
#    training and inference.
# - the output are JSON files with the fields 
#     {"doi": .., "source": "crossref", "text": ..}
#     and we will use the title and abstract as text
# - The new JSON files are stored in 'data/set1/unlabelled'
# - DOIs that already exist in 'data/set1/*/' are ignored

if __name__ == "__main__":
    # process input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--DATASETPATH", type=str, default="data/set1",
        help="path to the dataset.")
    parser.add_argument(
        "-r", "--RAWFILEPATH", type=str, default="data/raw/crossref",
        help="directory where single articles/docs are stored as JSON files.")
    args = parser.parse_args()

    # create dataset folder if necessary
    os.makedirs(os.path.join(args.DATASETPATH, "unlabelled"), exist_ok=True)

    # find all documents that exist in the dataset path    
    set_filepaths = glob.glob(args.DATASETPATH + "/*/*.json")
    set_filenames = [os.path.basename(s) for s in set_filepaths]

    # find all documents that exist in the raw file path
    raw_filepaths = glob.glob(args.RAWFILEPATH + "/*.json")
    raw_filenames = [os.path.basename(s) for s in raw_filepaths]

    cnt = 0
    for i, FILENAME in enumerate(raw_filenames):
        # check if raw file is new to set1
        if not (FILENAME in set_filenames):
            # read the raw document/article
            with open(raw_filepaths[i], "r") as fptr:
                doc = json.load(fptr)
                # create new json
                doc2 = {
                    "source": "crossref",
                    "doi": doc['DOI'],
                    "text": remove_html_tags(unicode_to_ascii(
                        f"{doc['title'][0]}. {doc['abstract']}"))}
                # store new file to unlabelled
                FILEPATH = os.path.join(args.DATASETPATH, 
                                        "unlabelled", FILENAME)
                with open(FILEPATH, "w") as fptr2:
                    json.dump(doc2, fptr2)
                    cnt += 1
    
    print(f"[INFO] {dt.now()}: '{cnt}' files moved.")
