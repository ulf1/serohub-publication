from datetime import datetime as dt

# PREPARE
import os
import json
from serohub_publication.utils import  normalize_string
# python3 -m spacy download en_core_web_sm
import spacy
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

# define preprocessor
# https://spacy.io/usage/spacy-101#annotations-pos-deps
def emb_preprocessor(s):
    # clean string
    sent = normalize_string(s)
    # Lemmatization
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sent)
    lemmas = [token.lemma_ for token in doc if token.tag_ in ('NNP', 'VBG', 'NN') and len(token.lemma_)>1]
    return " ".join(lemmas)

# Find VOCAB
"""
emb = TfidfVectorizer(
    preprocessor=emb_preprocessor,
    stop_words='english',  # ignore stopwords!
    analyzer='word', ngram_range=(1, 2),  # single word or bigram
    min_df = 3,  # lemma exist at least 3x times
    norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True)
X_for_rf = emb.fit_transform(X_train)
"""

"""
np.random.seed(42)
X_for_rf2 = scipy.sparse.hstack([X_for_rf, np.random.random((X_for_rf.shape[0], 1))])
X_for_rf2.shape

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(
    n_estimators=512, min_samples_leaf=0.025, 
    bootstrap=True, max_samples=0.7, oob_score=True, random_state=42, 
    class_weight='balanced_subsample')
clf.fit(X_for_rf2, y_train)

feat_names = np.array(emb.get_feature_names() + ['OUR_RANDOM_VAR'])
feat_score = clf.feature_importances_

mask = feat_names == "OUR_RANDOM_VAR"
mask2 = feat_score > feat_score[mask]
VOCAB = list(feat_names[mask2])
len(VOCAB)
"""

"""
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(
    n_estimators=1024, min_samples_leaf=0.0125, 
    bootstrap=True, max_samples=0.7, oob_score=True, random_state=42, 
    class_weight='balanced_subsample')
clf.fit(X_for_rf, y_train)

feat_names = np.array(emb.get_feature_names())
feat_score = clf.feature_importances_
# idx = np.argsort(feat_score)
# idx = np.flipud(idx)
# feat_score[idx]
# feat_names[idx[:1024]]
VOCAB = list(feat_names[feat_score > 0])
len(VOCAB)
"""

