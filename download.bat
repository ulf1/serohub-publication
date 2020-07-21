
:: BioRXiv
dvc unprotect data/raw/biorxiv.json
biorxiv-download.py
dvc add data/raw/biorxiv.json



:: update all changes (github)
git add *.dvc
git commit -m"automatic raw data update"
:: update remote data (dvc)
dvc push
