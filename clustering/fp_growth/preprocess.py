import re
from tqdm import tqdm

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet

# Download the packages
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

from tfidf import CustomTFIDF
from bm25 import OkapiBM25

class TextProcessor:
    def __init__(self, corpus):
        self.tokenized_corpus = self.tokenize(corpus)
        '''
        corpus = [
            "This is the first example sentence.",
            ...
        ]
        tokenized_corpus = [
            ["this", "is", "the", "first", "example", "sentence"],
            ...
        ]
        '''

    def tokenize(self, corpus):
        tokenized_corpus = []
        code_regex = re.compile('[!"#$%&\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]')
        for doc in corpus:
            doc = doc.lower()
            doc = code_regex.sub('', doc)
            tokens = nltk.word_tokenize(doc)
            tokenized_corpus.append(tokens)
        return tokenized_corpus

    def remove_stop_words(self):
        new_corpus = []
        for doc in self.tokenized_corpus:
            # https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
            tokens = [token for token in doc if not token in set(stopwords.words("english") + ["n't", "'m", "'re", "'d", "'ve"])]
            new_corpus.append(tokens)
        self.tokenized_corpus = new_corpus

    def lemmatize(self):
        new_corpus = []
        lemma = nltk.WordNetLemmatizer()
        for doc in self.tokenized_corpus:
            tokens = [lemma.lemmatize(token, 'v') for token in doc]
            new_corpus.append(tokens)
        self.tokenized_corpus = new_corpus

    def remove_dupulicates(self):
        new_corpus = []
        for doc in self.tokenized_corpus:
            tokens = list(set(doc))
            new_corpus.append(tokens)
        self.tokenized_corpus = new_corpus

    def filter_non_noun_verb(self):
        new_corpus = []

        # Create a list of part-of-speech tags for nouns and verbs
        noun_verb_tags = ['NN', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

        for doc in self.tokenized_corpus:
            tokens = [token for token in doc if wordnet.synsets(token) and nltk.pos_tag([token])[0][1] in noun_verb_tags]
            new_corpus.append(tokens)
        self.tokenized_corpus = new_corpus

    def tfidf(self, threshold=0.2, show_removed_wods=False):
        tfidf = CustomTFIDF(self.tokenized_corpus)
        tfidf.fit()
        _, removed_words = tfidf.get_important_words(threshold)

        if show_removed_wods:
            print(f'removed_words: {removed_words}')

        new_corpus = []
        for doc in self.tokenized_corpus:
            tokens = [token for token in doc if not token in removed_words]
            new_corpus.append(tokens)
        self.tokenized_corpus = new_corpus

    def bm25(self, threshold=0.1, show_removed_wods=False):
        bm25 = OkapiBM25(self.tokenized_corpus, k1=1.2, b=0.75, delta=0)
        _, removed_words = bm25.get_important_words(threshold)

        if show_removed_wods:
            print(f'removed_words: {removed_words}')

        new_corpus = []
        for doc in self.tokenized_corpus:
            tokens = [token for token in doc if not token in removed_words]
            new_corpus.append(tokens)
        self.tokenized_corpus = new_corpus


# corpus = [
#     "This is the first example sentence. This is the second sentence.",
#     "Trump isn't a president of U.S. He was a president.",
#     "I'm playing tennis. He is a great tennis player."
# ]

# tp = TextProcessor(corpus)
# tp.remove_stop_words()
# tp.lemmatize()
# tp.filter_non_noun_verb()
# # tp.tfidf(threshold=0.35, show_removed_wods=True)
# tp.bm25(threshold=0.05, show_removed_wods=True)
# # tp.remove_dupulicates()
# print(tp.tokenized_corpus)