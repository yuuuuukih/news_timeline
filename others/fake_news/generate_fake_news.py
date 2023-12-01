import os
import json
from get_gpt_basic_response import get_gpt_response
from argparse import ArgumentParser

def get_data_by_id(data_log, id):
    for item in data_log:
        if item['id'] == id:
            return item
    print(f"ID {id} is not found in the log.")
    return None

def main():
    parser = ArgumentParser()
    parser.add_argument('--model_name', default='gpt-4')
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/preprocessed/keywords/2019_2022/keywords.json')
    parser.add_argument('--id', default=0, type=int)
    args = parser.parse_args()

    # Open the dataset
    with open(args.file_path, 'r') as F:
        data = json.load(F)

    timeline = get_data_by_id(data['log'], args.id)

    system_content = (
        # "Please generate ONE fake news article following the given conditions.\n"
        # "The output should be a timeline that includes both the given articles and the generated fake news.\n"
        # "Please sort the timeline in ascending order based on the date.\n"
        f"I will provide you with {timeline['length']} articles related to {', '.join(timeline['keywords'])}.\n"
        "Please generate ONE fake news based on the following conditions from those articles.\n"
        "\n"
        "Conditions of fake news.\n"
        "- It needs to contain fake, headline, short_description, authors, date(YYYY-MM-DD), and content properties.\n"
        "- Set the fake property of the generated fake news to True.\n"
        # "- It smoothly connects to articles that is earlier in the timeline.\n"
        # "- It contradicts articles that comes later in the timeline.\n"
        f"The date of the fake news must be within a period that is later than the oldest date among the {timeline['length']} given articles and earlier than the newest date.\n"
        "- The article chronologically BEFORE the date of the fake news does not contradict and connects smoothly.\n"
        "- The article chronologically AFTER the date of the fake news clearly contradicts.\n"
    )

    user_content = ''
    for i, data in enumerate(timeline['data']):
        user_content += (
            f"fake: False\n"
            f"headline: {data['headline']}\n"
            f"short_description: {data['short_description']}\n"
            f"authors: {data['authors']}\n"
            f"date: {data['date']}\n"
            f"content: {data['content']}\n"
            "\n"
        )

    # print(system_content)
    # print(user_content)

    res = get_gpt_response(args.model_name, user_content, system_content)
    print(res)

if __name__ == '__main__':
    main()