# fixed VOCAB
VOCAB = ['ability', 'absence', 'access', 'accord', 'account', 'accuracy', 'ace2', 'acid', 'activity', 'addition', 'admission', 'age', 'agent', 'aim', 'air', 'analysis', 'antibody', 'application', 'approach', 'april', 'area', 'assay', 'assess', 'assessment', 'association', 'attention', 'background', 'basis', 'behavior', 'bind', 'blood', 'burden', 'capacity', 'care', 'care unit', 'case', 'case fatality', 'cause', 'cell', 'center', 'chain', 'challenge', 'change', 'chest', 'china', 'ci', 'city', 'cohort', 'cohort study', 'combination', 'community', 'compare', 'comparison', 'concern', 'conclusion', 'confidence', 'consider', 'contact', 'containment', 'context', 'contrast', 'control', 'coronavirus', 'coronavirus covid19', 'coronavirus disease', 'coronavirus sarscov2', 'correlation', 'cough', 'count', 'country', 'course', 'covid19', 'covid19 case', 'covid19 covid19', 'covid19 disease', 'covid19 epidemic', 'covid19 infection', 'covid19 mortality', 'covid19 outbreak', 'covid19 pandemic', 'covid19 sarscov2', 'covid19 study', 'covid19 use', 'crisis', 'ct', 'curve', 'data', 'database', 'dataset', 'date', 'day', 'death', 'december', 'decrease', 'demand', 'design', 'detection', 'detection sarscov2', 'develop', 'development', 'diabetes', 'diagnosis', 'difference', 'discussion', 'disease', 'disease covid19', 'disease severity', 'distance', 'distancing', 'distress', 'distribution', 'domain', 'drug', 'duration', 'effect', 'effectiveness', 'efficacy', 'emerge', 'emergence', 'emergency', 'end', 'entry', 'epidemic', 'equipment', 'estimate', 'estimation', 'europe', 'evaluation', 'evidence', 'evolution', 'exist', 'experience', 'exposure', 'expression', 'extent', 'factor', 'failure', 'fatality', 'february', 'fever', 'follow', 'forecast', 'framework', 'france', 'function', 'ge', 'gene', 'genome', 'germany', 'government', 'group', 'growth', 'health', 'health care', 'healthcare', 'heterogeneity', 'history', 'home', 'hospital', 'hospitalization', 'host', 'hubei', 'hubei province', 'hypertension', 'icu', 'identification', 'identify', 'igg', 'illness', 'immunity', 'impact', 'implementation', 'importance', 'incidence', 'include', 'increase', 'incubation', 'index', 'india', 'indicate', 'infection', 'information', 'interaction', 'interpretation', 'interval', 'intervention', 'introduction', 'investigation', 'isolation', 'italy', 'january', 'june', 'knowledge', 'laboratory', 'lack', 'lead', 'level', 'life', 'limit', 'literature', 'lockdown', 'lung', 'majority', 'make', 'management', 'march', 'mean', 'measure', 'mechanism', 'metaanalysis', 'method', 'mitigation', 'mobility', 'model', 'model covid19', 'modeling', 'modelling', 'mortality', 'mortality covid19', 'need', 'network', 'new', 'new york', 'novel', 'number', 'number covid19', 'objective', 'onset', 'order', 'organization', 'outbreak', 'outbreak coronavirus', 'outcome', 'pandemic', 'paper', 'parameter', 'patient', 'pattern', 'pcr', 'peak', 'percentage', 'performance', 'period', 'phase', 'place', 'plasma', 'pneumonia', 'point', 'policy', 'polymerase', 'population', 'potential', 'predict', 'prediction', 'presence', 'prevalence', 'prevention', 'probability', 'process', 'progression', 'proportion', 'protection', 'protein', 'protocol', 'province', 'public', 'pubmed', 'quality', 'quarantine', 'r0', 'range', 'rate', 'ratio', 'rbd', 'reaction', 'receptor', 'recovery', 'reduce', 'reduction', 'reference', 'regard', 'region', 'regression', 'relationship', 'replication', 'report', 'reproduction', 'reproduction number', 'research', 'resource', 'response', 'result', 'review', 'risk', 'risk covid19', 'rna', 'role', 'rtpcr', 'safety', 'sample', 'sars', 'sarscov', 'sarscov2', 'sarscov2 covid19', 'sarscov2 infection', 'sarscov2 pandemic', 'sarscov2 rna', 'sarscov2 spike', 'sarscov2 virus', 'scale', 'scenario', 'score', 'screening', 'search', 'selection', 'sensitivity', 'sensitivity specificity', 'sequence', 'sequencing', 'series', 'serum', 'set', 'severity', 'sex', 'sir', 'situation', 'size', 'source', 'south', 'spain', 'specificity', 'spike', 'spike protein', 'spread', 'spread covid19', 'staff', 'stage', 'start', 'state', 'states', 'status', 'strategy', 'structure', 'study', 'study covid19', 'suggest', 'support', 'surface', 'surveillance', 'survey', 'swab', 'symptom', 'syndrome', 'syndrome coronavirus', 'target', 'temperature', 'test', 'testing', 'therapy', 'threat', 'time', 'tool', 'total', 'transmission', 'travel', 'treatment', 'trend', 'type', 'uk', 'underlie', 'understand', 'understanding', 'unit', 'united', 'united states', 'university', 'usa', 'use', 'vaccine', 'validation', 'value', 'variation', 'ventilation', 'viral', 'virus', 'wave', 'way', 'week', 'work', 'world', 'world health', 'wuhan', 'wuhan china']
print(f"[INFO] {dt.now()}: Using a fixed vocabulary with '{len(VOCAB)}' words/ngrams.")


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
