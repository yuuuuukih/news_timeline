import os
import json
from argparse import ArgumentParser

from tqdm import tqdm
import re

import nltk
from nltk.corpus import stopwords
# Download the packages
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

from fp_growth import fp_growth

def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/preprocessed/with_content/2019_2022.json')
    parser.add_argument('--min_sup', default=0.05, type=float)
    parser.add_argument('--min_conf', default=0.4, type=float)
    args = parser.parse_args()

    with open(args.file_path, 'r') as F:
        data = json.load(F)

    #headline and short_description
    data_of_words = []
    for i, doc in enumerate(tqdm(data['data'][:-1])):
        hl_sd = ' '.join([doc['headline'], doc['short_description']])

        # preprocess
        hl_sd_azAZ_lower = re.sub("[^a-zA-Z]", " ", hl_sd).lower()
        tokens = nltk.word_tokenize(hl_sd_azAZ_lower)

        # Eliminate stop words
        tokens = [token for token in tokens if not token in set(stopwords.words("english"))]

        # Lemmatize
        lemma = nltk.WordNetLemmatizer()
        tokens = [lemma.lemmatize(token) for token in tokens]

        # Eliminate duplicates in tokens
        tokens = list(set(tokens))

        data_of_words.append((i, tokens))

    # FP-growth
    fp_growth(data_of_words, min_support=args.min_sup, min_confidence=args.min_conf)


if __name__ == '__main__':
    main()