import os
import json
from create_dataset.type.entities import Entities, EntityData


def main():
    '''
    キーワードグループのtop-30を表示する
    '''
    # with open('/mnt/mint/hara/datasets/news_category_dataset/dataset/keyword_groups.json', 'r') as F:
    #     keyword_groups: Entities = json.load(F)
    # keyword_groups_list: list[EntityData] = keyword_groups['data'][0]['entities']['list']
    # top_30: list[EntityData] = keyword_groups_list[::-1][:30]
    # for i, entity_data in enumerate(top_30):
    #     print(i, entity_data['freq'], entity_data['items'], len(entity_data['docs_info']['IDs']))

    '''
    Fake news datasetの統計情報を表示する(baseを用いる)
    '''
    fake_news_setting = 'ins1'
    diff = 6
    statistics = {
        'diff': diff,
        'train': {
            'real': 0,
            'fake': 0
        },
        'val': {
            'real': 0,
            'fake': 0
        },
        'test': {
            'real': 0,
            'fake': 0
        }
    }
    for what in ['train', 'val', 'test']:
        with open(f'/mnt/mint/hara/datasets/news_category_dataset/dataset/diff{diff}_{fake_news_setting}/base/{what}.json', 'r') as F:
            fake_news_dataset = json.load(F)
        for example in fake_news_dataset['data']:
            if example['tgt'] == 1: # mean fake
                statistics[what]['fake'] += 1
            elif example['tgt'] == 0:
                statistics[what]['real'] += 1
            else:
                raise ValueError(f'Invalid tgt: {example["tgt"]}')

    print(statistics)



if __name__ == '__main__':
    main()