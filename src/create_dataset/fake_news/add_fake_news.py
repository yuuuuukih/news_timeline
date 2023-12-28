import os
import sys
import json
import re
from typing import Tuple, Union, Literal

from create_dataset.timeline.get_gpt_response import GPTResponseGetter
from create_dataset.utils.retry_decorator import retry_decorator
from create_dataset.utils.measure_exe_time import measure_exe_time

from create_dataset.type.no_fake_timelines import TimelineData
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

class FakeNewsGenerater(GPTResponseGetter):
    def __init__(self, no_fake_timelines: SplitDataset, setting: Literal['none', 'rep0', 'rep1','rep2','rep3', 'ins0', 'ins1', 'ins2']) -> None:
        self.no_fake_timelines = no_fake_timelines
        # self.data = no_fake_timelines['data']
        self.data = no_fake_timelines['data'][:5]
        self.m = len(self.data)
        self.setting = setting
        self.setting_str, self.setting_num = FakeNewsSetter.decode(setting)

    def get_prompts_for_fakenews(self, entity_items: list[str], timeline_data: TimelineData):
        docs_num, timeline = timeline_data['docs_num'], timeline_data['timeline']
        timeline = sorted(timeline, key=lambda x: x['date'])

        '''
        system content
        '''
        system_content = "You are a logical writer. You must execute the function calling's format_fake_news function to format your outputs."

        '''
        user content
        '''
        user_content = (
            "# INSTRUCTIONS\n"
            f"Below are {docs_num} documents about {entity_items}. Each document contains time information (YYYY-MM-DD), forming a timeline.\n"
            "Generate ONE fake news in about 200 words based on the following constraints and input documents.\n"
        )

        user_content += "# INPUT DOCUMENTS\n"
        for i, doc in enumerate(timeline):
            user_content += (
                f"document ID. {doc['ID']}\n"
                f"headline: {doc['headline']}\n"
                f"short_description: {doc['short_description']}\n"
                f"date: {doc['date']}\n"
                f"content: {doc['content']}\n"
            )


        user_content += (
            "# CONSTRAINTS\n"
            "- It needs to contain headline, short_description, date (YYYY-MM-DD), and content properties.\n"
            "- In a step-by-step manner, first generate the content and date of fake news, and then generate the headline and short description.\n"
            "- Additionally, explain why you generate such fake news and which parts of the fake news meet the following constraints.\n"
            f"- The date of the fake news must be within a period that is later than the oldest date among the {docs_num} documents and earlier than the newest date.\n"
        )
        if self.setting_str == 'rep':
            user_content += (
                f"- Please generate fake news by replacing a suitable one among the {docs_num} documents included in the timeline I have entered.\n"
                f"- Please generate the document id and headline of the document to be replaced as remarks.\n"
            )
        elif self.setting_str == 'ins':
            user_content += f"- Please generate fake news to be inserted in the most suitable location in the timeline I have entered.\n"
        else:
            sys.exit("Setting Error! You can choose 'rep' or 'ins'.")

        if self.setting_num == '0':
            pass
        elif self.setting_num == '1':
            user_content += (
                # "- The documents chronologically BEFORE the date of the fake news does not contradict and connects smoothly.\n"
                # "- The documents chronologically AFTER the date of the fake news clearly contradicts.\n"
                "- The fake news you generate should not contradict with ealier documents and should connect smoothly and logically.\n"
                "- However, the fake news you generate should clearly contradict the later documents.\n"
            )
        elif self.setting_num == '2':
            user_content += f"- The fake news you generate should clearly contradict with any documents in the timeline.\n"
        elif self.setting_num == '3':
            user_content += f"- The fake news you generate should clearly contradict the original document before replacement.\n"
        else:
            sys.exit("Setting Error! You can choose '0' or '1' or '2' or '3'.")

        return system_content, user_content

    def set_gpt_for_fake_news(self, model_name, temp):
        self.__model_name = model_name
        self.__temp = temp

    @retry_decorator(max_error_count=10, retry_delay=1)
    def get_fake_news(self, entity_items: list[str], timeline_data: TimelineData) -> Tuple[DocForDataset, Union[str, None]]:
        system_content, user_content = self.get_prompts_for_fakenews(entity_items, timeline_data)
        messages = [
            {'role': 'system', 'content': system_content},
            {'role': 'user', 'content': user_content}
        ]
        # Generate fake news
        fake_news, remarks = self.get_gpt_response_fake_news(messages, self.__model_name, self.__temp)

        return fake_news, remarks

    @measure_exe_time
    def generate_fake_news_timelines(self):

        self.init_tokens_for_fakenews()

        for i, entity_info in enumerate(self.data):
            entity_id = entity_info['entity_ID']
            entity_items = entity_info['entity_items']
            timelines = entity_info['timeline_info']['data']
            timeline_num = len(timelines)

            print(f"=== {i+1}/{self.m}. entity: {entity_items} START ===")
            for j, timeline_data in enumerate(timelines):
                print(f"=== {j+1}/{timeline_num}. fake news generating... ===")
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

                if self.setting_str == 'rep':
                    for _ in range(30):
                        fake_news, remarks = self.get_fake_news(entity_items, timeline_data)
                        if remarks != None and self.is_valid_date_format(fake_news['date']):
                            break
                    else:
                        sys.exit('fake news generation error!')
                    print(remarks)
                    replaced_document_id = remarks['document_id']
                    new_timeline = list(filter(lambda doc: doc['ID'] != replaced_document_id, new_timeline))

                elif self.setting_str == 'ins':
                    for _ in range(30):
                        fake_news, remarks = self.get_fake_news(entity_items, timeline_data)
                        if remarks == None:
                            break
                    else:
                        sys.exit('fake news generation error!')

                # new_timeline.append(fake_news)
                # new_timeline = sorted(new_timeline, key=lambda doc: doc['date'])
                self.len_of_fakenews.append(len(fake_news['content'].split()))

                # new_timeline_info: TimelineDataInfo = {
                #     'entity_id': entity_id,
                #     'entity_items': entity_items,
                #     'timeline': new_timeline
                # }

                # self.save_fake_news_dataset(new_timeline_info)

                print(f"=== {j+1}/{timeline_num}. fake news DONE ===")

        self.calc_ave_tokens_for_fakenews()
        self.get_ave_len_of_fakenews()

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
