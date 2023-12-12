from sklearn.feature_extraction.text import TfidfVectorizer

# def calculate_tfidf(corpus):
#     tfidf_vectorizer = TfidfVectorizer()
#     tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
#     feature_names = tfidf_vectorizer.get_feature_names_out()
#     return tfidf_matrix, feature_names

# corpus = [
#     "The quick brown fox jumps over the lazy dog. This is the first sentence in the corpus.",
#     "A brown cat is chasing a playful squirrel. This is the second sentence.",
#     "The dog and the cat are good friends, but they have their differences.",
#     "Squirrels are known for their agility, and they can climb trees quickly.",
#     "The last sentence in the corpus is here. It's quite different from the others."
# ]

# tfidf_matrix, feature_names = calculate_tfidf(corpus)

# # TFIDF行列の内容を確認
# print(tfidf_matrix.toarray())

# # 各単語のリストを表示
# print(feature_names)


def get_important_words(corpus, threshold=0.2):
    # TFIDFベクトルライザーを作成
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

    # 単語のリストを取得
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # 重要な単語と除去された単語のリストを初期化
    important_words = []
    removed_words = []

    # 単語を分類してリストに追加
    for word, tfidf_score in zip(feature_names, tfidf_matrix.sum(axis=0).A1):
        if tfidf_score >= threshold:
            important_words.append(word)
        else:
            removed_words.append(word)

    return important_words, removed_words

# テスト用のcorpus
corpus = [
    "The quick brown fox jumps over the lazy dog. This is the first sentence in the corpus.",
    "brown cat is chasing a playful squirrel. This is the second sentence.",
    "The dog and the cat are good friends, but they have their differences.",
    "Squirrels are known for their agility, and they can climb trees quickly.",
    "The last sentence in the corpus is here. It's quite different from the others."
]
# corpus = [
#     "quick brown fox jumps over lazy dog. This first sentence corpus.",
#     "brown cat chasing  playful squirrel. This second sentence.",
#     " dog cat good friends, but they have their differences.",
#     "Squirrels known their agility, they can climb trees quickly.",
#     "last sentence corpus here. It's quite different others.",
#     "Trump president unated states. Now president there Biden."
# ]

# 閾値を設定して重要な単語を取得
important_words, removed_words = get_important_words(corpus, threshold=0.35)

# 結果を表示
print("重要な単語:")
print(important_words)
print("\n除去された単語:")
print(removed_words)

