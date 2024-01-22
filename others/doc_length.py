import os
import json
from argparse import ArgumentParser

from create_dataset.type.fake_news_dataset import FakeNewsDataset
import numpy as np

import numpy as np

def calculate_boxplot_data(data):
    """箱ひげ図に必要な統計値（平均値含む）を計算する関数"""
    min_val = np.min(data)  # 最小値
    max_val = np.max(data)  # 最大値
    q1 = np.percentile(data, 25)  # 第一四分位数 (Q1)
    q3 = np.percentile(data, 75)  # 第三四分位数 (Q3)
    median = np.median(data)  # 中央値
    mean = np.mean(data)  # 平均値

    iqr = q3 - q1  # 四分位範囲 (IQR)
    lower_bound = q1 - (1.5 * iqr)  # 外れ値に対する下限界
    upper_bound = q3 + (1.5 * iqr)  # 外れ値に対する上限界

    # 外れ値を除いた実際の最小値と最大値
    actual_min_val = min([x for x in data if x >= lower_bound], default=min_val)
    actual_max_val = max([x for x in data if x <= upper_bound], default=max_val)

    return {
        'min': min_val,
        'max': max_val,
        'q1': q1,
        'q3': q3,
        'median': median,
        'mean': mean,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'actual_min_val': actual_min_val,
        'actual_max_val': actual_max_val,
        'outliers': [x for x in data if x < lower_bound or x > upper_bound]
    }

def main():
    parser = ArgumentParser()
    parser.add_argument("--root_dir", default='/mnt/mint/hara/datasets/news_category_dataset/dataset')
    parser.add_argument('--sub_dir', default='', help='e.g., diff7_rep1, diff7_rep3, diff7_ins1, diff6_rep1, diff6_rep3, diff6_ins1')
    args = parser.parse_args()

    real_doc_length = {
        'headline': {
            'word': [],
            'char': []
        },
        'short_description': {
            'word': [],
            'char': []
        },
        'content': {
            'word': [],
            'char': []
        }
    }
    fake_doc_length = {
        'headline': {
            'word': [],
            'char': []
        },
        'short_description': {
            'word': [],
            'char': []
        },
        'content': {
            'word': [],
            'char': []
        }
    }

    data_dir = os.path.join(args.root_dir, args.sub_dir)

    data_list = ['train', 'val', 'test']
    content_none_count = 0

    for what in data_list:
        file_path = os.path.join(data_dir, f'{what}.json')
        with open(file_path, 'r') as f:
            data: FakeNewsDataset = json.load(f)
        for timeline_data_info in data['data']:
            for doc in timeline_data_info['timeline']:
                try:
                    if doc['is_fake']:
                        for key in ['headline', 'short_description', 'content']:
                            fake_doc_length[key]['char'].append(len(doc[key]))
                            fake_doc_length[key]['word'].append(len(doc[key].split()))
                    else:
                        for key in ['headline', 'short_description', 'content']:
                            real_doc_length[key]['char'].append(len(doc[key]))
                            real_doc_length[key]['word'].append(len(doc[key].split()))
                except TypeError as e :
                    print(e)
                    print(doc)
                    print(what)
                    print(timeline_data_info['entity_id'])
                    print(timeline_data_info['entity_items'])
                    content_none_count += 1

    stats_words = {
        'real': {
            'headline': 0,
            'short_description': 0,
            'content': 0
        },
        'fake': {
            'headline': 0,
            'short_description': 0,
            'content': 0
        }
    }

    for key in ['headline', 'short_description', 'content']:
        stats_words['real'][key] = calculate_boxplot_data(real_doc_length[key]['word'])
        stats_words['fake'][key] = calculate_boxplot_data(fake_doc_length[key]['word'])

    print(stats_words)

    # Average of length
    # for key in ['headline', 'short_description', 'content']:
    #     for key2 in ['word', 'char']:
    #         real_doc_length[key][key2] = sum(real_doc_length[key][key2]) / len(real_doc_length[key][key2])
    #         fake_doc_length[key][key2] = sum(fake_doc_length[key][key2]) / len(fake_doc_length[key][key2])


    # print('\n')
    # print('real_doc_length')
    # print(real_doc_length)
    # print('fake_doc_length')
    # print(fake_doc_length)

if __name__ == "__main__":
    main()