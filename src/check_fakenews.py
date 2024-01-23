# Description: Check the quality of fake news.
import os
import json
from argparse import ArgumentParser
import random

from create_dataset.fake_news.add_fake_news import FakeNewsGenerater, FakeNewsSetter

from create_dataset.type.split_dataset import SplitDataset


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
    parser.add_argument('--root_dir', default='/mnt/mint/hara/datasets/news_category_dataset/dataset')
    parser.add_argument('--model_name', default='gpt-4-1106-preview')
    parser.add_argument('--diff', default=7, type=int)
    parser.add_argument('--temp_for_fake_news', default=0.8, type=float)
    parser.add_argument('--setting', default='none', choices=FakeNewsSetter.get_choices())
    parser.add_argument('--not_filtered', default=False, action='store_true')
    args = parser.parse_args()

    # Set the output directory
    out_dir = os.path.join(args.root_dir, f"diff{args.diff}") if args.not_filtered else os.path.join(args.root_dir, f"filtered_diff{args.diff}")

    template_no_fake_timemlines: SplitDataset = {
        'name': 'check_fakenews.py',
        'description': 'check the quality of fake news.',
        'entities_num': 0,
        'timelines_num': 0,
        'split_n': 1,
        'setting': '',
        'data': []
    }
    for what in ['train', 'val', 'test']:
        with open(os.path.join(out_dir, f"{what}.json"), 'r') as F:
            no_fake_timelines: SplitDataset = json.load(F)
        template_no_fake_timemlines['data'].extend(no_fake_timelines['data'])

    sampling_num = 20
    template_no_fake_timemlines['data'] = random.sample(template_no_fake_timemlines['data'], sampling_num)

    fng = FakeNewsGenerater(template_no_fake_timemlines, args.setting)
    fng.set_gpt_for_fake_news(args.model_name, args.temp_for_fake_news)
    dir_name = f"diff{args.diff}_{args.setting}" if args.not_filtered else f"filtered_diff{args.diff}_{args.setting}"
    fng.set_file_to_save(os.path.join(args.root_dir, dir_name), 'sample20')
    fng.generate_fake_news_timelines()

if __name__ == '__main__':
    main()
