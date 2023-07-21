'''
Get the content of articles by scraping
'''

import os
import json
import html
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from argparse import ArgumentParser

# Scrape the article content by getting url
def scrape_article_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP error check

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = " ".join([html.unescape(p.get_text().strip()) for p in paragraphs if p.get_text().strip()])
        if content:
            return content
        else:
            raise ValueError("No article content found.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Receives a list of data, scrapes it, and outputs a list with the article content added.
def add_content(data_list):
    formatted_data = []

    for d in tqdm(data_list):
        # Double quotes are obtained as "\".
        content = scrape_article_content(d['link'])

        new_d = d.copy()
        new_d['content'] = content
        formatted_data.append(new_d)

    print('Contents are added completely.')
    return formatted_data

# Output to json formatted data
def output_to_json(output, out_path, file_name):
    try:
        with open(out_path, 'w', encoding='utf-8') as F:
            json.dump(output, F, indent=4, ensure_ascii=False)
        print(f"Data saved to {file_name}")
    except IOError as e:
        print(f"Error saving data to {file_name}: {e}")


def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/preprocessed/without_content/data.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/preprocessed/with_content')
    parser.add_argument('--file_name', default='data.json')
    parser.add_argument('--start_year', default=2012, type=int)
    parser.add_argument('--end_year', default=2022, type=int)
    args = parser.parse_args()

    # Get data with no content.
    with open(args.file_path, 'r') as F:
        data = json.load(F)

    # Split the data over an appropriate period of time (args.start_year to args.end_year).
    split_data = [d for d in data['data'] if args.start_year <= int(d['year']) <= args.end_year] if not (args.start_year == 2012 and args.end_year == 2022) else data['data']
    formatted_data = add_content(split_data)

    # Output.
    output = {'name': f'News_Category_Dataset_v3 with content ({args.start_year} - {args.end_year})','length': len(formatted_data) , 'data': formatted_data}
    out_path = os.path.join(args.out_dir, args.file_name)

    output_to_json(output, out_path, args.file_name)

if __name__ == '__main__':
    main()