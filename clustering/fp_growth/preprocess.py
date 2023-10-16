import functools

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

# decorator
def print_processing_status(func):
    functools.wraps(func)
    def _wrapper(*args, **keywords):
        print(f'== Processing {func.__name__} ... START ==')
        v = func(*args, **keywords)
        print(f'== Processing {func.__name__} ... DONE ==')
        return v
    return _wrapper


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
        corpus = [ doc[ token, ... ], ... ]
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

    def add_doc_id(self, tokenized_corpus):
        corpus_with_docID = [(i, doc) for i, doc in enumerate(tokenized_corpus)]
        return corpus_with_docID

    def process_corpus(self, func):
        new_corpus = []
        for doc in tqdm(self.tokenized_corpus):
            tokens = func(doc)
            new_corpus.append(tokens)
        self.tokenized_corpus = new_corpus

    @print_processing_status
    def remove_stop_words(self):
        def _remove_stop_words_func(doc):
            # https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
            my_stopwords = ["n't", "'m", "'re", "'d", "'ve", "'s", "say", "get", "make", "fox", "news"]
            original_stop_words = set(stopwords.words("english") + my_stopwords)
            tokens = [token for token in doc if not token in original_stop_words]
            return tokens

        self.process_corpus(_remove_stop_words_func)

    @print_processing_status
    def lemmatize(self):
        lemma = nltk.WordNetLemmatizer()
        def _lemmatize_func(doc):
            tokens = [lemma.lemmatize(token, 'v') for token in doc]
            return tokens

        self.process_corpus(_lemmatize_func)


    @print_processing_status
    def remove_single_character(self):
        def _remove_single_character_func(doc):
            tokens = [token for token in doc if len(token) > 1]
            return tokens

        self.process_corpus(_remove_single_character_func)

    @print_processing_status
    def remove_dupulicates(self):
        def _remove_dupulicates_func(doc):
            tokens = list(set(doc))
            return tokens

        self.process_corpus(_remove_dupulicates_func)

    @print_processing_status
    def remove_non_noun_verb(self):
        # Create a list of part-of-speech tags for nouns and verbs
        noun_verb_tags = ['NN', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        def _remove_non_noun_verb_func(doc):
            tokens = [token for token in doc if wordnet.synsets(token) and nltk.pos_tag([token])[0][1] in noun_verb_tags]
            return tokens

        self.process_corpus(_remove_non_noun_verb_func)

    @print_processing_status
    def tfidf(self, threshold=0.2, show_removed_wods=False, num_of_words_to_display=20):
        tfidf = CustomTFIDF(self.tokenized_corpus)
        tfidf.fit()
        _, removed_words = tfidf.get_important_words(threshold)

        if show_removed_wods:
            print(f'removed_words {min(num_of_words_to_display, len(removed_words))}/{len(removed_words)}: {removed_words[:num_of_words_to_display]}')

        def _tfidf_func(doc):
            tokens = [token for token in doc if not token in removed_words]
            return tokens

        self.process_corpus(_tfidf_func)
        return removed_words

    @print_processing_status
    def bm25(self,k1=1.2, threshold=0.1, show_removed_wods=False, num_of_words_to_display=20):
        bm25 = OkapiBM25(self.tokenized_corpus, k1=k1, b=0.75, delta=0)
        _, removed_words = bm25.get_important_words(threshold)

        if show_removed_wods:
            print(f'removed_words {min(num_of_words_to_display, len(removed_words))}/{len(removed_words)}: {removed_words[:num_of_words_to_display]}')

        def _bm25_func(doc):
            tokens = [token for token in doc if not token in removed_words]
            return tokens
        self.process_corpus(_bm25_func)
        return removed_words


# corpus = [
#     "This is the first example sentence. This is the second sentence.",
#     "Trump isn't a president of U.S. He was a president.",
#     "I'm playing tennis. He is a great tennis player.",
#     "Japan is a beautiful country. It has a rich history.",
#     "I love sushi. It's a popular Japanese dish.",
#     "Learning a new language is challenging, but rewarding.",
#     "The weather in Tokyo is often hot and humid in summer.",
#     "I enjoy exploring the unique culture of Japan.",
#     "Traveling to new places broadens your perspective.",
#     "Technology continues to advance at a rapid pace."
# ]


# tp = TextProcessor(corpus)
# tp.remove_stop_words()
# tp.lemmatize()
# tp.filter_non_noun_verb()
# # tp.tfidf(threshold=0.35, show_removed_wods=True)
# tp.bm25(threshold=0.05, show_removed_wods=True)
# tp.remove_dupulicates()
# print(tp.tokenized_corpus)