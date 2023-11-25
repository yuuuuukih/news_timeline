import os
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
            request_timeout=60,
            functions=[
                # self._format_timeline_info(),
                self._format_fake_news_info(),
            ],
            function_call='auto'
        )

        response_message = response['choices'][0]['message']
        assistant_message = {'role': 'assistant', 'content': response_message['content']}
        messages.append(assistant_message)

        if not response_message.get('function_call'):
            print('No function calling (get_gpt_response.py).')
            return messages
        else:
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "fortmat_timeline": self.fortmat_timeline,
                "format_fake_news": self.format_fake_news,
            }
            function_name = response_message['function_call']['name']
            print(f"Called function in get_gpt_response.py: {function_name}")
            function_to_call = available_functions[function_name]
            try:
                function_args = json.loads(response_message['function_call']['arguments'])
            except json.decoder.JSONDecodeError as e:
                print(f"json.decoder.JSONDecodeError: {e}")
                print(response_message['function_call']['arguments'])

            if function_name == "fortmat_timeline":
                function_response, IDs_from_gpt = function_to_call(
                    number=function_args.get('number'),
                    IDs=function_args.get('IDs'),
                    reasons=function_args.get('reasons'),
                )
                return function_response, IDs_from_gpt

            elif function_name == 'format_fake_news':
                function_response = function_to_call(
                    headline=function_args.get('headline'),
                    short_description=function_args.get('short_description'),
                    date=function_args.get('date'),
                    content=function_args.get('content'),
                    remarks=function_args.get('remarks') or None
                )
                fake_news, remarks = function_response
                return fake_news, remarks

    '''
    === For function calling ===
    '''
    # format timeline
    def set_docs_num_in_1timeline(self, value):
        # self.__dict__['__docs_num_in_1timeline'] = value
        self.__docs_num_in_1timeline = value

    def set_entity_info(self, value):
        self.__entity_info = value

    def fortmat_timeline(self, number, IDs: list[int], reasons: list[str]):
        self.set_docs_num_in_1timeline(number)
        if not (len(IDs) == len(reasons) == self.__docs_num_in_1timeline):
            print(f"number: {number}")
            print(f"IDs: {IDs}")
            print(f"reasons: {reasons}")
            print('Input ERROR!')
            return [], IDs
        else:
            timeline = []
            for i in range(self.__docs_num_in_1timeline):
                doc_ID = IDs[i]
                get_doc_info_by_id = lambda: next((item for item in self.__entity_info['docs_info']['docs'] if item['ID'] == doc_ID), None)
                doc_info_dict = get_doc_info_by_id()
                headline, short_description, date, content = doc_info_dict['headline'], doc_info_dict['short_description'], doc_info_dict['date'], doc_info_dict['content']
                doc = {
                    'ID': IDs[i],
                    'is_fake': False,
                    'document': f"{headline}: {short_description}",
                    'headline': headline,
                    'short_description': short_description,
                    'date': date,
                    'content': content,
                    'reason': reasons[i]
                }

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
                    'number': {
                        'type': 'integer',
                        'description': 'The number of documents.'
                    },
                    'IDs': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': 'A list of Document ID.'
                    },
                    'reasons': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'A list of REASONS and STATEMENTS.'
                    }
                },
                'required': ['number', 'IDs', 'reasons']
            },
        }
        return function_info


    # fromat fake news
    def format_fake_news(self, headline, short_description, date, content, remarks=None):
        fake_news = {
            'is_fake': True,
            'headline': headline,
            'short_description': short_description,
            'date': date,
            'content': content
        }
        return fake_news, remarks

    def _format_fake_news_info(self):
        function_info = {
            'name': 'format_fake_news',
            'description': 'Convert the information about generated fake news into a dictionary type.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'headline': {
                        'type': 'string',
                        'description': 'headline of fake news.'
                    },
                    'short_description': {
                        'type': 'string',
                        'description': 'short description of fake news.'
                    },
                    'date': {
                        'type': 'string',
                        'description': 'The date of fake news. This must be YYYY-MM-DD.'
                    },
                    'content': {
                        'type': 'string',
                        'description': 'content of fake news.'
                    },
                    'remarks': {
                        'type': 'object',
                        'description': 'It is only valid when fake news is generated by replacing a suitable one among the documents included in the input timeline.',
                        'properties': {
                            'document_id': {'type': 'integer', 'description': 'document ID of the original document before replacement.'},
                            'headline': {'type': 'string', 'description': 'headline of the original document before replacement.'},
                            'short_description': {'type': 'string', 'description': 'short_description of the original document before replacement.'},
                        }
                    }
                },
                'required': ['headline', 'short_description', 'date', 'content']
            }
        }
        return function_info
