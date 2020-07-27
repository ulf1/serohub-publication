#!/usr/bin/env python
from datetime import datetime as dt
import os
import json
import serohub_publication.biorxiv as sp_biorxiv
import serohub_publication.crossref as sp_crossref
import argparse

# NOTES
# see https://github.com/ulf1/serohub-publication/issues/30

if __name__ == "__main__":
    # process input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--DATASETPATH", type=str, default="data/set1",
        help="path to the dataset.")
    parser.add_argument(
        "-r", "--RAWDATAPATH", type=str, default="data/raw",
        help="directory where single articles/docs are stored as JSON files.")
    parser.add_argument(
        "-o", "--OUTPUTPATH", type=str, default="data/tmp/export-set1",
        help="directory where to dump markdown files with front matter.")
    args = parser.parse_args()

    # create dataset folder if necessary
    os.makedirs(os.path.join(args.OUTPUTPATH, "biorxiv"), exist_ok=True)
    os.makedirs(os.path.join(args.OUTPUTPATH, "crossref"), exist_ok=True)

    # read all 1-label DOIs
    with open(os.path.join(args.DATASETPATH, "1.txt"), "r") as fptr:
        doi = fptr.readlines()
        files = [s.strip().replace("/", "-") + ".json" for s in doi]

    cnt = 0
    for FILENAME in files:
        # open json from training set
        dataset_filepath = os.path.join(args.DATASETPATH, "1", FILENAME)
        if os.path.isfile(dataset_filepath):
            # find the raw data source, e.g. "biorxiv"
            with open(dataset_filepath, "r") as fptr:
                data = json.load(fptr)
                RAWSRC = data["source"]

                # process depending on the raw data source
                frontmatter_content = None
                if RAWSRC in ("biorxiv", "crossref"):
                    doc_filepath = os.path.join(
                        args.RAWDATAPATH, RAWSRC, FILENAME)
                    with open(doc_filepath, "r") as fptr2:
                        doc = json.load(fptr2)
                # generate and save front matter
                if RAWSRC == "biorxiv":
                    frontmatter_content = sp_biorxiv.to_front_matter(doc)
                elif RAWSRC == "crossref":
                    frontmatter_content = sp_crossref.to_front_matter(doc)
                else:
                    print(f"[INFO] {dt.now()}: Cannot find '{RAWSRC}' source")

                if frontmatter_content:
                    frontmatter_filepath = os.path.join(
                        args.OUTPUTPATH, RAWSRC,
                        os.path.splitext(FILENAME)[0] + ".md")
                    with open(frontmatter_filepath, "w") as fptr3:
                        fptr3.write(frontmatter_content)
                        cnt += 1

            
    print(f"[INFO] {dt.now()}: '{cnt}' md files with front matter generated.")
