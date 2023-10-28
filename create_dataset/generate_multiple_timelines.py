import os
import sys

import json
from argparse import ArgumentParser

from generate_timeline import TimelineGenerator

# class MultipleTimelineGenerator(TimelineGenerator):
#     def __init__(self, entities_data, model_name, temp, docs_num_in_1timeline=10, top_tl=0.5):
#         super().__init__(entity_info=None, model_name=model_name, temp=temp, docs_num_in_1timeline=docs_num_in_1timeline, top_tl=top_tl)

#         self.entity_info_list = entities_data['data'][0]['entities']['list']
#         # multiple timelines
#         self.multiple_timelines = []

#     def generate_multiple_timelines(self):
#         for entity_info in self.entity_info_list:
#             self.entity_info_left = entity_info
#             self.generate_timelines()
#             outout_data = {
#             'entity_ID': entity_info['ID'],
#             'entity_items': entity_info['items'],
#             'timeline_info': {
#                 'timeline_num': self.timeline_num,
#                 'data': self.timelines
#             }
#         }

#     def save_timelines(self):
#         pass

def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/entities.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/')
    parser.add_argument('--model_name', default='gpt-4')
    parser.add_argument('--temp', default=0.8, type=float)
    parser.add_argument('--top_tl', default=0.5, type=float, help="top_tl: Number of timelines to be generated, relative to the number of timelines that can be generated.")
    args = parser.parse_args()

    with open(args.file_path, 'r') as F:
        entities_data = json.load(F)

    # entity_info_list = entities_data['data'][0]['entities']['list']

if __name__ == '__main__':
    main()