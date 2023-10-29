import sys
from typing import TypedDict

from get_gpt_response import GPTResponseGetter

class TimelineSetter(GPTResponseGetter):
    '''
    docs_num_in_1timeline: The number of documents contained in ONE timeline,
    top_tl: Number of timelines to be generated, relative to the number of timelines that can be generated.
    '''
    def __init__(self, model_name, temp, docs_num_in_1timeline=10, top_tl=0.5):
        # super
        # super.__init__()
        # parameters
        self.model_name = model_name
        self.temp = temp
        self.docs_num_in_1timeline = docs_num_in_1timeline
        self.top_tl = top_tl

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
            f"Pick {self.docs_num_in_1timeline} documents that are most relevant to the above story.\n"
            "When responding, generate the Document ID, the headline: short_description of the document, and which sentence in the story the document is most related to.\n"
            "Generate in the following format.\n"
        )

        return system_content, user_content_1, user_content_2

    def _delete_dicts_by_id(self, dictionary_list, id_list):
        # Find the indexes of dictionaries with IDs to be removed
        indexes_to_remove = [i for i, item in enumerate(dictionary_list) if item['ID'] in id_list]
        # Create a new list without the dictionaries at the identified indexes
        filtered_list = [item for i, item in enumerate(dictionary_list) if i not in indexes_to_remove]
        return filtered_list

    def _check_timeline(self, entity_info, IDs_from_gpt):
        # Check document ID
        if not set(IDs_from_gpt) <= set(entity_info['docs_info']['IDs']):
            sys.exit('ID ERROER!')


    def generate_story_and_timeline(self, entity_info):
        # setter for GPTResponseGetter
        self.set_docs_num_in_1timeline(self.docs_num_in_1timeline)
        self.set_entity_info(entity_info)

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
        timeline_list, IDs_from_gpt = self.get_gpt_response(messages, model_name=self.model_name, temp=0)
        print('Got 2nd GPT response.')

        # Check
        self._check_timeline(entity_info, IDs_from_gpt)

        # Update timelines
        timeline_info = {
            'story': story,
            'timeline': timeline_list
        }

        return timeline_info, IDs_from_gpt

    def generate_timelines(self, entity_info_left: dict, timeline_num: int) -> list:
        entity_ID, entity_items = entity_info_left['ID'], entity_info_left['items']
        list_to_save_timelines = []
        docs_IDs = []
        for i in range(timeline_num):
            print(f'=== {i+1}/{timeline_num}. START ===')

            timeline_info, IDs_from_gpt = self.generate_story_and_timeline(entity_info_left)
            list_to_save_timelines.append(timeline_info)
            docs_IDs.extend(IDs_from_gpt)

            # Update entity info left
            entity_info_left['docs_info'] = {
                'IDs': list(set(entity_info_left['docs_info']['IDs']) - set(IDs_from_gpt)),
                'docs': self._delete_dicts_by_id(entity_info_left['docs_info']['docs'], IDs_from_gpt)
            }
            entity_info_left['freq'] = len(entity_info_left['docs_info']['IDs'])

            print(f'=== {i+1}/{timeline_num}. DONE ===')

        output_data = {
            'entity_ID': entity_ID,
            'entity_items': entity_items,
            'docs_info': {
                'IDs': docs_IDs
            },
            'timeline_info': {
                'timeline_num': timeline_num,
                'data': list_to_save_timelines
            }
        }

        return output_data
