import os
import sys
import openai

import json
from argparse import ArgumentParser

class TimelineGenerater:
    def __init__(self, entity_info, model_name, temp, docs_num=10) -> None:
        self.entity_info_left = entity_info
        '''structure of entity_info
        {
            "freq": xxx,
            "items": ["xxx", ...],
            "ID": 0,
            "docs_info": {
                "IDs": [],
                "docs": [
                    {
                        "link": xxx,
                        "headline": xxx,
                        "category": xxx,
                        "short_description": xxx,
                        "authors": xxx,
                        "date": xxx,
                        "year": xxx,
                        "month": xxx,
                        "day": xxx,
                        "content": xxx,
                        "ID": xxx,
                        "preprocessed_tokens": [
                            "xxx",
                            ...
                        ],
                        "entities_info": {
                            "num": xxx,
                            "IDs": [],
                            "entities": []
                        }
                    },
                    ...
                ]
            }
        },
        '''

        # parameters
        self.model_name = model_name
        self.temp = temp
        self.docs_num = docs_num
        # timeline
        self.timelines = []

    # Setting the prompts
    def get_prompts(self, entity_info):
        '''
        system content
        '''
        system_content = 'You are a professional story writer.'

        '''
        user content 1
        '''
        user_content_1 = (
            "# INSTRUCTIONS\n"
            "Generate the best story based on the following constraints and input statements.\n"

            "# CONSTRAINTS\n"
            f"- Generate stories based on the {entity_info['freq']} documents (consisting of headline and short description) in the INPUT STATEMENTS below.\n"
            f"- The story must be about {', '.join(entity_info['items'])}.\n"
            "- It must be less than 100 words.\n"

            "# INPUT STATEMENTS\n"
            # "Document ID. headline: short description"
        )
        for doc in entity_info['docs_info']['docs']:
            doc_ID, headline, short_description = doc['ID'], doc['headline'], doc['short_description']
            user_content_1 += f"Document ID -> {doc_ID}, documents -> {headline}: {short_description}\n"
            # user_content_1 += f"{doc_ID}. {headline}: {short_description}\n"
        user_content_1 += "# OUTPUT STORY\n"

        '''
        user content 2
        '''
        user_content_2 = (
            f"Pick {self.docs_num} documents that are most relevant to the above story.\n"
            "When responding, generate the Document ID, the headline: short_description of the document, and which sentence in the story the document is most related to.\n"
            "Generate in the following format.\n"
        )

        return system_content, user_content_1, user_content_2

    # Get gpt response
    def get_gpt_response(self, messages: list, functions=[], model_name='gpt-4', temp=1.0):
        openai.organization = os.environ['OPENAI_KUNLP']
        openai.api_key = os.environ['OPENAI_API_KEY_TIMELINE']

        if len(functions) == 0:
            response = openai.ChatCompletion.create(
                model=model_name,
                temperature=temp,
                messages=messages
            )
        else:
            response = openai.ChatCompletion.create(
                model=model_name,
                temperature=temp,
                messages=messages,
                functions=functions,
                function_call='auto'
            )

        response_message = response['choices'][0]['message']
        assistant_message = {'role': 'assistant', 'content': response_message['content']}
        messages.append(assistant_message)

        if not response_message.get('function_call'):
            return messages
        else:
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "fortmat_timeline": self.fortmat_timeline,
            }
            function_name = response_message['function_call']['name']
            function_to_call = available_functions[function_name]
            function_args = json.loads(response_message['function_call']['arguments'])
            function_response = function_to_call(
                IDs=function_args.get('IDs'),
                documents=function_args.get('documents'),
                reasons=function_args.get('reasons'),
            )
            return function_response

    # For function calling
    def fortmat_timeline(self, IDs: list[int], documents: list[str], reasons: list[str]):
        if not (len(IDs) == len(documents) == len(reasons) == self.docs_num):
            print(f"IDs: {IDs}")
            print(f"documents: {documents}")
            print(f"reasons: {reasons}")
            sys.exit('Input ERROR!')
            return None
        else:
            timeline = []
            for i in range(self.docs_num):
                # get_doc_by_id = lambda id: next((f"{item['headline']}: {item['short_description']}" for item in self.entity_info_left['docs_info']['docs'] if item['ID'] == id), None)
                get_doc_info_by_id = lambda id: next((item for item in self.entity_info_left['docs_info']['docs'] if item['ID'] == id), None)
                doc = {'ID': IDs[i], 'document': get_doc_info_by_id(IDs[i]), 'reason': reasons[i]}

                # Check
                # if documents[i] != get_doc_by_id(IDs[i]):
                #     print(f"ID: {IDs[i]}")
                #     print(f"generated doc: {documents[i]}")
                #     print(f"raw_doc: {get_doc_by_id(IDs[i])}")

                timeline.append(doc)
            return timeline, IDs

    def format_timeline_info(self):
        function_info = {
            'name': 'fortmat_timeline',
            'description': 'Convert the generated timeline information into a dictionary type.',
            'parameters': {
                # https://json-schema.org/understanding-json-schema/reference/array
                'type': 'object',
                'properties': {
                    'IDs': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': 'A list of Document ID.'
                    },
                    'documents': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    },
                    'reasons': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                },
                'required': ['IDs', 'documents', 'reasons']
            },
        }
        return function_info

    def _remove_dicts_by_id(self, dictionary_list, id_list):
        # Find the indexes of dictionaries with IDs to be removed
        indexes_to_remove = [i for i, item in enumerate(dictionary_list) if item['ID'] in id_list]
        # Create a new list without the dictionaries at the identified indexes
        filtered_list = [item for i, item in enumerate(dictionary_list) if i not in indexes_to_remove]
        return filtered_list

    def _check_timeline(self, entity_info, IDs_from_gpt):
        # Check document ID
        if not set(IDs_from_gpt) <= set(entity_info['docs_info']['IDs']):
            sys.exit('ID ERROER!')

    def generate_story_and_timeline(self):
        entity_info = self.entity_info_left
        # prompts
        system_content, user_content_1, user_content_2 = self.get_prompts(entity_info)
        # messages
        messages=[
            {'role': 'system', 'content': system_content},
            {'role': 'user', 'content': user_content_1}
        ]
        messages = self.get_gpt_response(messages, model_name=self.model_name, temp=self.temp)
        story = messages[-1]['content']
        print('Got 1st GPT response.')

        messages.append({'role': 'user', 'content': user_content_2})
        timeline_list, IDs_from_gpt = self.get_gpt_response(messages, model_name=self.model_name, temp=0, functions=[self.format_timeline_info()])
        print('Got 2nd GPT response.')

        # Check
        self._check_timeline(entity_info, IDs_from_gpt)

        # Update timelines
        timeline_info = {
            'story': story,
            'timeline': timeline_list
        }
        self.timelines.append(timeline_info)

        # Update entity info left
        self.entity_info_left['docs_info'] = {
            'IDs': list(set(entity_info['docs_info']['IDs']) - set(IDs_from_gpt)),
            'docs': self._remove_dicts_by_id(entity_info['docs_info']['docs'], IDs_from_gpt)
        }
        self.entity_info_left['freq'] = len(self.entity_info_left['docs_info']['IDs'])

    def generate_timelines(self):
        cnt = 1
        while self.entity_info_left['freq'] >= self.docs_num:
            print(f'=== {cnt}. START ===')
            self.generate_story_and_timeline()
            print(f'=== {cnt}. DONE ===')
            cnt += 1


def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/entities.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/')
    parser.add_argument('--model_name', default='gpt-4')
    parser.add_argument('--temp', default=0.8, type=float)
    args = parser.parse_args()

    with open(args.file_path, 'r') as F:
        entities_data = json.load(F)

    # Test ['russia', 'ukraine']
    entity_info = entities_data['data'][0]['entities']['list'][236]
    print(entity_info['docs_info']['IDs'])

    tg = TimelineGenerater(entity_info, args.model_name, args.temp)
    tg.generate_timelines()
    timelines = tg.timelines
    print('\n')
    # print(timelines)

    # save the json file.
    file_name = 'timeline_test_' + '_'.join(entity_info['items'])
    data_json = os.path.join(args.out_dir, f'{file_name}.json')
    with open(data_json, 'w', encoding='utf-8') as json_file:
        json.dump(timelines, json_file, indent=4, ensure_ascii=False, separators=(',', ': '))
        print(f'Data is saved to {file_name}.json')



if __name__ == '__main__':
    main()