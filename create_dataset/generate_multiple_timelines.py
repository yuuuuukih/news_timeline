import os
import sys
import json
import functools
import datetime
import time
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
    def __init__(self, entities_data, model_name, temp, docs_num_in_1timeline=10, top_tl=0.5):
        super().__init__(model_name, temp, docs_num_in_1timeline, top_tl)

        self.entity_info_list = entities_data['data'][0]['entities']['list']

    def generate_timelines_for_certain_entity(self, entity_info):
        # Define the number of timelines to generate for this entity
        timeline_num = int(int(entity_info['freq'] / self.docs_num_in_1timeline) * self.top_tl)
        # Generate timelines
        output_data = self.generate_timelines(entity_info, timeline_num)
        return output_data

    @measure_exe_time
    def generate_multiple_timelines(self):
        multiple_timelines = []
        for i, entity_info in enumerate(self.entity_info_list):
            print(f"{i+1}/{len(self.entity_info_list)}. ID: {entity_info['ID']}, entity: {entity_info['items']}")
            output_data = self.generate_timelines_for_certain_entity(entity_info)
            multiple_timelines.append(output_data)
        return multiple_timelines


def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/entities.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/')
    parser.add_argument('--model_name', default='gpt-4')
    parser.add_argument('--temp', default=0.8, type=float, help='Temperature for 1st response of GPT.')
    parser.add_argument('--docs', default=10, type=int, help='docs_num_in_1timeline')
    parser.add_argument('--top_tl', default=0.5, type=float, help='top_tl: Number of timelines to be generated, relative to the number of timelines that can be generated.')
    parser.add_argument('--json_file_name', default='no_fake_timelines')
    args = parser.parse_args()

    with open(args.file_path, 'r') as F:
        entities_data = json.load(F)

    mtg = MultipleTimelineGenerator(entities_data, args.model_name, args.temp, args.docs, args.top_tl)
    multiple_timelines = mtg.generate_multiple_timelines()

    no_fake_timelines = {
        'name': args.json_file_name,
        'description': 'Timeline dataset without fake news.',
        'date': f'{datetime.datetime.today()}',
        'setting': {
            'model': args.model_name,
            'temperature': {
                '1st_response': args.temp,
                '2nd_response': 0,
            },
            'docs_num_in_1timeline': args.docs,
            'top_tl': args.top_tl
        },
        'data': multiple_timelines
    }

    # save the json file.
    data_json = os.path.join(args.out_dir, f'{args.json_file_name}.json')
    with open(data_json, 'w', encoding='utf-8') as F:
        json.dump(no_fake_timelines, F, indent=4, ensure_ascii=False, separators=(',', ': '))
        print(f'Data is saved to {args.json_file_name}.json')


if __name__ == '__main__':
    main()