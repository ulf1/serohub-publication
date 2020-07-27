#!/usr/bin/env python
from datetime import datetime as dt
import os
from habanero import Crossref
import re
import json
import argparse


# EXAMPLE
# python scripts/crossref-download.py -l 10 -f "2020-07-15" -s 15.0


if __name__ == "__main__":
    # process input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--FROM_DATE", type=str, required=True,
        help="From/start date (update date), e.g. '2020-04-01'")
    parser.add_argument(
        "-t", "--TILL_DATE", type=str, default=None,
        help="Until/end date (update date), e.g. '2020-04-05'")
    parser.add_argument(
        "-l", "--LIMIT", type=int, default=25,
        help="Max. number of papers to retrieve, max 1000.")
    parser.add_argument(
        "-s", "--MIN_SCORE", type=float, default=20.0,
        help="Minimum search score from 0.0 to 100.0")
    parser.add_argument(
        "-o", "--OUTPUTPATH", type=str, default="data/raw/crossref",
        help="directory where single articles/docs are stored as JSON files.")
    args = parser.parse_args()

    # make folders
    os.makedirs(args.OUTPUTPATH, exist_ok=True)

    # instantiate downloader object
    cr = Crossref()

    # search query
    keys1 = ['seroprevalence', 'serology', 'serological',
             'sero-epidemiological', 'antibody', 'antibodies']
    q1 = "'" + "' OR '".join(keys1) + "'"
    keys2 = ['sars-cov-2', 'covid-19']
    q2 = "'" + "' OR '".join(keys2) + "'"
    query = f"({q1}) AND ({q2})"

    # help about more filters: cr.filter_names(type="works")
    # Search with START DATE (argparse) -> Search Daily!
    filterspecs = {
        'type': 'journal-article', 'has_abstract': 'true',
        'from_pub_date': args.FROM_DATE,
        'until_pub_date': args.TILL_DATE if args.TILL_DATE else args.FROM_DATE
    }

    # fetch
    data = cr.works(query=query,
                    limit=min(1000, args.LIMIT),
                    filter=filterspecs)

    print((f"[INFO] {dt.now()}: {len(data['message']['items'])} Crossref"
           f" articles fetched from '{filterspecs['from_update_date']}' till"
           f" '{filterspecs['until_update_date']}'."))

    # Store each paper in seperate JSON file
    cnt = 0
    for doc in data['message']['items']:
        if (doc['score'] > args.MIN_SCORE) and (len(doc['abstract']) > 200):
            DOCFILE = re.sub(r"/", "-", doc['DOI']) + ".json"
            DOCFILE = os.path.join(args.OUTPUTPATH, DOCFILE)
            with open(DOCFILE, "w") as fptr:
                json.dump(doc, fptr)
            cnt += 1

    print((f"[INFO] {dt.now()}: {cnt} new crossref papers added "
           f"to '{args.OUTPUTPATH}'."))
