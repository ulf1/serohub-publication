#!/bin/bash

# checkout new branch
OLDBRANCH="$(git rev-parse --abbrev-ref HEAD)"
BRANCHNAME="data-set1-update-$(date +%s)"
git checkout -b ${BRANCHNAME}

# pull files
DATASETPATH="data/set1"
set1-pull-biorxiv.py -d ${DATASETPATH} -r "data/raw/biorxiv"
set1-pull-crossref.py -d ${DATASETPATH} -r "data/raw/crossref"

# sync files
set1-sync.py -d ${DATASETPATH}
dvc add "${DATASETPATH}/0"
dvc add "${DATASETPATH}/1"
git add "${DATASETPATH}/0.dvc"
git add "${DATASETPATH}/1.dvc"

# upload files to DVC remote repo
dvc push

# commit files
git commit -m "raw files updated"
git push origin ${BRANCHNAME}
git checkout ${OLDBRANCH}
