import functools
import openai
import time
import sys
from typing import Tuple
from sumeval.metrics.rouge import RougeCalculator

from get_gpt_response import GPTResponseGetter

sys.path.append('../')
from type.entities import EntityData
from type.no_fake_timelines import TimelineData, EntityTimelineData, Doc

# Define the retry decorator
def retry_decorator(max_error_count=10, retry_delay=1): # Loop with a maximum of 10 attempts
    def decorator_retry(func):
        functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Initialize an error count
            error_count = 0
            while error_count < max_error_count:
                try:
                    v = func(*args, **kwargs)
                    return v
                except openai.error.Timeout as e:
                    print(f"Timeout error occurred: {e}. Re-running the function.")
                    error_count += 1
                except openai.error.APIError as e:
                    print(f"OPENAI API error occurred: {e}. Re-running the function.")
                    error_count += 1
                except ValueError as e:
                    print(f"ValueError occurred: {e}. Re-running the function.")
                    error_count += 1
                except TypeError as e: # For when other functions are called in function calling.
                    print("TypeError occurred. Re-running the function.")
                    print(f"TypeError: {e}")
                    error_count += 1
                except openai.error.InvalidRequestError as e:
                    print("InvalidRequestError occurred. Continuing the program.")
                    print(f"openai.error.InvalidRequestError: {e}")
                    break  # Exit the loop
                time.sleep(retry_delay)  # If an error occurred, wait before retrying
            if error_count == max_error_count:
                sys.exit("Exceeded the maximum number of retries. Exiting the function.")
                return None
        return wrapper
    return decorator_retry

