from datetime import datetime as dt
import os
import glob
import joblib
import json

from serohub_publication.utils import  normalize_string
import re
def emb_preprocessor(s):
    s = normalize_string(s)
    return re.sub(r'[0-9]', r'', s)

# Predict unlabelled files
# move unlabelled files to DATASETPATH/predicted/{0,1,0.txt,1.txt}

# misc arguments
DATASETPATH = "data/set1"
os.makedirs(os.path.join(DATASETPATH, "predicted"), exist_ok=True)

#os.makedirs(os.path.join(DATASETPATH, "predicted", "0"), exist_ok=True)
#os.makedirs(os.path.join(DATASETPATH, "predicted", "1"), exist_ok=True)

# load unlaballed data
cnt = 0
dois = []
X = []
for FILEPATH in glob.glob(DATASETPATH + "/unlabelled/*.json"):
    if os.path.isfile(FILEPATH):
        with open(FILEPATH, 'r') as fptr:
            doc = json.load(fptr)
            X.append(doc['text'])
            dois.append(doc['doi'])
            cnt += 1

print(f"[INFO] {dt.now()}: '{cnt}' unlabelled documents will be classified.")


# find latest model
EMBPATH = sorted(glob.glob(DATASETPATH + "/models/embedding-*.joblib"), key=os.path.getmtime, reverse=True)[0]
MODELPATH = sorted(glob.glob(DATASETPATH + "/models/hardvoting-*.joblib"), key=os.path.getmtime, reverse=True)[0]

emb = joblib.load(EMBPATH)
model = joblib.load(MODELPATH)


# Apply word embedding
X_emb = emb.transform(X)

# Predict labels
labels = model.predict(X_emb.toarray())


# Write to file
f0 = open(os.path.join(DATASETPATH, "predicted/0.txt"), "w")
f1 = open(os.path.join(DATASETPATH, "predicted/1.txt"), "w")
for i, doi in enumerate(dois):
    if labels[i] == 0:
        f0.write(doi + '\n')
    elif labels[i] == 1:
        f1.write(doi + '\n')

f0.close()
f1.close()
