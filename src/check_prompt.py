import os
import json
from create_dataset.fake_news.add_fake_news import FakeNewsGenerater

def main():
    root_dir = '/mnt/mint/hara/datasets/news_category_dataset/dataset/diff7/train.json'
    with open(root_dir, 'r') as F:
        no_fake_timelines = json.load(F)

    fake_news_generater = FakeNewsGenerater(no_fake_timelines=no_fake_timelines, setting='rep3')
    which_entity = 159
    prompts = fake_news_generater.get_prompts( no_fake_timelines['data'][which_entity]['entity_items'], no_fake_timelines['data'][which_entity]['timeline_info']['data'][-1])
    print(prompts[3])

if __name__ == '__main__':
    main()