import os
import sys
import json
import openai

from argparse import ArgumentParser

from get_gpt_response import GPTResponseGetter

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
    def decode(cls, setting: str) -> tuple:
        instance = cls()
        if not setting in instance.choices:
            sys.exit('This setting does not exist.')
        elif setting == 'none':
            sys.exit('NO setting.')
        else:
            return setting.rstrip('0123456789'), setting.lstrip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') # ex: ('rep', '0')


class FakeNewsGenerater(GPTResponseGetter):
    def __init__(self, no_fake_timelines, setting) -> None:
        self.no_fake_timelines = no_fake_timelines
        self.data = no_fake_timelines['data']
        self.setting_str, self.setting_num = FakeNewsSetter.decode(setting)

    def get_prompts(self, entity, timeline_data):
        docs_num, timeline = timeline_data['docs_num'], timeline_data['timeline']
        timeline = sorted(timeline, key=lambda x: x['date'])

        '''
        system content
        '''
        system_content = "You are a logical writer."

        '''
        user content
        '''
        user_content = (
            "# INSTRUCTIONS\n"
            f"Below are {docs_num} documents about {entity}. Each document contains time information (YYYY-MM-DD), forming a timeline.\n"
            "Generate ONE fake news based on the following constraints and input documents.\n"
        )

        user_content += "# INPUT DOCUMENTS\n"
        for i, doc in enumerate(timeline_data):
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
            "- In a step-by-step manner, first generate the content and date of fake news, and then generate the headline and short description."
            f"- The date of the fake news must be within a period that is later than the oldest date among the {docs_num} documents and earlier than the newest date.\n"
        )
        if self.setting_str == 'rep':
            user_content += (
                f"- Please generate fake news by replacing a suitable one among the {docs_num} documents included in the timeline I have entered.\n"
                f"- Please generat the document id and headline of the document to be replaced as remarks."
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
                "- The fake news you generate should not contradict with ealier documents and should connect smmothly and logically.\n"
                "- However, the fake news you generate should clearly contradict the later documents.\n"
            )
        elif self.setting_num == '2':
            user_content += f"- The fake news you generate should clearly contradict with any documents in the timeline.\n"
        elif self.setting_num == '3':
            user_content += f"- The fake news you generate should clearly contradict the original document before replacement.\n"
        else:
            sys.exit("Setting Error! You can choose '0' or '1' or '2' or '3'.")

        return system_content, user_content

    



def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/no_fake_timelines.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/')
    parser.add_argument('--setting', default='none', choices=FakeNewsSetter.get_choices())
    args = parser.parse_args()

    with open(args.file_path, 'r') as F:
        no_fake_timelines = json.load(F)

    fng = FakeNewsGenerater(no_fake_timelines, args.setting)

if __name__ =='__main__':
    main()