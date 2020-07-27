#!/bin/bash

BRANCHNAME="publication-update-$(date +%F)"
SEROHUBPATH="/tmp/serohub-$(date +%s)"

# create a branch of serohub.git
rm -rf ${SEROHUBPATH}
git clone git@github.com:hzi-braunschweig/serohub.git ${SEROHUBPATH}
git -C ${SEROHUBPATH} checkout -b ${BRANCHNAME}

# export MD files with front-matter directly into serohub.git
set1-export.py -o "${SEROHUBPATH}/content/publication"

# push new branch to serohub.git (create PR in serohub.git in the UI)
git -C ${SEROHUBPATH} add content/publication
git -C ${SEROHUBPATH} commit -m "serohub publication update $(date +%F)"
git -C ${SEROHUBPATH} push origin ${BRANCHNAME}
