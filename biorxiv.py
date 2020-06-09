import re
import unicodedata
import requests
from pprint import pprint
import pathlib
import os

# Turn a Unicode string to plain ASCII, thanks to
# https://stackoverflow.com/a/518232/2809427
def unicode_to_ascii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')

# Lowercase, trim, and remove non-letter characters
def normalize_string(s):
    s = unicode_to_ascii(s)
    s = re.sub(r'([!.?])', r' \1', s)
    s = re.sub('-', '', s)  # delete dash btw words
    s = re.sub(r'[^a-zA-Z0-9.!?]+', r' ', s)  # replace special characters with whitespace
    s = re.sub(r'\s+', r' ', s)
    return s.lower()


# Convert to serohub format
def to_jekyll_header(dat):
    names = ', '.join([f"\"{row['author_name']}\"" for row in dat['rel_authors']])
    return f"""+++
draft = true
abstract = "{dat['rel_abs']}"
abstract_short = ""
authors = [{names}]
date = "{dat['rel_date']}"
image = ""
image_preview = ""
math = false
publication = "{dat['rel_site']}"
publication_short = ""
title = "{dat['rel_title']}"
doi = "{dat['rel_doi']}"
url_code = ""
url_dataset = ""
url_pdf = "{dat['rel_link']}.full.pdf"
url_project = ""
url_slides = ""
url_video = ""
+++"""


if __name__ == "__main__":
    # Download the whole "SARS-CoV-2" feed
    URL = "https://connect.biorxiv.org/relate/collection_json.php?grp=181"
    resp = requests.get(URL)
    dat = resp.json()

    # a match is any combinatin of keys1 and keys2
    keys1 = [normalize_string(s) for s in ['seroprevalence']]   # , 'serology', 'serological', 'sero-epidemiological', 'antibody', 'antibodies'
    keys2 = [normalize_string(s) for s in ['SARS-CoV-2', 'Covid-19']]
    print(keys1, keys2)

    # search each article
    articles = []
    for idx, article in enumerate(dat['rels']):
        text = normalize_string(f"{article['rel_title']}. {article['rel_abs']}")
        if any([k in text for k in keys1]) and any([k in text for k in keys2]):
            articles.append(article)
    print(f"matches: {len(articles)}")

    # Convert to serohub format and store files
    FILEPATH = "files/biorxiv"
    pathlib.Path(FILEPATH, exist_ok=True)

    for tmp in articles:
        s = to_jekyll_header(tmp)
        FILENAME = f"{tmp['rel_doi']}.md"
        with open(os.path.join(FILEPATH, FILENAME), "w") as fptr:
            fptr.write(s)
        print(f"{FILENAME} stored ...")

