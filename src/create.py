'''
Create dataset
'''

import os
import json
from argparse import ArgumentParser

from create_dataset.preprocess.preprocess import Preprocessor

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
    parser.add_argument('--raw_file_path', default='/mnt/mint/hara/datasets/news_category_dataset/raw/News_Category_Dataset_v3.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/test')
    parser.add_argument('--file_name', default='data')
    parser.add_argument('--start_year', default=2019, type=int)
    parser.add_argument('--end_year', default=2022, type=int)
    args = parser.parse_args()

    preprocessor = Preprocessor(args.raw_file_path, args.start_year, args.end_year)
    preprocessed_data = preprocessor.get_preprocessed_data()

    save_dataset(preprocessed_data, args.out_dir, args.file_name)

if __name__ == '__main__':
    main()