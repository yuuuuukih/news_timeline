'''
Create dataset
'''

import os
import json
from argparse import ArgumentParser

from create_dataset.preprocess.preprocess import Preprocessor
from create_dataset.keyword_groups.get_keyword_groups import KeywordGroupsGetter

from create_dataset.type.entities import Entities

#Output to json formatted data
def save_dataset(data: dict, out_dir: str, file_name: str):
    out_path = os.path.join(out_dir, f"{file_name}.json")
    try:
        with open(out_path, 'w', encoding='utf-8') as F:
            json.dump(data, F, indent=4, ensure_ascii=False, separators=(',', ': '))
        print(f"Data is saved to {file_name}.json")
    except IOError as e:
        print(f"Error saving data to {file_name}: {e}")

def main():
    parser = ArgumentParser()
    '''
    For ALL
    '''
    parser.add_argument('--raw_file_path', default='/mnt/mint/hara/datasets/news_category_dataset/raw/News_Category_Dataset_v3.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/test')
    parser.add_argument('--file_name', default='data')
    '''
    For Preprocess
    '''
    parser.add_argument('--start_year', default=2019, type=int)
    parser.add_argument('--end_year', default=2022, type=int)
    '''
    For Keyword Groups
    '''
    # Hyper parameter
    parser.add_argument('--th', default=0.6, type=float)
    parser.add_argument('--min_sup', default=0.003, type=float)
    parser.add_argument('--min_conf', default=0.6, type=float)
    parser.add_argument('--k1', default=1.2, type=float)
    # Preprocess
    parser.add_argument('--rm_stopwords', default=True, action='store_false')
    parser.add_argument('--lemmatize', default=True, action='store_false')
    parser.add_argument('--rm_single_char', default=True, action='store_false')
    parser.add_argument('--rm_non_noun_verb', default=False, action='store_true')
    parser.add_argument('--rm_non_noun', default=True, action='store_false')
    parser.add_argument('--rm_duplicates', default=True, action='store_false')
    parser.add_argument('--tfidf', default=False, action='store_true') #DEFAULT ONLY FALSE
    parser.add_argument('--bm25', default=True, action='store_false')
    # Comments for conditions
    parser.add_argument('--m', default='items >= 2', type=str)
    # Basically fixed
    # parser.add_argument('--max_output', default=40, type=int)
    parser.add_argument('--max_for_removed_words', default=20, type=int)
    # Others
    parser.add_argument('--table_show', default=False, action='store_true')

    args = parser.parse_args()

    preprocessor = Preprocessor(args.raw_file_path, args.start_year, args.end_year)
    preprocessed_data = preprocessor.get_preprocessed_data()
    save_dataset(preprocessed_data, args.out_dir, 'preprocessed_data')

    # with open('/mnt/mint/hara/datasets/news_category_dataset/test/data.json', 'r') as F:
    #     preprocessed_data = json.load(F)

    kgg = KeywordGroupsGetter(
        preprocessed_data, args.th, args.min_sup, args.min_conf, args.k1,
        args.rm_stopwords, args.lemmatize, args.rm_single_char, args.rm_non_noun_verb, args.rm_non_noun, args.rm_duplicates, args.tfidf, args.bm25,
        args.m, args.max_for_removed_words, args.table_show
    )
    keyword_groups_data: Entities = kgg.get_keyword_groups()

    save_dataset(keyword_groups_data, args.out_dir, 'keyword_groups')

if __name__ == '__main__':
    main()