class TimelineSetter(GPTResponseGetter):
    '''
    docs_num_in_1timeline: The number of documents contained in ONE timeline,
    top_tl: Number of timelines to be generated, relative to the number of timelines that can be generated.
    '''
    def __init__(self, model_name, temp, min_docs_num_in_1timeline=8, max_docs_num_in_1timeline=10, top_tl=0.5):
        # super
        # super.__init__()
        # parameters
        self.model_name = model_name
        self.temp = temp
        self.min_docs_num_in_1timeline = min_docs_num_in_1timeline
        self.max_docs_num_in_1timeline = max_docs_num_in_1timeline
        self.top_tl = top_tl
        # preprocess of docs_num_in_1timeline
        self.list_docs_num_in_1timeline = list(range(self.min_docs_num_in_1timeline, self.max_docs_num_in_1timeline + 1))
        self.str_docs_num_in_1timeline = ' or '.join([str(n) for n in self.list_docs_num_in_1timeline])
        # For analytics
        self.initialize_list_for_analytics()

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
    def get_prompts(self, entity_info: EntityData):
        '''
        system content
        '''
        system_content = "You are a professional story writer. Execute the function calling's format_timeline function."

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
            "# INSTRUCTIONS\n"
            f"Select \" at least {self.min_docs_num_in_1timeline}\", and \"at most {self.max_docs_num_in_1timeline}\" documents that are most relevant to the above story.\n"
            # f"Pick \"{self.str_docs_num_in_1timeline}\" documents that are most relevant to the above story.\n"
            # "When responding, generate the Document ID, the headline: short_description of the document, and which sentence in the story the document is most related to.\n"
            "The headline and short_description you choose should cover most of the story.\n"
            f"Please follow these two conditions and generate by using the following OUTPUT FORMAT.\n"
            # f"When responding for \"{self.str_docs_num_in_1timeline}\" documents, please follow these two conditions and generate by using the following OUTPUT FORMAT \"{self.str_docs_num_in_1timeline}\" times.\n"

            "# CONDITIONS\n"
            f"1. First of all, please generate how many documents you have picked out of {self.str_docs_num_in_1timeline}.\n"
            "2. generate the Document ID, the headline: short_description of the document.\n"
            "3. generate REASONS why you chose this document and clearly point out the STATEMENT in the story you generated which is most relevant to this document.\n"

            "# OUTPUT FORMAT\n"
            "1. Number of documents -> \n"
            "2. ID -> , document -> \n"
            "3. REASONS and STATEMENT -> \n"
        )

        return system_content, user_content_1, user_content_2

    def _delete_dicts_by_id(self, dictionary_list: list[dict], id_list: list[int]) -> list[dict]:
        # Find the indexes of dictionaries with IDs to be removed
        indexes_to_remove = [i for i, item in enumerate(dictionary_list) if item['ID'] in id_list]
        # Create a new list without the dictionaries at the identified indexes
        filtered_list = [item for i, item in enumerate(dictionary_list) if i not in indexes_to_remove]
        return filtered_list
    
    def _check_coverage_by_rouge(self, timeline_list: list[Doc], story: str) -> bool:
        docs_list = []
        for doc in timeline_list:
            docs_list.append(f"{doc['headline']} {doc['short_description']}")
        docs_str = " ".join(docs_list)

        # Calcurate rouge score
        rouge = RougeCalculator(stopwords=True, lang="en")
        rouge_1 = rouge.rouge_n(
                    summary=docs_str,
                    references=story,
                    n=1)
        rouge_2 = rouge.rouge_n(
                    summary=docs_str,
                    references=story,
                    n=2)
        rouge_l = rouge.rouge_l(
                    summary=docs_str,
                    references=story)

        THRESHOLD = {
            'rouge_1': 0.32,
            'rouge_2': 0.15,
            'rouge_l': 0.2
        }
        boolean: bool = rouge_1 > THRESHOLD['rouge_1'] or rouge_2 > THRESHOLD['rouge_2'] or rouge_l > THRESHOLD['rouge_l']

        if not boolean:
            print('Coverage by rouge score is not enough.')
            print(f"ROUGE-1: {rouge_1}, ROUGE-2: {rouge_2}, ROUGE-L: {rouge_l}")
            print(f"Timeline num: {len(timeline_list)}")
        return boolean

    def _check_conditions(self, entity_info: EntityData, IDs_from_gpt: list[int], timeline_list: list[Doc]) -> bool:
        # Check number of docs
        cond1 = len(IDs_from_gpt) in self.list_docs_num_in_1timeline
        # Check document ID
        cond2 = set(IDs_from_gpt) <= set(entity_info['docs_info']['IDs'])
        # Check the length between IDs_from_gpt and timeline_list
        cond3 = len(timeline_list) == len(IDs_from_gpt)
        return cond1 and cond2 and cond3

    def initialize_list_for_analytics(self):
        self.no_timeline_entity_id = []
        self.analytics_docs_num = []
        self.analytics_reexe_num = []

    def get_max_reexe_num(self) -> int:
        return self.__max_reexe_num

    def set_max_reexe_num(self, value: int) -> None:
        self.__max_reexe_num = value

    def set_reexe_num(self, value: int) -> None:
        self.__reexe_num = value

    @retry_decorator(max_error_count=10, retry_delay=1)
    def generate_story_and_timeline(self, entity_info: EntityData) -> Tuple[TimelineData, list[int]]:
        # setter for GPTResponseGetter
        self.set_entity_info(entity_info)

        # prompts
        system_content, user_content_1, user_content_2 = self.get_prompts(entity_info)

        # Loop processing
        for i in range(self.__max_reexe_num+1):
            self.set_reexe_num(i)

            # messages
            messages=[
                {'role': 'system', 'content': system_content},
                {'role': 'user', 'content': user_content_1}
            ]

            messages = self.get_gpt_response_classic(messages, model_name=self.model_name, temp=self.temp)
            story: str = messages[-1]['content']
            print('Got 1st GPT response.')

            messages.append({'role': 'user', 'content': user_content_2})
            timeline_list, IDs_from_gpt = self.get_gpt_response_timeline(messages, model_name=self.model_name, temp=0)

            #Check
            if self._check_conditions(entity_info, IDs_from_gpt, timeline_list) and self._check_coverage_by_rouge(timeline_list, story):
                # If all conditions are met
                print('Got 2nd GPT response.')
                break # Exit the loop as conditions are met
            else:
                print('Failed to get 2nd GPT response.')
                messages = []
                if i != self.__max_reexe_num:
                    print(f"Re-execution for the {i + 1}-th time")
        else:
            print('NO TIMELINE INFO')
            self.set_reexe_num(-1)
            self.no_timeline_entity_id.append(entity_info['ID'])
            story = ''
            timeline_list = []

        # Update timelines
        timeline_info: TimelineData = {
            'reexe_num': self.__reexe_num,
            'docs_num': len(timeline_list),
            'story': story,
            'timeline': timeline_list
        }

        return timeline_info, IDs_from_gpt

    def generate_timelines(self, entity_info_left: EntityData, timeline_num: int) -> EntityTimelineData:
        entity_ID, entity_items = entity_info_left['ID'], entity_info_left['items']
        list_to_save_timelines: list[TimelineData] = []
        docs_IDs: list[int] = []

        # Initialize for analytics list
        self.initialize_list_for_analytics()
        for i in range(timeline_num):
            print(f'=== {i+1}/{timeline_num}. START ===')

            timeline_info, IDs_from_gpt = self.generate_story_and_timeline(entity_info_left)

            if len(IDs_from_gpt) > 0 and timeline_info['reexe_num'] != -1:
                list_to_save_timelines.append(timeline_info)
                docs_IDs.extend(IDs_from_gpt)
                self.analytics_docs_num.append(timeline_info['docs_num'])
            self.analytics_reexe_num.append(timeline_info['reexe_num'])

            # Update entity info left
            entity_info_left['docs_info'] = {
                'IDs': list(set(entity_info_left['docs_info']['IDs']) - set(IDs_from_gpt)),
                'docs': self._delete_dicts_by_id(entity_info_left['docs_info']['docs'], IDs_from_gpt)
            }
            entity_info_left['freq'] = len(entity_info_left['docs_info']['IDs'])

            print(f'=== {i+1}/{timeline_num}. DONE ===')

        output_data: EntityTimelineData = {
            'entity_ID': entity_ID,
            'entity_items': entity_items,
            'docs_info': {
                'IDs': docs_IDs
            },
            'timeline_info': {
                'timeline_num': len(list_to_save_timelines),
                'data': list_to_save_timelines
            }
        }

        return output_data
