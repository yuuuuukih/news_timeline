'''
Process the raw news category dataset to json format.
'''
import os
import json
from argparse import ArgumentParser

'''raw data example
{
    "link": "https://www.huffpost.com/entry/covid-boosters-uptake-us_n_632d719ee4b087fae6feaac9",
    "headline": "Over 4 Million Americans Roll Up Sleeves For Omicron-Targeted COVID Boosters",
    "category": "U.S. NEWS",
    "short_description": "Health experts said it is too early to predict whether demand would match up with the 171 million doses of the new boosters the U.S. ordered for the fall.",
    "authors": "Carla K. Johnson, AP",
    "date": "2022-09-23"
}
'''

# Formatting the dataset.
def format_json(file_path):
    data = [json.loads(line.strip()) for line in open(file_path)]
    print('Format completed.')
    return data

# Add the year, month, day infomation as properties.
def add_time_info(data):
    formatted_data = []
    for d in data:
        year, month, day = d['date'].split('-')
        new_d = d.copy()
        new_d['year'] = year
        new_d['month'] = month
        new_d['day'] = day
        formatted_data.append(new_d)

    print('Time info addition completed.')
    return formatted_data

def main():
    parser = ArgumentParser()
    parser.add_argument('--raw_file_path', default='/mnt/mint/hara/datasets/news_category_dataset/raw/News_Category_Dataset_v3.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/preprocessed/without_content')
    parser.add_argument('--file_name', default='data.json')
    args = parser.parse_args()

    data = format_json(args.raw_file_path)
    formatted_data = add_time_info(data)
    out_path = os.path.join(args.out_dir, args.file_name)

    output = {'name': 'News_Category_Dataset_v3 without content', 'data': formatted_data}
    with open(out_path, 'w', encoding='utf-8') as F:
        json.dump(output, F, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()