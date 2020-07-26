#!/usr/bin/env python
from datetime import datetime as dt
import requests
import os
import argparse
URL = "https://connect.biorxiv.org/relate/collection_json.php?grp=181"


if __name__ == "__main__":
    # process input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--outputfile", type=str, default="data/raw/tmp/biorxiv.json",
        help="full path where to store the biorxiv JSON file.")
    parser.add_argument(
        "-u", "--url", type=str, default=URL,
        help="URL of biorxiv feed")
    args = parser.parse_args()

    # Download the whole "SARS-CoV-2" feed
    print(f"[INFO] {dt.now()}: Download started from '{args.url}'.")
    resp = requests.get(args.url)
    print(f"[INFO] {dt.now()}: Latest biorxiv SARS-Cov-2 feed downloaded.")

    # Store the response as JSON
    os.makedirs(os.path.dirname(args.outputfile), exist_ok=True)
    with open(args.outputfile, "wb") as fptr:
        fptr.write(resp.content)
    print(f"[INFO] {dt.now()}: Feed stored as '{args.outputfile}'.")
