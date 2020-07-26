#!/bin/bash

# checkout new branch
OLDBRANCH="$(git rev-parse --abbrev-ref HEAD)"
BRANCHNAME="raw-file-update-$(date +%s)"
git checkout -b ${BRANCHNAME}

# BioRxiv
TMPFILE="data/raw/tmp/biorxiv.json"
RAWPATH="data/raw/biorxiv"
biorxiv-download.py -o ${TMPFILE}
biorxiv-splitup.py -i ${TMPFILE} -o ${RAWPATH}
dvc add ${RAWPATH}
git add "${RAWPATH}.dvc"

# upload files to DVC remote repo
dvc push

# commit files
git commit -m "raw files updated"
git push origin ${BRANCHNAME}
git checkout ${OLDBRANCH}
