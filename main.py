from flask import Flask, request
from nltk.corpus import wordnet as wn
import json
import re

app = Flask(__name__)

NonAlphaMatcher = re.compile(r'[^A-Za-z]+')


def allHyponyms(word):
    # A word may have multiple Synsets, for different meanings, or
    # different uses of the same word.
    # From each Synset, we can get a list of Hyponyms, which are words
    # that are sort of categorically within that Synset's meaning.
    # Note that each Hyponym itself is just another Synset.
    return [h for s in wn.synsets(word) for h in s.hyponyms()]

def allHyponymLemmas(word):
    # Once we have all the hyponyms (from all synsets) for the word,
    # retrieve all the hyponyms' lemmas' names.
    # A lemma's name is the word itself, though it will contain underscores
    # instead of spaces.
    return [l.name() for h in allHyponyms(word) for l in h.lemmas()]


@app.route('/hyponyms/<word>')
def hyponyms(word):
    # Replace any punctuation (targeting those underscores) with spaces
    hypos = [NonAlphaMatcher.sub(' ', w) for w in allHyponymLemmas(word)]
    return json.dumps(hypos)


@app.route('/')
def hello():
    return 'hello'
