'''
1. Process the raw news category dataset to json format.
2. Get the content of articles by scraping
'''

import json
import html
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

class Preprocessor:
    def __init__(self, raw_file_path: str, start_year: int, end_year: int) -> None:
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
        self.news_catedory_dataset = raw_file_path
        self.start_year = start_year
        self.end_year = end_year

        self._preprocess()

    # Formatting the dataset.
    def _format_json(self, file_path: str):
        data = [json.loads(line.strip()) for line in open(file_path)]
        print('Format completed.')
        return data

    # Add the year, month, day infomation as properties.
    def _add_time_info(self, data):
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

    # Scrape the article content by getting url
    def _scrape_article_content(self, url: str):
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
    def _add_content(self, data_list):
        formatted_data = []
        for d in tqdm(data_list):
            # Double quotes are obtained as "\".
            content = self._scrape_article_content(d['link'])

            new_d = d.copy()
            new_d['content'] = content
            formatted_data.append(new_d)
        print('Contents are added completely.')
        return formatted_data

    def _preprocess(self):
        formatted_data = self._format_json(self.news_catedory_dataset)
        data_without_content = self._add_time_info(formatted_data)
        split_data = [d for d in data_without_content if self.start_year <= int(d['year']) <= self.end_year] if not (self.start_year == 2012 and self.end_year == 2022) else data_without_content
        data_with_content = self._add_content(split_data)

        self.preprocessed_data = {
            'name': f'News_Category_Dataset_v3 with content ({self.start_year} - {self.end_year})',
            'length': len(data_with_content),
            'data': data_with_content
        }

    def get_preprocessed_data(self):
        return self.preprocessed_data
