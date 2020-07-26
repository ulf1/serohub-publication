# serohub-publication

## Purpose
The section of the website [serohub.netlify.app/en/publication](https://serohub.netlify.app/en/publication/) needs to be filled with relevant scientific papers for seroprevalence studies about SARS-Cov-2. 

## Solution
- [ ] get machine-readable access to public literature websites (e.g. XML feeds, R and python packages; We are using DOIs as unique IDs)
- [ ] train a binary text classifer (i.e., annotate/label a training set, find better ML algorithms and word embeddings, label more training examples and train again)
- [ ] run the text classifier's `predict` method on new unknown publications 
- [ ] create `.md` files for the website


## Installation

### Linux und MacOS

```bash
# clone the git repo
git clone git@github.com:ulf1/serohub-publication.git

# download versionened datasets (dvc)
dvc pull

# install and activate virtualenv
python3.6 -m venv .venv
source .venv/bin/activate

# install this python package
pip install -r requirements.txt
python setup.py install
```

(Remove package: `pip uninstall serohub-publication`)

### Notes for Windows
Assuming that [python 3.6](https://www.python.org/downloads/windows/) is installed in `C:\Python\Python36`:

```
C:\Python\Python36\python.exe -m venv .venv
.venv\Scripts\activate.bat
```


## DVC usage

### Setup Remote DVC storage
Please refer to [DVC Docs](https://dvc.org/doc/command-reference/remote/add#supported-storage-types) to pick remote storage option.
The DVC remote storage hosts the (bigger) data files **outside** the git repo. You can use the `dvc` commands in similar way to `git` commands to pull, and push changes regarding the dataset.

For this project, we decided to the data on [Google Drive](https://drive.google.com/drive/folders/10jiIPmfpXOs2JcNTbXng_Y3Xxg59qJyl). 
An we followed this [instruction](https://dvc.org/doc/user-guide/setup-google-drive-remote)


```bash
dvc remote add --default myremote gdrive://10jiIPmfpXOs2JcNTbXng_Y3Xxg59qJyl
git commit .dvc/config -m "My remote storage configuration for Google Drive"
dvc push
```

### Add a new Dataset folder to DVC

```bash
dvc add data/set123
git add data/set123.dvc

dvc push
git commit -m "dataset updated"
git push
```

## Scripts

### Download new raw files and update DVC
```bash
source .venv/bin/activate
bash download.sh
```

**Notes for Windows**

```
.venv\Scripts\activate.bat
download.bat
```
