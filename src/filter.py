"""
Create filtered_diff7, so you need ro create diff7 (generate timelines) at first before running this script.
"""

import os
import json

from argparse import ArgumentParser

from create_dataset.type.split_dataset import SplitDataset

KEYWORD_GROUPS_TO_REMOVE = {
    'words': [
        'person', 'duke', 'users', 'use', 'tweet', 'twitter', 'post', 'jan', 'day', 'week', 'years', 'time',
        'want', 'think', 'ask', 'claim', 'talk', 'hear', 'look', 'write', 'put', 'look', 'suggest', 'support', 'response',
        'test', 'report', 'funniest', 'york', 'gop', 'rep', 'senate', 'house', 'official', 'officials'
    ],
    'pairs': [
        ['move', 'trump'], ['people', 'trump'], ['name', 'trump'], ['help', 'trump'], ['trump', 'video'], ['order', 'trump'], ['chief', 'trump'],
        ['media', 'trump'], ['minister', 'prime'], ['people', 'president'], ['host', 'president'], ['harry', 'sussex'], ['court', 'supreme']
    ]
}

def main():
    parser = ArgumentParser()
    parser.add_argument('--root_dir', default='/mnt/mint/hara/datasets/news_category_dataset/dataset')
    parser.add_argument('--diff', default=7, type=int)
    # parser.add_argument('--sub_dir', default='', help='e.g., diff7_rep1, diff7_rep3, diff7_ins1, diff6_rep1, diff6_rep3, diff6_ins1')
    args = parser.parse_args()

    for what in ['train', 'val', 'test']:
        with open(os.path.join(args.root_dir, f"diff{args.diff}", f"{what}.json"), 'r') as F:
            no_fake_timelines: SplitDataset = json.load(F)

        # Filter out keyword groups (entities) that contain words in KEYWORD_GROUPS_TO_REMOVE
        new_timelines = [
            entity_timeline_data for entity_timeline_data in no_fake_timelines['data']
            if set(entity_timeline_data['entity_items']).intersection(set(KEYWORD_GROUPS_TO_REMOVE['words'])) == set()
            and entity_timeline_data['entity_items'] not in KEYWORD_GROUPS_TO_REMOVE['pairs']
        ]

        # Check how many keyword groups (entities) new_timelines have
        # new_entities = []
        # for entity_timeline_data in new_timelines:
        #     if entity_timeline_data['entity_items'] not in new_entities:
        #         new_entities.append(entity_timeline_data['entity_items'])

        # Check the distribution of the number of docs
        # doc_num_dist = {'4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0}
        # for entity_timeline_data in new_timelines:
        #     num_of_docs = len(entity_timeline_data['timeline'])
        #     doc_num_dist[str(num_of_docs)] += 1

        # Update
        no_fake_timelines['data'] = new_timelines
        # no_fake_timelines['no_fake_timelines_info']['entities_num'] = len(new_entities)
        # no_fake_timelines['no_fake_timelines_info']['timeline_num'] = len(new_timelines)
        # no_fake_timelines['docs_num_in_1_timeline'] = doc_num_dist

        # Save
        sub_dir = f"filtered_diff{args.diff}"
        out_dir = os.path.join(args.root_dir, sub_dir)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, f"{what}.json"), 'w') as F:
            json.dump(no_fake_timelines, F, indent=4, ensure_ascii=False, separators=(',', ': '))
        print(f"Data is saved to {what}.json")


if __name__ == '__main__':
    main()