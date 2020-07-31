from datetime import datetime as dt

# PREPARE
import os
import json
from serohub_publication.utils import  normalize_string
import re
from sklearn.model_selection import train_test_split

# FEATURIZATION
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# TRAINING
from sklearn.naive_bayes import GaussianNB  # 95/50
from sklearn.svm import SVC  # 95/68
from sklearn.ensemble import RandomForestClassifier  # 90/79
from sklearn.neural_network import MLPClassifier  # 92/54
#from sklearn.neighbors import KNeighborsClassifier  # useless
from sklearn.linear_model import PassiveAggressiveClassifier  # 92/86
from sklearn.ensemble import VotingClassifier
import joblib 

# EVALUATION
from sklearn.metrics import confusion_matrix, balanced_accuracy_score, classification_report



# misc arguments
DATASETPATH = "data/set1"

MODELPATH = os.path.join(DATASETPATH, "models")
os.makedirs(MODELPATH, exist_ok=True)

CURRENT_TIME = dt.timestamp(dt.now())


# PREPARE

# read all 0-label DOIs
with open(os.path.join(DATASETPATH, "0.txt"), "r") as fptr:
    doi0 = fptr.readlines()
    files0 = [s.strip().replace("/", "-") + ".json" for s in doi0]

# read all 1-label DOIs
with open(os.path.join(DATASETPATH, "1.txt"), "r") as fptr:
    doi1 = fptr.readlines()
    files1 = [s.strip().replace("/", "-") + ".json" for s in doi1]

# read all JSON files
y = []
X = []
for label in (0, 1):
    cnt = 0
    for FILENAME in vars()[f"files{label}"]:
        FILEPATH = os.path.join(DATASETPATH, str(label), FILENAME)
        if os.path.isfile(FILEPATH):
            with open(FILEPATH, 'r') as fptr:
                doc = json.load(fptr)
                #s = normalize_string(doc['text'])
                #s = re.sub(r'[0-9]', r'', s)  # remove all numbers
                X.append(doc['text'])
                y.append(label)
                cnt += 1
    print(f"[INFO] {dt.now()}: '{cnt}' labels are '{label}'.")
        

# Data Splitting
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)


# FEATURIZATION

# fixate vocabulary
VOCAB = ['south', 'admitted', 'data', 'end', 'expected', 'number', 'studies', 'diagnostic', 'structure', 'impact', 'understand', 'increased', 'coronavirus sarscov', 'reproduction', 'method', 'ongoing', 'higher', 'measures', 'change', 'approach', 'specificity', 'background', 'major', 'secondary', 'admission', 'disease', 'asymptomatic', 'symptoms', 'changes', 'ci', 'detected', 'value', 'observed', 'pandemic', 'public', 'diagnosis', 'specific', 'rapid', 'given', 'parameters', 'covid infection', 'tests', 'effective', 'international', 'especially', 'association', 'setting', 'needed', 'future', 'taken', 'united states', 'simple', 'detection', 'efficacy', 'considered', 'early', 'understanding', 'syndrome coronavirus', 'values', 'immune', 'unknown', 'mean', 'compared', 'evaluate', 'development', 'identification', 'scenarios', 'cases covid', 'proportion', 'assessed', 'immunity', 'modeling', 'viral', 'followed', 'retrospective', 'economic', 'likely', 'low', 'related', 'state', 'weeks', 'small', 'need', 'strategies', 'implications', 'online', 'similar', 'italy', 'severe', 'average', 'workers', 'additional', 'crucial', 'used', 'quarantine', 'confirmed', 'type', 'analysis', 'systematic', 'severity', 'pneumonia', 'estimated', 'protective', 'isolation', 'emergency', 'objective', 'spike', 'uk', 'effectiveness', 'published', 'lockdown', 'basic', 'virus', 'caused', 'outbreak', 'developed', 'history', 'risk factors', 'demonstrated', 'design', 'city', 'identify', 'prior', 'large', 'april', 'control', 'recently', 'hospitals', 'hospitalization', 'respectively', 'months', 'cases', 'scale', 'burden', 'underlying', 'review', 'detect', 'models', 'symptom', 'possible', 'population', 'syndrome', 'people', 'genome', 'propose', 'spread covid', 'social distancing', 'mortality', 'significant', 'did', 'countries', 'patients', 'covid outbreak', 'mathematical', 'wuhan', 'epidemic', 'respiratory syndrome coronavirus', 'included', 'function', 'mild', 'growth', 'implemented', 'covid pandemic', 'hubei', 'risk', 'coronavirus', 'cells', 'care', 'robust', 'distancing', 'patient', 'ncov', 'evaluation', 'covid cases', 'positive', 'having', 'provide', 'outbreaks', 'modelling', 'ratio', 'status', 'determine', 'present', 'world', 'laboratory', 'provides', 'prevent', 'essential', 'molecular', 'test', 'potentially', 'report', 'initial', 'overall', 'community', 'strategy', 'intensive care', 'performance', 'current', 'performed', 'investigate', 'multiple', 'findings', 'lower', 'reduced', 'host', 'acid', 'prediction', 'local', 'conducted', 'therapeutic', 'national', 'key', 'ace', 'covid epidemic', 'second', 'proteins', 'interventions', 'various', 'effect', 'covid disease', 'total', 'vs', 'infectious', 'surveillance', 'distribution', 'outcomes', 'response', 'potential', 'respiratory syndrome', 'assessment', 'capacity', 'characteristics', 'cell', 'health', 'coronaviruses', 'better', 'outcome', 'diseases', 'screening', 'efforts', 'estimates', 'factors', 'deaths', 'incidence', 'acute respiratory syndrome', 'united', 'drug', 'fatality', 'expression', 'develop', 'prevention', 'disease covid']
print(f"[INFO] {dt.now()}: Using a fixed vocabulary with '{len(VOCAB)}' words/ngrams.")

