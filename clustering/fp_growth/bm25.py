import math

class OkapiBM25:
    def __init__(self, corpus, k1=1.2, b=0.75, delta=0):
        self.corpus = corpus
        self.k1 = k1
        self.b = b
        self.delta = delta

        self.N = len(corpus)  # The number of documents
        self.avgdl = sum([len(doc) for doc in corpus]) / self.N
        self.idf = self.compute_idf()

    def compute_idf(self):
        idf = {}
        for doc in self.corpus:
            for term in set(doc):
                idf[term] = idf.get(term, 0) + 1
        for term, doc_freq in idf.items():
            idf[term] = math.log((self.N - doc_freq + 0.5) / (doc_freq + 0.5))
        return idf

    def score(self, query):
        scores = [0] * self.N
        for i in range(self.N):
            doc = self.corpus[i]
            doc_length = len(doc)
            for term in query:
                if term in self.idf:
                    idf = self.idf[term]
                    tf = doc.count(term) / doc_length
                    new_tf = (tf * (self.k1 + 1)) / (tf + self.k1 * (1 - self.b + self.b * (doc_length / self.avgdl))) + self.delta
                    scores[i] += idf * new_tf
        return scores

    def get_term_scores(self):
        term_scores = {}
        for doc in self.corpus:
            for term in set(doc):
                if term not in term_scores.keys():
                    scores = self.score([term])
                    term_scores[term] = scores
        return term_scores

    def get_important_words(self, threshold=0.2):
        term_scores = self.get_term_scores()
        important, others = [], []
        for term, score in term_scores.items():
            if max(score) >= threshold:
                important.append(term)
            else:
                others.append(term)
        return important, others

# Example usage
# corpus = [
#     ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog'],
#     ['A', 'brown', 'cat', 'is', 'sleeping', 'on', 'the', 'couch'],
#     ['the', 'sky', 'is', 'blue', 'and', 'the', 'sun', 'is', 'shining']
# ]
# corpus = [
#     ['quick', 'brown', 'fox', 'jumps', 'over', 'lazy', 'dog'],
#     ['brown', 'cat', 'sleeping', 'couch'],
#     ['sky', 'blue', 'sun', 'shining']
# ]

# bm25 = OkapiBM25(corpus)
# # print(bm25.get_term_scores())

# important_words, other_words = bm25.get_important_words()

# print("Important Words:", important_words)
# print("Other Words:", other_words)
