#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='semi-supervised-morpheme-extraction',
      version='1.0',
      description='Semi-Supervied Morpheme Extraction Framework',
      author='Ramya Narayanaswamy, Dariusz Kuc, Chris Kim',
      url='https://gitlab-beta.engr.illinois.edu/ssme/semi-supervised-morpheme-extraction',
      # packages=['utils'],
      install_requires=['argparse', 'datetime', 'nltk', 'sklearn'])
