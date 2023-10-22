import os
import json
import random
from argparse import ArgumentParser

from text_process.preprocess import TextProcessor
from fp_growth.fp_growth import fp_growth

def get_sorted_random_list(list, num):
    new_list = random.sample(list, min(num, len(list)))
    new_list = sorted(new_list, key=lambda x: x['freq'])
    return new_list

def save_entities(data, out_dir, file_name='fp_growth_entities'):
    data_json = os.path.join(out_dir, f'{file_name}.json')

    '''
    Template is generated if file_name.json is not available.
    '''
    if not os.path.exists(data_json):
        format = {
            'name': 'Entities Log',
            'description': 'This file contains the results of previous runs of get_entities.py with hyper parameters.',
            'year': '2019-2022',
            'The number of documents': '7523',
            'data': []
        }
    else:
        with open(data_json, 'r') as json_file:
            format = json.load(json_file)

    # Update
    format['data'].append(data)

    # save the json file.
    with open(data_json, 'w', encoding='utf-8') as json_file:
        json.dump(format, json_file, indent=4, ensure_ascii=False, separators=(',', ': '))
        print(f'Data is saved to {file_name}.json')


def main():
    parser = ArgumentParser()
    # Path
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/preprocessed/with_content/2019_2022.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/')
    # Hyper parameter
    parser.add_argument('--th', default=0.4, type=float)
    parser.add_argument('--min_sup', default=0.01, type=float)
    parser.add_argument('--min_conf', default=0.2, type=float)
    parser.add_argument('--k1', default=1.2, type=float)
    # Preprocess
    parser.add_argument('--rm_stopwords', default=True, type=bool)
    parser.add_argument('--lemmatize', default=True, type=bool)
    parser.add_argument('--rm_single_char', default=True, type=bool)
    parser.add_argument('--rm_non_noun_verb', default=False, type=bool)
    parser.add_argument('--rm_non_noun', default=True, type=bool)
    parser.add_argument('--rm_duplicates', default=True, type=bool)
    parser.add_argument('--tfidf', default=False, type=bool) #DEFAULT ONLY FALSE
    parser.add_argument('--bm25', default=True, type=bool)
    # Comments for conditions
    parser.add_argument('--m', default='', type=str)
    # Basically fixed
    parser.add_argument('--max_output', default=40, type=int)
    parser.add_argument('--max_for_removed_words', default=20, type=int)
    # Others
    parser.add_argument('--table_show', default=False, action='store_true')
    parser.add_argument('--no_save', default=True, action='store_false')

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

    # Lemmatize
    if args.lemmatize:
        tp.lemmatize()

    # Remove stop words
    if args.rm_stopwords:
        tp.remove_stop_words()

    # Remove single character
    if args.rm_single_char:
        tp.remove_single_character()

    # Remove non noun and verb
    if args.rm_non_noun_verb:
        tp.remove_non_noun_verb()

    # Remove non noun
    if args.rm_non_noun:
        tp.remove_non_noun()

    # TF-IDF
    if args.tfidf:
        removed_words = tp.tfidf(threshold=args.th, show_removed_wods=False, num_of_words_to_display=args.max_for_removed_words)

    # Okapi BM25
    if args.bm25:
        removed_words = tp.bm25(threshold=args.th, k1=args.k1, show_removed_wods=False, num_of_words_to_display=args.max_for_removed_words)

    # Remove dupulicates
    if args.rm_duplicates:
        tp.remove_dupulicates()

    # print(tp.tokenized_corpus[:30])

    # Add doc ID
    corpus_with_docID = tp.add_doc_id(tp.tokenized_corpus)

    # FP-growth
    output = fp_growth(corpus_with_docID, min_support=args.min_sup, min_confidence=args.min_conf, show=args.table_show)

    # Filter
    filtered_output = []
    for entities in output:
        # --m examples: "items >= 2", "items >= 2 and freq < 50"
        if len(entities['items']) >= 2:
        # if len(entities['items']) >= 2 and entities['freq'] < 50:
            filtered_output.append(entities)

    sorted_output = sorted(filtered_output, key=lambda x: x['freq'])
    for i, entities in enumerate(sorted_output):
        entities['ID'] = i

    # Save
    # Test
    # data = {
    #     "preprocess": {
    #         "Remove stop words": args.rm_stopwords,
    #         "Lemmatize": args.lemmatize,
    #         "Remove single character": args.rm_single_char,
    #         "Remove non noun and verb": args.rm_non_noun_verb,
    #         "Remove non noun": args.rm_non_noun,
    #         "Remove dupulicates": args.rm_duplicates,
    #         "TF-IDF": args.tfidf,
    #         "Okapi BM25": args.bm25
    #     },
    #     "hparm": {
    #         "threshold": args.th,
    #         "min_support": args.min_sup,
    #         "min_confidence": args.min_conf,
    #         "k1": None if args.bm25 == False else args.k1
    #     },
    #     "words removed by Okapi BM25 / TF-IDF": {
    #         "The number of words": f"{min(args.max_for_removed_words, len(removed_words))}/{len(removed_words)}",
    #         "list": removed_words[:args.max_for_removed_words]
    #     },
    #     "entities": {
    #         "commentso": args.m,
    #         "The number of entities": f"{min(args.max_output, len(filtered_output))}/{len(filtered_output)}",
    #         "list": get_sorted_random_list(filtered_output, args.max_output), # 旧filtered_output[:args.max_output]
    #     }
    # }

    # Produciton
    data = {
        "preprocess": {
            "Remove stop words": args.rm_stopwords,
            "Lemmatize": args.lemmatize,
            "Remove single character": args.rm_single_char,
            "Remove non noun and verb": args.rm_non_noun_verb,
            "Remove non noun": args.rm_non_noun,
            "Remove dupulicates": args.rm_duplicates,
            "TF-IDF": args.tfidf,
            "Okapi BM25": args.bm25
        },
        "hparms": {
            "threshold": args.th,
            "min_support": args.min_sup,
            "min_confidence": args.min_conf,
            "k1": None if args.bm25 == False else args.k1
        },
        "words removed by Okapi BM25 / TF-IDF": {
            "The number of words": len(removed_words),
            "list": removed_words
        },
        "entities": {
            "comments": args.m,
            "The number of entities": len(filtered_output),
            "list": sorted_output
        }
    }
    if args.no_save:
        save_entities(data, args.out_dir)

    # Print
    print(data)


if __name__ == '__main__':
    main()