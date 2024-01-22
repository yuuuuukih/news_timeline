import os
import sys
import json
import re
from datetime import datetime
from typing import Literal

from create_dataset.gpt.fakenews_gpt import FakenewsGPTResponseGetter
from create_dataset.utils.retry_decorator import retry_decorator
from create_dataset.utils.measure_exe_time import measure_exe_time

from create_dataset.type.no_fake_timelines import TimelineData, Doc
from create_dataset.type.fake_news_dataset import FakeNewsDataset, TimelineDataInfo, DocForDataset
from create_dataset.type.split_dataset import SplitDataset

from create_dataset.utils.update_occurrences import update_occurrences

class FakeNewsSetter:
    def __init__(self):
        self.choices = ['none', 'rep0', 'rep1','rep2','rep3', 'ins0', 'ins1', 'ins2']
        '''description
        - Strings in the first half: ['rep', 'ins']
            - 'rep': means repracing method.
            - 'ins': means inserting method.
        - Numbers in the second half: ['0', '1', '2', '3']
            - '0': means no condition about contradictions.
            - '1': means don't contradict earlier documents but contradict a later document.
            - '2': means contradict any one document.
            - '3': means contradict the original document before replacement (only replacing).
        - Others
            - 'none': means no setting.
        '''

    @classmethod
    def get_choices(cls) -> list:
        instance = cls()
        return instance.choices

    @classmethod
    def decode(cls, setting: Literal['none', 'rep0', 'rep1','rep2','rep3', 'ins0', 'ins1', 'ins2']) -> tuple:
        instance = cls()
        if not setting in instance.choices:
            sys.exit('This setting does not exist.')
        elif setting == 'none':
            sys.exit('NO setting.')
        else:
            return setting.rstrip('0123456789'), setting.lstrip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') # ex: ('rep', '0')

