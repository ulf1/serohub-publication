import unicodedata
import re


# Turn a Unicode string to plain ASCII, thanks to
# https://stackoverflow.com/a/518232/2809427
def unicode_to_ascii(s: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')


# Lowercase, trim, and remove non-letter characters
def normalize_string(s: str) -> str:
    s = unicode_to_ascii(s)
    s = re.sub(r'([!.?])', r' \1', s)
    s = re.sub('-', '', s)  # delete dash btw words
    s = re.sub(r'[^a-zA-Z0-9.!?]+', r' ', s)  # replace special characters with whitespace
    s = re.sub(r'\s+', r' ', s)
    return s.lower()
