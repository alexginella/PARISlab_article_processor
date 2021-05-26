import string
import re
import json
import pandas as pd
import numpy as np
import pprint
from pathlib import Path

import spacy
from spacy.matcher import Matcher 
from spacy import displacy
from gensim.models import Word2Vec
import en_core_web_sm
nlp = en_core_web_sm.load()

import nltk
nltk.download('stopwords')

import chemdataextractor as cde
from chemdataextractor import Document
from chemdataextractor.nlp.tokenize import ChemWordTokenizer

from prettytable import PrettyTable