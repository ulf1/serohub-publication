#!/bin/bash

# create a branch of serohub.git
rm -rf ../serohub-tmp
git clone git@github.com:hzi-braunschweig/serohub.git ../serohub-tmp
git -C ../serohub-tmp checkout -b publication-update-2020-07-27

# export MD files with front-matter directly into serohub.git
set1-export.py -o ../serohub-tmp/content/publication

# push new branch to serohub.git (create PR in serohub.git in the UI)
git -C ../serohub-tmp add content/publication
git -C ../serohub-tmp commit -m "serohub publication update 2020-07-27"
git -C ../serohub-tmp push origin publication-update-2020-07-27
