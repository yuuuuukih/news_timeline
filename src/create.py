'''
Create dataset
'''

import os
import json
from argparse import ArgumentParser

from create_dataset.preprocess.preprocess import Preprocessor
from create_dataset.keyword_groups.get_keyword_groups import KeywordGroupsGetter
from create_dataset.timeline.generate_multiple_timelines import MultipleTimelineGenerator
from create_dataset.split.split_dataset import TimelinesSplitter
from create_dataset.fake_news.add_fake_news import FakeNewsGenerater, FakeNewsSetter

from create_dataset.type.entities import Entities
from create_dataset.type.no_fake_timelines import NoFakeTimeline
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
    '''
    For ALL
    '''
    parser.add_argument('--raw_file_path', default='/mnt/mint/hara/datasets/news_category_dataset/raw/News_Category_Dataset_v3.json')
    parser.add_argument('--root_dir', default='/mnt/mint/hara/datasets/news_category_dataset/dataset')
    '''
    For Preprocess
    '''
    parser.add_argument('--start_year', default=2019, type=int)
    parser.add_argument('--end_year', default=2022, type=int)
    '''
    For Keyword Groups
    '''
    # Hyper parameter
    parser.add_argument('--th', default=0.6, type=float, help='Threshold for bm25')
    parser.add_argument('--min_sup', default=0.003, type=float)
    parser.add_argument('--min_conf', default=0.6, type=float)
    parser.add_argument('--k1', default=1.2, type=float)
    # Preprocess
    parser.add_argument('--rm_stopwords', default=True, action='store_false')
    parser.add_argument('--lemmatize', default=True, action='store_false')
    parser.add_argument('--rm_single_char', default=True, action='store_false')
    parser.add_argument('--rm_non_noun_verb', default=False, action='store_true')
    parser.add_argument('--rm_non_noun', default=True, action='store_false')
    parser.add_argument('--rm_duplicates', default=True, action='store_false')
    parser.add_argument('--tfidf', default=False, action='store_true') #DEFAULT ONLY FALSE
    parser.add_argument('--bm25', default=True, action='store_false')
    # Comments for conditions
    parser.add_argument('--m', default='items >= 2', type=str)
    # Basically fixed
    parser.add_argument('--max_for_removed_words', default=20, type=int)
    # Others
    parser.add_argument('--table_show', default=False, action='store_true')
    '''
    For timeline
    '''
    parser.add_argument('--model_name', default='gpt-4')
    parser.add_argument('--temp', default=0.8, type=float, help='Temperature for 1st response of GPT.')
    parser.add_argument('--min_docs', default=4, type=int, help='min_docs_num_in_1timeline')
    parser.add_argument('--max_docs', default=10, type=int, help='max_docs_num_in_1timeline')
    parser.add_argument('--top_tl', default=0.5, type=float, help='top_tl: Number of timelines to be generated, relative to the number of timelines that can be generated.')
    parser.add_argument('--max_reexe_num', default=2, type=int)
    parser.add_argument('--start_entity_id', default=0, type=int)
    # For rouge score
    parser.add_argument('--judgement', default='diff', choices=['diff', 'rate', 'value'])
    parser.add_argument('--alpha', default=0.8, type=float)
    parser.add_argument('--th_1', default=0.25, type=float, help='Threshold for rouge-1')
    parser.add_argument('--th_2', default=0.12, type=float, help='Threshold for rouge-2')
    parser.add_argument('--th_l', default=0.15, type=float, help='Threshold for rouge-l')
    parser.add_argument('--th_2_rate', default=1.1, type=float, help='Threshold for the rate of rouge-2')
    parser.add_argument('--th_2_diff', default=0.007, type=float, help='Threshold for the difference of rouge-2')
    '''
    For split dataset
    '''
    parser.add_argument('--diff', default=7, type=int)
    parser.add_argument('--split_n', default=1, type=int)
    parser.add_argument('--do_not_save_split', default=True, action='store_false')
    '''
    For fake news
    '''
    parser.add_argument('--temp_for_fake_news', default=0.8, type=float)
    parser.add_argument('--setting', default='none', choices=FakeNewsSetter.get_choices())

    args = parser.parse_args()

    # Set the output directory
    out_dir = os.path.join(args.root_dir, f"diff{args.diff}")

    '''
    Preprocess
    '''
    # preprocessor = Preprocessor(args.raw_file_path, args.start_year, args.end_year)
    # preprocessed_data = preprocessor.get_preprocessed_data()
    # save_dataset(preprocessed_data, args.root_dir, 'preprocessed_data')

    # with open('/mnt/mint/hara/datasets/news_category_dataset/dataset/preprocessed_data.json', 'r') as F:
    #     preprocessed_data = json.load(F)

    '''
    Get keyword groups
    '''
    # kgg = KeywordGroupsGetter(
    #     preprocessed_data, args.th, args.min_sup, args.min_conf, args.k1,
    #     args.rm_stopwords, args.lemmatize, args.rm_single_char, args.rm_non_noun_verb, args.rm_non_noun, args.rm_duplicates, args.tfidf, args.bm25,
    #     args.m, args.max_for_removed_words, args.table_show
    # )
    # keyword_groups_data: Entities = kgg.get_keyword_groups()
    # save_dataset(keyword_groups_data, args.root_dir, 'keyword_groups')

    # with open('/mnt/mint/hara/datasets/news_category_dataset/dataset/keyword_groups.json', 'r') as F:
    #     keyword_groups_data: Entities = json.load(F)

    '''
    Generate timelines
    '''
    # mtg = MultipleTimelineGenerator(keyword_groups_data, args.model_name, args.temp, args.judgement, args.min_docs, args.max_docs, args.top_tl, args.start_entity_id)
    # mtg.set_max_reexe_num(args.max_reexe_num)
    # mtg.set_rouge_parms(args.alpha, args.th_1, args.th_2, args.th_l, args.th_2_rate, args.th_2_diff, rouge_used=True)
    # mtg.set_file_to_save(json_file_name='timeline_diff6', out_dir=out_dir)
    # mtg.generate_multiple_timelines()

    '''
    Split dataset
    '''
    # with open(os.path.join(out_dir, f"timeline_diff{args.diff}.json"), 'r') as F:
    #     timelines: NoFakeTimeline = json.load(F)

    # ts = TimelinesSplitter(timelines)
    # ts.set_split_n(args.split_n)
    # communities = ts.community()
    # com_info = ts.get_community_info(communities)
    # ts.get_split_dataset(com_info, out_dir, args.diff, args.min_docs, args.do_not_save_split)


    '''
    Add fake news
    '''
    for what in ['train', 'val', 'test']:
        print(what)
        with open(os.path.join(out_dir, f"{what}.json"), 'r') as F:
            no_fake_timelines: SplitDataset = json.load(F)

        fng = FakeNewsGenerater(no_fake_timelines, args.setting)
        fng.set_gpt_for_fake_news(args.model_name, args.temp_for_fake_news)
        fng.set_file_to_save(os.path.join(args.root_dir, f"diff{args.diff}_{args.setting}"), what)
        fng.generate_fake_news_timelines()

if __name__ == '__main__':
    main()