class FakeNewsGenerater(FakenewsGPTResponseGetter):
    def __init__(self, no_fake_timelines: SplitDataset, setting: Literal['none', 'rep0', 'rep1','rep2','rep3', 'ins0', 'ins1', 'ins2']) -> None:
        self.no_fake_timelines = no_fake_timelines
        self.data = no_fake_timelines['data']
        # self.data = no_fake_timelines['data'][0:1]
        self.m = len(self.data)
        self.setting = setting
        self.setting_str, self.setting_num = FakeNewsSetter.decode(setting)

    def get_prompts(self, entity_items: list[str], timeline_data: TimelineData, fake_news_position: int = 3, content_words: int = 200):
        docs_num, timeline = timeline_data['docs_num'], timeline_data['timeline']
        timeline = sorted(timeline, key=lambda x: x['date'])
        posi = fake_news_position - 1
        def _doc_template(doc: Doc, with_content: bool = True):
            template = (
                f"document ID. {doc['ID']}\n"
                f"headline: {doc['headline']}\n"
                f"short_description: {doc['short_description']}\n"
                f"date: {doc['date']}\n"
            )
            if with_content:
                template += f"content: {doc['content']}\n"
            return template

        '''
        system content
        '''
        system_content_1st = "You are a logical writer. You must execute the function calling's format_fakenews_1st_step function to format your outputs."
        system_content_2nd = "You are a logical writer. You must execute the function calling's format_fakenews_2nd_step function to format your outputs."

        '''
        user content (1st step)
        '''
        user_content_1 = (
            "# INSTRUCTIONS\n"
            f"Below are {docs_num} documents about {entity_items}. Each document contains time information (YYYY-MM-DD), forming a timeline.\n"
            "You must generate ONE fake news in two steps based on the following constraints and input documents.\n"
            "There needs to be two documents ahead and one behind the fake news."
            f"First of all, please tell me which position from the front is optimal for generating fake news while satisfying the following conditions, and please return that position as a number (3~{len(timeline)-1}).\n"
        )

        user_content_1 += "# INPUT DOCUMENTS\n"
        for i, doc in enumerate(timeline):
            user_content_1 += _doc_template(doc)

        user_content_1 += (
            "# CONSTRAINTS\n"
            f"- The date of the fake news must be within a period that is later than the oldest date among the {docs_num} documents and earlier than the newest date.\n"
            "- The fake news that is generated needs to be temporally consistent and naturally connected with the two documents that precede it.\n"
        )

        '''
        user content (2nd step)
        '''
        user_content_2 = (
            "# INSTRUCTIONS\n"
            "Generate ONE fake news based on the following constraints and input documents by following criteria:\n"
            f"- It needs to contain headline, short_description, date (YYYY-MM-DD), and content properties, and please strictly adhere to around {content_words} words for the content you generate.\n"
            "- Additionally, explain how the fake news contradicts the real ones.\n"
            "\n"
        )

        if self.setting_num == '0':
            pass
        elif self.setting_num == '1':
            user_content_1 += f"- The fake news you generate should clearly contradict the subsequent document.\n"
            user_content_2 += (
                "- However, ensure that the fake news you generate clearly contradicts the following document.\n"
                f"{_doc_template(timeline[posi+1])}\n"
            )
        elif self.setting_num == '2':
            # user_content += f"- The fake news you generate should clearly contradict with any documents in the timeline.\n"
            pass
        elif self.setting_num == '3':
            user_content_1 += f"- The fake news you generate should clearly contradict the original document before replacement.\n"
            user_content_2 += (
                "## criteria1: Ensure that the headline and content of the fake news you generate are contradict to headline and content of the following document."
                f"{_doc_template(timeline[posi])}\n"
            )
        else:
            sys.exit("Setting Error! You can choose '0' or '1' or '2' or '3'.")

        if self.setting_str == 'rep':
            user_content_1 += (
                "- The fake news is integrated into the timeline by replacing a single document.\n"
            )
            user_content_2 += (
                "## criteria2: Please generate fake news that is a possible consequence of the following two documents.\n"
                f"{_doc_template(timeline[posi-2], with_content=False)}\n"
                f"{_doc_template(timeline[posi-1], with_content=False)}\n"
                f"- The date of the fake news you generate should be {timeline[posi]['date']}.\n"
            )

        elif self.setting_str == 'ins':
            # user_content += f"- Please generate fake news to be inserted in the most suitable location in the timeline I have entered.\n"
            # f"- To avoid any contradictions, please ensure the date of the fake news should be set between {timeline[posi-1]['date']}, and {timeline[posi+1]['date']}."
            pass
        else:
            sys.exit("Setting Error! You can choose 'rep' or 'ins'.")

        return system_content_1st, user_content_1, system_content_2nd, user_content_2

    def set_gpt_for_fake_news(self, model_name, temp):
        self.__model_name = model_name
        self.__temp = temp

    @retry_decorator(max_error_count=50, retry_delay=1)
    def get_fake_news(self, entity_items: list[str], timeline_data: TimelineData) -> DocForDataset:
        # Generate fake news
        # 1st step
        system_content_1, user_content_1, _, _ = self.get_prompts(entity_items, timeline_data)
        messages_1st = [
            {'role': 'system', 'content': system_content_1},
            {'role': 'user', 'content': user_content_1}
        ]
        for _ in range(30):
            position: int = self.get_gpt_response_fakenews_1st_step(messages_1st, self.__model_name, self.__temp)
            print(f"position: {position}, len: {len(timeline_data['timeline'])}")
            if 3 <= position <= len(timeline_data['timeline'])-1:
                self.position = position - 1
                break

        # 2nd step
        _, _, system_content_2, user_content_2 = self.get_prompts(entity_items, timeline_data, fake_news_position=position)
        messages_2nd = [
            {'role': 'system', 'content': system_content_2},
            {'role': 'user', 'content': user_content_2}
        ]
        fake_news: DocForDataset = self.get_gpt_response_fakenews_2nd_step(messages_2nd, self.__model_name, self.__temp)

        return fake_news

    @measure_exe_time
    def generate_fake_news_timelines(self):
        for i, entity_info in enumerate(self.data):
            entity_id = entity_info['entity_ID']
            entity_items = entity_info['entity_items']
            timelines = entity_info['timeline_info']['data']
            timeline_num = len(timelines)

            print(f"=== {i+1}/{self.m}. entity: {entity_items} START ===")
            for j, timeline_data in enumerate(timelines):
                print(f"=== {j+1}/{timeline_num}. fake news generating... ===")
                # Create a new timeline
                new_timeline: list[DocForDataset] = []
                for doc in timeline_data['timeline']:
                    new_doc: DocForDataset = {
                        'ID': doc['ID'],
                        'is_fake': doc['is_fake'],
                        'headline': doc['headline'],
                        'short_description': doc['short_description'],
                        'date': doc['date'],
                        'content': doc['content']
                    }
                    new_timeline.append(new_doc)

                # Generate fake news
                for _ in range(30):
                    fake_news = self.get_fake_news(entity_items, timeline_data)
                    try:
                        if (self.is_valid_date_format(fake_news['date'])
                            and 150<len(fake_news['content'].split())<250):
                            prev_date = datetime.strptime(timeline_data['timeline'][self.position-1]['date'], '%Y-%m-%d')
                            next_date = datetime.strptime(timeline_data['timeline'][self.position+1]['date'], '%Y-%m-%d')
                            fake_date = datetime.strptime(fake_news['date'], '%Y-%m-%d')

                            if prev_date < fake_date < next_date:
                                break
                        else:
                            print(f"Invalid output (content len = {len(fake_news['content'].split())}). Retry...")
                    except Exception as e:
                        print(f"Exception Error: {e}")
                        print("Retry...")
                        continue
                else:
                    sys.exit('fake news generation error!')

                if self.setting_str == 'rep':
                    replaced_doc = new_timeline[self.position]
                    replaced_document_id = replaced_doc['ID']
                    new_timeline = list(filter(lambda doc: doc['ID'] != replaced_document_id, new_timeline))

                elif self.setting_str == 'ins':
                    replaced_doc = None

                new_timeline.append(fake_news)
                new_timeline = sorted(new_timeline, key=lambda doc: doc['date'])

                new_timeline_info: TimelineDataInfo = {
                    'entity_id': entity_id,
                    'entity_items': entity_items,
                    'replaced_doc': replaced_doc,
                    'timeline': new_timeline
                }

                self.save_fake_news_dataset(new_timeline_info)

                print(f"=== {j+1}/{timeline_num}. fake news DONE ===")

    def is_valid_date_format(self, date_string):
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        match = re.match(pattern, date_string)
        return bool(match)

    def set_file_to_save(self, out_dir, json_file_name):
        self.__json_file_name = json_file_name
        self.__out_dir = out_dir

    def save_fake_news_dataset(self, new_timeline_info: TimelineDataInfo, name_to_save='Data'):
        # Open the file
        file_path = os.path.join(self.__out_dir, f"{self.__json_file_name}.json")
        try:
            with open(file_path, 'r', encoding='utf-8') as F:
                fake_news_dataset: FakeNewsDataset = json.load(F)
        except FileNotFoundError:
            fake_news_dataset: FakeNewsDataset = {
                'name': self.__json_file_name,
                'description': 'Timeline dataset with fake news.',
                'setting': self.setting,
                'docs_num_in_1_timeline': {},
                'no_fake_timelines_info': {
                    'entities_num': self.no_fake_timelines['entities_num'],
                    'timeline_num': self.no_fake_timelines['timelines_num'],
                    'split_n': self.no_fake_timelines['split_n'],
                    'setting': self.no_fake_timelines['setting'],
                },
                'data': []
            }
        # Update
        fake_news_dataset['data'].append(new_timeline_info)
        fake_news_dataset['docs_num_in_1_timeline'] = update_occurrences(fake_news_dataset['docs_num_in_1_timeline'], [len(new_timeline_info['timeline'])])

        # save the json file.
        with open(file_path, 'w', encoding='utf-8') as F:
            json.dump(fake_news_dataset, F, indent=4, ensure_ascii=False, separators=(',', ': '))
            print(f'{name_to_save} is saved to {self.__json_file_name}.json')
