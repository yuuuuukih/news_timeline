import os
import json
import openai

from argparse import ArgumentParser

class FakeNewsGenerater():
    def __init__(self, timelines_for_certain_entity) -> None:
        self.timelines = timelines_for_certain_entity
        '''structure of timelines_for_certain_entity
        [
            {
                'story': xxx,
                'timeline': [
                    {
                        'ID': xxx,
                        'document': headline: short_description,
                        'headline': xxx,
                        'short_description': xxx,
                        'date': '0000-00-00',
                        'reason': xxx,
                    }, ...
                ]
            }, ...
        ]
        '''




def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/timeline_test_russia_ukraine.json.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/')
    parser.add_argument('--model_name', default='gpt-4')
    parser.add_argument('--temp', default=0.8, type=float)
    args = parser.parse_args()

if __name__ =='__main__':
    main()