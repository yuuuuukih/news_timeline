import os
import json
from argparse import ArgumentParser

from tqdm import tqdm

from preprocess import TextProcessor
from fp_growth import fp_growth

def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/preprocessed/with_content/2019_2022.json')
    parser.add_argument('--min_sup', default=0.05, type=float)
    parser.add_argument('--min_conf', default=0.4, type=float)
    parser.add_argument('--show', default=False, action='store_true')
    args = parser.parse_args()

    with open(args.file_path, 'r') as F:
        data = json.load(F)

    #headline and short_description
    corpus = []
    for doc in data['data']:
        hl_sd = ' '.join([doc['headline'], doc['short_description']])
        corpus.append(hl_sd)

    '''
    Preprocess
    '''
    # Instantiation and tokenize
    tp = TextProcessor(corpus)

    # Remove stop words
    tp.remove_stop_words()

    # Lemmatize
    tp.lemmatize()

    # Filter
    tp.filter_non_noun_verb()

    # TF-IDF
    # tp.tfidf(threshold=0.35, show_removed_wods=False)

    # Okapi BM25
    tp.bm25(threshold=0.05, show_removed_wods=False)

    # Remove dupulicates
    # tp.remove_dupulicates()

    print(tp.tokenized_corpus[:30])

    # data_of_words = []
    # for i, doc in enumerate(tqdm(data['data'])):
    #     hl_sd = ' '.join([doc['headline'], doc['short_description']])

    #     # preprocess
    #     # Eliminate the symbols
    #     hl_sd_azAZ_lower = re.sub("[^a-zA-Z]", " ", hl_sd).lower()
    #     tokens = nltk.word_tokenize(hl_sd_azAZ_lower)

    #     # Eliminate stop words
    #     tokens = [token for token in tokens if not token in set(stopwords.words("english"))]

    #     # Lemmatize
    #     lemma = nltk.WordNetLemmatizer()
    #     tokens = [lemma.lemmatize(token) for token in tokens]

    #     # Eliminate duplicates in tokens
    #     tokens = list(set(tokens))

    #     # Only noun and verb
    #     tokens = filter_non_noun_verb_words(tokens)

    #     data_of_words.append((i, tokens))

    # TF-IDF

    # FP-growth
    # output = fp_growth(data_of_words, min_support=args.min_sup, min_confidence=args.min_conf, show=args.show)

    # # Filter
    # new_output = []
    # for item in output:
    #     if len(item['item']) >= 2 and item['freq'] < 50:
    #         new_output.append(item)

    # # Print
    # print(len(new_output))
    # print(new_output[:20])


if __name__ == '__main__':
    main()