import os
import json

import copy
from argparse import ArgumentParser

import sys

def count_elements(list):
    count_dict = {}
    for item in list:
        if str(item) not in count_dict.keys():
            count_dict[str(item)] = list.count(item)
    return count_dict

def add_props_to_entities(entities_data, docs_data):
    output_data = copy.deepcopy(entities_data)
    entities_list = output_data['data'][0]['entities']['list']

    '''
    docs_info prop
    '''
    for entities in entities_list:
        prop = {'IDs': [], 'docs': []}
        my_entity_ID = entities['ID']

        for doc in docs_data['data']:
            if my_entity_ID in doc['entities_info']['IDs']:
                prop['IDs'].append(doc['ID'])
                prop['docs'].append(doc)

        # validation
        if entities['freq'] != len(prop['IDs']):
            sys.exit('数があっていません！')

        entities['docs_info'] = prop

    return output_data

def main():
    parser = ArgumentParser()
    # Path
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/fp_growth_entities.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/')
    parser.add_argument('--docs_path', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/documents.json')
    parser.add_argument('--json_file_name', default='entities')

    args = parser.parse_args()

    with open(args.file_path, 'r') as F:
        entities = json.load(F)

    with open(args.docs_path, 'r') as F:
        docs = json.load(F)

    entities_data = add_props_to_entities(entities, docs)

    # save the json file.
    data_json = os.path.join(args.out_dir, f'{args.json_file_name}.json')
    with open(data_json, 'w', encoding='utf-8') as json_file:
        json.dump(entities_data, json_file, indent=4, ensure_ascii=False, separators=(',', ': '))
        print(f'Data is saved to {args.json_file_name}.json')


if __name__ == '__main__':
    main()