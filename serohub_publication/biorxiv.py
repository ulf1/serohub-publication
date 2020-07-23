
def to_jekyll_header(doc: dict) -> str:
    """Convert biorxiv example to serohub format

    Example:
    --------
    import requests
    import os

    # Download the whole "SARS-CoV-2" feed
    URL = "https://connect.biorxiv.org/relate/collection_json.php?grp=181"
    resp = requests.get(URL)
    data = resp.json()

    # Loop over each article 
    for doc in data['rels']:
        s = to_jekyll_header(doc)
        FILENAME = f"{doc['rel_doi']}.md"
        with open(os.path.join(FILEPATH, FILENAME), "w") as fptr:
            fptr.write(s)
    """
    names = ', '.join([f"\"{row['author_name']}\"" for row in doc['rel_authors']])
    return f"""+++
draft = true
abstract = "{doc['rel_abs']}"
abstract_short = ""
authors = [{names}]
date = "{doc['rel_date']}"
image = ""
image_preview = ""
math = false
publication = "{doc['rel_site']}"
publication_short = ""
title = "{doc['rel_title']}"
doi = "{doc['rel_doi']}"
url_code = ""
url_dataset = ""
url_pdf = "{doc['rel_link']}.full.pdf"
url_project = ""
url_slides = ""
url_video = ""
+++"""
