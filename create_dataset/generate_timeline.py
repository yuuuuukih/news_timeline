import os
import sys
import openai

import json
from argparse import ArgumentParser

from set_timeline import TimelineSetter

class TimelineGenerator(TimelineSetter):
    '''
    docs_num_in_1timeline: The number of documents contained in ONE timeline,
    top_tl: Number of timelines to be generated, relative to the number of timelines that can be generated.
    '''
    def __init__(self, entity_info, model_name, temp, docs_num_in_1timeline=10, top_tl=0.5) -> None:
        # super
        super().__init__(model_name, temp, docs_num_in_1timeline, top_tl)
        self.entity_info_left = entity_info
        '''structure of entity_info
        {
            "freq": xxx,
            "items": ["xxx", ...],
            "ID": 0,
            "docs_info": {
                "IDs": [],
                "docs": [
                    {
                        "link": xxx,
                        "headline": xxx,
                        "category": xxx,
                        "short_description": xxx,
                        "authors": xxx,
                        "date": xxx,
                        "year": xxx,
                        "month": xxx,
                        "day": xxx,
                        "content": xxx,
                        "ID": xxx,
                        "preprocessed_tokens": [
                            "xxx",
                            ...
                        ],
                        "entities_info": {
                            "num": xxx,
                            "IDs": [],
                            "entities": []
                        }
                    },
                    ...
                ]
            }
        },
        '''

        # timeline
        self.timelines = []

        # The number of timeline to generate
        # e.g., int(int(55/10)*0.5)
        self.timeline_num = int(int(entity_info['freq'] / self.docs_num_in_1timeline) * top_tl)

    def generate_timelines(self):
        for i in range(self.timeline_num):
            print(f'=== {i+1}/{self.timeline_num}. START ===')

            timeline_info, IDs_from_gpt = self.generate_story_and_timeline(self.entity_info_left)
            self.timelines.append(timeline_info)

            # Update entity info left
            self.entity_info_left['docs_info'] = {
                'IDs': list(set(self.entity_info_left['docs_info']['IDs']) - set(IDs_from_gpt)),
                'docs': self._delete_dicts_by_id(self.entity_info_left['docs_info']['docs'], IDs_from_gpt)
            }
            self.entity_info_left['freq'] = len(self.entity_info_left['docs_info']['IDs'])

            print(f'=== {i+1}/{self.timeline_num}. DONE ===')


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

    # Test ['russia', 'ukraine']
    entity_info = entities_data['data'][0]['entities']['list'][236]
    # print(entity_info['docs_info']['IDs'])

    tg = TimelineGenerator(entity_info, args.model_name, args.temp, top_tl=args.top_tl)
    tg.generate_timelines()
    outout_data = {
            'entity_ID': entity_info['ID'],
            'entity_items': entity_info['items'],
            'timeline_info': {
                'timeline_num': tg.timeline_num,
                'data': tg.timelines
            }
        }
    print('\n')
    # print(timelines)

    # save the json file.
    file_name = 'timeline_test_' + '_'.join(entity_info['items'])
    data_json = os.path.join(args.out_dir, f'{file_name}.json')
    with open(data_json, 'w', encoding='utf-8') as json_file:
        json.dump(outout_data, json_file, indent=4, ensure_ascii=False, separators=(',', ': '))
        print(f'Data is saved to {file_name}.json')



if __name__ == '__main__':
    main()