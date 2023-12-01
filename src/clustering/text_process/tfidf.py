import math

class CustomTFIDF:
    def __init__(self, corpus, sklearn_method=True):
        self.corpus = corpus
        self.sklearn_method = sklearn_method

        self.word_document_count = {}
        self.idf = {}
        self.tfidf_matrix = None
        self.feature_names = []

    def fit(self):
        # Calculate the count of words appearing in documents
        for document in self.corpus:
            for word in set(document):
                self.word_document_count[word] = self.word_document_count.get(word, 0) + 1

        # Calculate IDF
        total_documents = len(self.corpus)
        for word, doc_count in self.word_document_count.items():
            if self.sklearn_method:
                self.idf[word] = math.log(total_documents + 1 / (doc_count + 1)) + 1
            else:
                self.idf[word] = math.log(total_documents / (doc_count + 1))  # +1 to avoid division by zero

        # Calculate TFIDF matrix
        self.tfidf_matrix = []
        for document in self.corpus:
            tfidf_vector = [0] * len(self.word_document_count)
            # words = document
            for i, word in enumerate(self.word_document_count.keys()):
                tf = document.count(word) / len(document)
                tfidf_vector[i] = tf * self.idf[word]
            self.tfidf_matrix.append(tfidf_vector)

        # Get the list of words
        self.feature_names = list(self.word_document_count.keys())

    def get_matrix(self):
        return self.tfidf_matrix

    def get_feature_names(self):
        return self.feature_names

    def get_important_words(self, threshold=0.2):
        important_words = []
        removed_words = []
        for word, tfidf_scores in zip(self.feature_names, zip(*self.tfidf_matrix)):
            if max(tfidf_scores) >= threshold:
                important_words.append(word)
            else:
                removed_words.append(word)
        return important_words, removed_words

# Test corpus in the new format
# corpus = [
#     ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog', 'this', 'is', 'the', 'first', 'sentence', 'in', 'the', 'corpus'],
#     ['a', 'brown', 'cat', 'is', 'chasing', 'a', 'playful', 'squirrel', 'this', 'is', 'the', 'second', 'sentence'],
#     ['the', 'dog', 'and', 'the', 'cat', 'are', 'good', 'friends', 'but', 'they', 'have', 'their', 'differences'],
#     ['squirrels', 'are', 'known', 'for', 'their', 'agility,', 'and', 'they', 'can', 'climb', 'trees', 'quickly'],
#     ['the', 'last', 'sentence', 'in', 'the', 'corpus', 'is', 'here', "it's", 'quite', 'different', 'from', 'the', 'others']
# ]
# corpus = [
#     ['quick', 'brown', 'fox', 'jumps', 'over', 'lazy', 'dog', 'this', 'first', 'sentence', 'corpus'],
#     ['brown', 'cat', 'chasing', 'playful', 'squirrel', 'this', 'second', 'sentence'],
#     ['dog', 'cat', 'good', 'friends', 'they', 'have', 'their', 'differences'],
#     ['squirrels', 'known', 'their', 'agility,', 'they', 'can', 'climb', 'trees', 'quickly'],
#     ['last', 'sentence', 'corpus', 'here', "it's", 'quite', 'different', 'from', 'others']
# ]

# # Instantiate the TFIDF class and perform the calculation
# tfidf = CustomTFIDF(corpus)
# tfidf.fit()

# # Get the TFIDF matrix
# tfidf_matrix = tfidf.get_matrix()
# print("TFIDF matrix:")
# print(tfidf_matrix)

# # Get the list of words
# feature_names = tfidf.get_feature_names()
# print("\nList of words:", feature_names)

# # Get important words and removed words
# important_words, removed_words = tfidf.get_important_words(threshold=0.2)
# print("\nImportant words:", important_words)
# print("Removed words:", removed_words)
