#!/usr/bin/env python
from datetime import datetime as dt
import requests
import os

if __name__ == "__main__":
    # Download the whole "SARS-CoV-2" feed
    URL = "https://connect.biorxiv.org/relate/collection_json.php?grp=181"
    resp = requests.get(URL)
    print(f"[INFO] {dt.now()}: Latest biorxiv SARS-Cov-2 feed downloaded")

    # Store the response as JSON
    FILEPATH = "data/raw/tmp"
    FILENAME = "biorxiv.json"
    os.makedirs(FILEPATH, exist_ok=True)
    with open(os.path.join(FILEPATH, FILENAME), "wb") as fptr:
        fptr.write(resp.content)
    print(f"[INFO] {dt.now()}: Feed stored as {FILEPATH}")
