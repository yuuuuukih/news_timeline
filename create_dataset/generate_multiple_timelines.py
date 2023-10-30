import os
import sys
import json
import functools
import datetime
import time
from collections import Counter
from argparse import ArgumentParser

from set_timeline import TimelineSetter

# decorator
def measure_exe_time(func):
    functools.wraps(func)
    def _wrapper(*args, **keywords):
        start_time = time.time()

        v = func(*args, **keywords)

        end_time = time.time()
        exe_time = end_time - start_time
        hours, remainder = divmod(exe_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_time = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        print(f"The execution time of the {func.__name__} function is {formatted_time}.")

        return v
    return _wrapper

class MultipleTimelineGenerator(TimelineSetter):
    def __init__(self, entities_data, model_name, temp, min_docs_num_in_1timeline=8, max_docs_num_in_1timeline=10, top_tl=0.5, start_entity_id=0):
        super().__init__(model_name, temp, min_docs_num_in_1timeline, max_docs_num_in_1timeline, top_tl)

        self.entity_info_list = entities_data['data'][0]['entities']['list'][start_entity_id:]

    @measure_exe_time
    def generate_multiple_timelines(self):
        for i, entity_info in enumerate(self.entity_info_list):
            print('\n')
            print(f"{i+1}/{len(self.entity_info_list)}. ID: {entity_info['ID']}, entity: {entity_info['items']}")
            # Define the number of timelines to generate for this entity
            timeline_num = int(int(entity_info['freq'] / self.max_docs_num_in_1timeline) * self.top_tl)
            # Generate timelines
            output_data = self.generate_timelines(entity_info, timeline_num)
            # Save
            self.save_timelines(output_data)

    # For save timelines
    def save_timelines(self, timeline_data, name_to_save='Data'):
        # Open the file
        file_path = os.path.join(self.__out_dir, f"{self.__json_file_name}.json")
        try:
            with open(file_path, 'r') as F:
                no_fake_timelines = json.load(F)
        except FileNotFoundError:
            no_fake_timelines = {
                'name': self.__json_file_name,
                'description': 'Timeline dataset without fake news.',
                'date': f'{datetime.datetime.today()}',
                'entities_num': 0,
                'setting': {
                    'model': self.model_name,
                    'temperature': {
                        '1st_response': self.temp,
                        '2nd_response': 0,
                    },
                    'docs_num_in_1timeline': {
                        'min': self.min_docs_num_in_1timeline,
                        'max': self.max_docs_num_in_1timeline
                    },
                    'top_tl': self.top_tl,
                    'max_reexe_num': self.get_max_reexe_num()
                },
                'analytics': {
                    'docs_num_in_1_timeline': {},
                    're_execution_num': {},
                    'no_timeline_entity_id': []
                },
                'data': []
            }
        # Update
        no_fake_timelines['data'].append(timeline_data)
        no_fake_timelines['entities_num'] = len(no_fake_timelines['data'])

        count_occurrences = lambda list: dict(sorted(Counter(list).items(), key=lambda item: item[0]))
        no_fake_timelines['analytics']['docs_num_in_1_timeline'] = self.add_dicts(no_fake_timelines['analytics']['docs_num_in_1_timeline'], count_occurrences(self.analytics_docs_num))
        no_fake_timelines['analytics']['re_execution_num'] = self.add_dicts(no_fake_timelines['analytics']['re_execution_num'], count_occurrences(self.analytics_reexe_num))
        no_fake_timelines['analytics']['no_timeline_entity_id'].extend(self.no_timeline_entity_id)
        # save the json file.
        with open(file_path, 'w', encoding='utf-8') as F:
            json.dump(no_fake_timelines, F, indent=4, ensure_ascii=False, separators=(',', ': '))
            print(f'{name_to_save} is saved to {self.__json_file_name}.json')

    def set_file_to_save(self, json_file_name, out_dir):
        self.__json_file_name = json_file_name
        self.__out_dir = out_dir

    def add_dicts(self, dict1, dict2):
        result = dict1.copy()
        for key, value in dict2.items():
            str_key = str(key)
            if str_key in result.keys():
                result[str_key] += value
            else:
                result[str_key] = value

        sorted_result = {k: result[k] for k in sorted(result.keys())}
        return sorted_result



def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/entities.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/')
    parser.add_argument('--model_name', default='gpt-4')
    parser.add_argument('--temp', default=0.8, type=float, help='Temperature for 1st response of GPT.')
    parser.add_argument('--min_docs', default=6, type=int, help='min_docs_num_in_1timeline')
    parser.add_argument('--max_docs', default=10, type=int, help='max_docs_num_in_1timeline')
    parser.add_argument('--top_tl', default=0.5, type=float, help='top_tl: Number of timelines to be generated, relative to the number of timelines that can be generated.')
    parser.add_argument('--json_file_name', default='no_fake_timelines')
    parser.add_argument('--max_reexe_num', default=1, type=int)
    parser.add_argument('--start_entity_id', default=0, type=int)
    args = parser.parse_args()

    with open(args.file_path, 'r') as F:
        entities_data = json.load(F)

    mtg = MultipleTimelineGenerator(entities_data, args.model_name, args.temp, args.min_docs, args.max_docs, args.top_tl, args.start_entity_id)
    mtg.set_max_reexe_num(args.max_reexe_num)
    mtg.set_file_to_save(json_file_name=args.json_file_name, out_dir=args.out_dir)
    mtg.generate_multiple_timelines()

'''
テストの時は
- [:]の中を確認
- get_gpt_response.pyのcontentを確認
'''


if __name__ == '__main__':
    main()