# serohub-publication-crawler

## Purpose
The section of the website [serohub.netlify.app/en/publication](https://serohub.netlify.app/en/publication/) needs to be filled with relevant scientific papers for seroprevalence studies about SARS-Cov-2. 

## Solution
- [ ] get machine-readable access to public literature websites (e.g. XML feeds, R and python packages; We are using DOIs as unique IDs)
- [ ] train a binary text classifer (i.e., annotate/label a training set, find better ML algorithms and word embeddings, label more training examples and train again)
- [ ] run the text classifier's `predict` method on new unknown publications 
- [ ] create `.md` files for the website
