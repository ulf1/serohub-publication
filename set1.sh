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

# re-train model
python model/train.py
dvc add "${DATASETPATH}/models"
git add "${DATASETPATH}/models.dvc"

# upload files to DVC remote repo
dvc push

# commit files
git commit -m "data set1 updated $(date +%F)"
git push origin ${BRANCHNAME}
git checkout ${OLDBRANCH}
