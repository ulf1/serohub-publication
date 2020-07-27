#!/usr/bin/env python
from setuptools import setup


setup(
    name='serohub-publication',
    version="0.4.0",
    description='Find relevant SARS-CoV-2 seroprevalance studies',
    license='MIT',
    author='Ulf Hamster',
    author_email='554c46@gmail.com',
    url='https://gitlab.com/ulf1/serohub-publication',
    python_requires='>=3.6',
    install_requires=[
        'dvc==1.1.*',
        'pydrive2==1.4.*',
        'habanero==0.7.*'
    ],
    scripts=[
        'scripts/biorxiv-download.py',
        'scripts/biorxiv-splitup.py',
        'scripts/set1-pull-biorxiv.py',
        'scripts/crossref-download.py',
        'scripts/set1-sync.py',
        'scripts/set1-export.py'
    ],
    packages=['serohub_publication'],
)
