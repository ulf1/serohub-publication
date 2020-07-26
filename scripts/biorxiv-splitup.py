#!/usr/bin/env python
from datetime import datetime as dt
import json
import os
import re
import argparse


if __name__ == "__main__":
    # process input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--inputfile", type=str, default="data/raw/tmp/biorxiv.json",
        help="full path to the downloaded biorxiv file.")
    parser.add_argument(
        "-o", "--outputpath", type=str, default="data/raw/biorxiv",
        help="directory where single articles/docs are stored as JSON files.")
    args = parser.parse_args()

    # load JSON file als dict
    with open(args.inputfile, "r") as fptr:
        data = json.load(fptr)
    print(f"[INFO] {dt.now()}: Raw file read '{args.inputfile}'.")

    # save each doc/article/doi
    os.makedirs(args.outputpath, exist_ok=True)
    cnt_new = 0
    for doc in data['rels']:
        DOCFILE = re.sub(r"/", "-", doc['rel_doi']) + ".json"
        DOCFILE = os.path.join(args.outputpath, DOCFILE)
        if not os.path.isfile(DOCFILE):
            with open(DOCFILE, "w") as fptr:
                json.dump(doc, fptr)
                cnt_new += 1

    print((f"[INFO] {dt.now()}: {cnt_new} new biorxiv papers added "
           f"to '{args.outputpath}'."))
