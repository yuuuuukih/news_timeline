import os
import sys
import openai
import json

class GPTResponseGetter:
    # def __init__(self):
        # For function calling

    # Get gpt response
    def get_gpt_response(self, messages: list, model_name='gpt-4', temp=1.0):
        openai.organization = os.environ['OPENAI_KUNLP']
        openai.api_key = os.environ['OPENAI_API_KEY_TIMELINE']

        response = openai.ChatCompletion.create(
            model=model_name,
            temperature=temp,
            messages=messages,
            functions=[
                self._format_timeline_info()
            ],
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

    '''
    === For function calling ===
    '''
    # format timeline
    def set_docs_num_in_1timeline(self, value):
        # self.__dict__['__docs_num_in_1timeline'] = value
        self.__docs_num_in_1timeline = value

    def fortmat_timeline(self, IDs: list[int], documents: list[str], reasons: list[str]):
        if not (len(IDs) == len(documents) == len(reasons) == self.__docs_num_in_1timeline):
            print(f"IDs: {IDs}")
            print(f"documents: {documents}")
            print(f"reasons: {reasons}")
            sys.exit('Input ERROR!')
            return None
        else:
            timeline = []
            for i in range(self.__docs_num_in_1timeline):
                doc_ID = IDs[i]
                # get_doc_by_id = lambda id: next((f"{item['headline']}: {item['short_description']}" for item in self.entity_info_left['docs_info']['docs'] if item['ID'] == id), None)
                get_doc_info_by_id = lambda: next((item for item in self.entity_info_left['docs_info']['docs'] if item['ID'] == doc_ID), None)
                doc_info_dict = get_doc_info_by_id()
                headline, short_description, date, content = doc_info_dict['headline'], doc_info_dict['short_description'], doc_info_dict['date'], doc_info_dict['content']
                # doc = {'ID': IDs[i], 'document': get_doc_info_by_id(), 'reason': reasons[i]}
                doc = {
                    'ID': IDs[i],
                    'document': f"{headline}: {short_description}",
                    'headline': headline,
                    'short_Description': short_description,
                    'date': date,
                    # 'content': content,
                    'reason': reasons[i]
                }

                # Check
                # if documents[i] != get_doc_by_id(doc_ID):
                #     print(f"ID: {doc_ID}")
                #     print(f"generated doc: {documents[i]}")
                #     print(f"raw_doc: {get_doc_by_id(doc_ID)}")

                timeline.append(doc)
            return timeline, IDs

    def _format_timeline_info(self):
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
