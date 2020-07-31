#!/bin/bash


# create a branch of serohub.git
BRANCHNAME="publication-update-$(date +%F)"
SEROHUBPATH="/tmp/serohub-$(date +%s)"

rm -rf ${SEROHUBPATH}
git clone git@github.com:hzi-braunschweig/serohub.git ${SEROHUBPATH}
git -C ${SEROHUBPATH} checkout -b ${BRANCHNAME}


# predict unlabelled data
python model/predict.py


# sync files in the "predicted" folder
DATASETPATH="data/set1"
# delete target folder
rm "${DATASETPATH}/predicted/unlabelled"
# copy unlabelled folder
cp "${DATASETPATH}/unlabelled" "${DATASETPATH}/predicted/unlabelled"
# sync files
set1-sync.py -d "${DATASETPATH}/predicted"


# Generate markdown files 
set1-export.py \
  -d "${DATASETPATH}/predicted" \
  -o "${SEROHUBPATH}/content/publication"


# push new branch to serohub.git (create PR in serohub.git in the UI)
git -C ${SEROHUBPATH} add content/publication
git -C ${SEROHUBPATH} commit -m "serohub publication update $(date +%F)"
git -C ${SEROHUBPATH} push origin ${BRANCHNAME}