# define preprocessor
def emb_preprocessor(s):
    s = normalize_string(s)
    return re.sub(r'[0-9]', r'', s)

# Word Embedding with fixed VOCAB
emb = TfidfVectorizer(
    preprocessor=emb_preprocessor,
    stop_words='english',  # ignore stopwords!
    vocabulary=VOCAB,
    norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True)

# fit transform
X_emb_train = emb.fit_transform(X_train)
X_emb_test = emb.transform(X_test)
print(f"training set dimension: {X_emb_train.shape}")
print(f"test set dimension: {X_emb_test.shape}")

# save embedding
joblib.dump(emb, os.path.join(MODELPATH, f"embedding-{CURRENT_TIME}.joblib"))
print(f"[INFO] {dt.now()}: Embedding object stored.")



# TRAINING


# classifiers
print(f"[INFO] {dt.now()}: Specify and train binary classifiers.")
clf1 = GaussianNB()
clf2 = SVC(C=0.01, kernel="rbf", class_weight="balanced")
clf3 = RandomForestClassifier(n_estimators=128, min_samples_leaf=0.025, bootstrap=True, max_samples=0.7, oob_score=True, random_state=42, class_weight='balanced_subsample')
clf4 = MLPClassifier(hidden_layer_sizes=(16), activation='relu', solver='adam')
#clf = KNeighborsClassifier(n_neighbors=5)
clf5 = PassiveAggressiveClassifier(C=1, class_weight="balanced")


model = VotingClassifier(estimators=[
    ('clf1', clf1), ('clf2', clf2), ('clf3', clf3), ('clf4', clf4), ('clf5', clf5)],
    voting='hard')


model.fit(X_emb_train.toarray(), y_train)
print(f"[INFO] {dt.now()}: Training completed.")


joblib.dump(model, os.path.join(MODELPATH, f"hardvoting-{CURRENT_TIME}.joblib"))
print(f"[INFO] {dt.now()}: Trained model stored.")


# EVALUATION

# training set error
y_hat = model.predict(X_emb_train.toarray())

print(f"[INFO] {dt.now()}: Evaluation on the Training set")
print("\nConfusion Matrix\n", confusion_matrix(y_train, y_hat))
print("\nBalanced Accuracy\n", balanced_accuracy_score(y_train, y_hat))
print("\nSummary", classification_report(y_train, y_hat))


# test set errors
y_hat = model.predict(X_emb_test.toarray())

print(f"[INFO] {dt.now()}: Evaluation on the Test set")
print("\nConfusion Matrix\n", confusion_matrix(y_test, y_hat))
print("\nBalanced Accuracy\n", balanced_accuracy_score(y_test, y_hat))
print("\nSummary", classification_report(y_test, y_hat))
