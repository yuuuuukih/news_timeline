import os
import json

import copy
from argparse import ArgumentParser

import sys
sys.path.append('../')
from clustering.text_process.preprocess import TextProcessor


def count_elements(list):
    count_dict = {}
    for item in list:
        if str(item) not in count_dict.keys():
            count_dict[str(item)] = list.count(item)
    return count_dict

def add_props_to_docs(docs_data, entities_data):
    output_data = copy.deepcopy(docs_data)
    output_data['description'] = 'This dataset is /datasets/news_category_dataset/preprocessed/with_content/2019_2022.json with the analytics and docs of ID, preprocessed_tokens, entities_info properties added.'
    data = output_data['data']

    '''
    ID prop
    '''
    for i, doc in enumerate(data):
        doc['ID'] = i

    '''
    preprocessed_tokens prop
    '''
    corpus = []
    for doc in data:
        hl_sd = ' '.join([doc['headline'], doc['short_description']])
        corpus.append(hl_sd)

    # Preprocess
    tp = TextProcessor(corpus)
    tp.lemmatize()
    tp.remove_stop_words()
    tp.remove_single_character()
    tp.remove_non_noun()
    #NO BM25
    tp.remove_dupulicates()
    for doc, tokenized_doc in zip(data, tp.tokenized_corpus):
        doc['preprocessed_tokens'] = tokenized_doc

    '''
    entities_info prop
    '''
    entities_list = entities_data['data'][0]['entities']['list']
    for doc in data:
        prop = {'num': -1, 'IDs': [], 'entities': []}
        for entities in entities_list:
            if set(entities['items']) <= set(doc['preprocessed_tokens']):
                prop['IDs'].append(entities['ID'])
                prop['entities'].append(entities['items'])
        prop['num'] = len(prop['IDs'])
        doc['entities_info'] = prop

    '''
    Analytics prop
    '''
    category_list = []
    entities_num_list = []
    for doc in data:
        category_list.append(doc['category'])
        entities_num_list.append(doc['entities_info']['num'])

    output_data['analytics'] = {
        'category': count_elements(category_list),
        'entities_num': {k: v for k, v in sorted(count_elements(entities_num_list).items(), key=lambda item: int(item[0]))}
    }
    # print(output_data['analytics'])

    return output_data

def main():
    parser = ArgumentParser()
    # Path
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/preprocessed/with_content/2019_2022.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/')
    parser.add_argument('--entities_path', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/fp_growth_entities.json')

    args = parser.parse_args()

    with open(args.file_path, 'r') as F:
        docs = json.load(F)

    with open(args.entities_path, 'r') as F:
        entities = json.load(F)

    doc_data = add_props_to_docs(docs, entities)

    # save the json file.
    file_name = 'documents'
    data_json = os.path.join(args.out_dir, f'{file_name}.json')
    with open(data_json, 'w', encoding='utf-8') as json_file:
        json.dump(doc_data, json_file, indent=4, ensure_ascii=False, separators=(',', ': '))
        print(f'Data is saved to {file_name}.json')


if __name__ == '__main__':
    main()