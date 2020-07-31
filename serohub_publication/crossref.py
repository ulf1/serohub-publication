from serohub_publication.utils import unicode_to_ascii, remove_html_tags
import datetime


def to_front_matter(doc: dict) -> str:
    """Convert CrossRef JSON document to serohub dron-matter

    Example:
    --------
    # Loop over each article 
    for doc in data['message']['items']:
        s = to_front_matter(doc)
    """
    names = ', '.join([f"\"{row['given']} {row['family']}\"" for row in doc['author']])
    pubdate = doc['issued']['date-parts'][0]
    if len(pubdate) == 2: pubdate.append(1) 
    return f"""+++
draft = false
abstract = "{remove_html_tags(unicode_to_ascii(doc['abstract'])).strip('\n')}"
abstract_short = ""
authors = [{names}]
date = "{datetime.date(*pubdate).isoformat()}"
image = ""
image_preview = ""
math = false
publication = "{doc['container-title'][0]}"
publication_preprint = ""
publication_short = ""
title = "{remove_html_tags(unicode_to_ascii(doc['title'][0])).strip('\n')}"
doi = "{doc['DOI']}"
url_code = ""
url_dataset = ""
url_pdf = ""
url_project = ""
url_slides = ""
url_video = ""
+++"""
