import os
import json
import datetime

from create_dataset.timeline.set_timeline import TimelineSetter

from create_dataset.utils.measure_exe_time import measure_exe_time

from create_dataset.type.entities import Entities
from create_dataset.type.no_fake_timelines import EntityTimelineData, NoFakeTimeline
from typing import Literal

from create_dataset.utils.update_occurrences import update_occurrences

class MultipleTimelineGenerator(TimelineSetter):
    def __init__(self, entities_data: Entities, model_name: str, temp: float, judgement: Literal['diff', 'rate', 'value'], min_docs_num_in_1timeline=8, max_docs_num_in_1timeline=10, top_tl=0.5, start_entity_id=0):
        super().__init__(model_name, temp, judgement, min_docs_num_in_1timeline, max_docs_num_in_1timeline, top_tl)

        self.entity_info_list = entities_data['data'][0]['entities']['list'][start_entity_id:]
        # self.entity_info_list = entities_data['data'][0]['entities']['list'][236:236+3]

    @measure_exe_time
    def generate_multiple_timelines(self):
        for i, entity_info in enumerate(self.entity_info_list):
            print('\n')
            print(f"{i+1}/{len(self.entity_info_list)}. ID: {entity_info['ID']}, entity: {entity_info['items']}")
            # Define the number of timelines to generate for this entity
            timeline_num = int(int(entity_info['freq'] / self.max_docs_num_in_1timeline) * self.top_tl)

            # Generate timelines
            output_data: EntityTimelineData = self.generate_timelines(entity_info, timeline_num)
            # Save
            self.save_timelines(output_data)


    # For save timelines
    def save_timelines(self, timeline_data: EntityTimelineData, name_to_save='Data'):
        # Open the file
        file_path = os.path.join(self.__out_dir, f"{self.__json_file_name}.json")
        try:
            with open(file_path, 'r') as F:
                no_fake_timelines:NoFakeTimeline = json.load(F)
        except FileNotFoundError:
            no_fake_timelines = {
                'name': self.__json_file_name,
                'description': 'Timeline dataset without fake news.',
                'date': f'{datetime.datetime.today()}',
                'entities_num': 0,
                'setting': {
                    'model': self.model_name,
                    'temperature': {
                        '1st_response': self.temp,
                        '2nd_response': 0,
                    },
                    'docs_num_in_1timeline': {
                        'min': self.min_docs_num_in_1timeline,
                        'max': self.max_docs_num_in_1timeline
                    },
                    'top_tl': self.top_tl,
                    'max_reexe_num': self.get_max_reexe_num(),
                    'rouge': {
                        'rouge_used': self.rouge_used,
                        'alpha': self.rouge_alpha,
                        'th_1': self.rouge_th_1,
                        'th_2': self.rouge_th_2,
                        'th_l': self.rouge_th_l,
                        'th_2_rate': self.rouge_th_2_rate,
                        'th_2_diff': self.rouge_th_2_diff,
                    }
                },
                'analytics': {
                    'docs_num_in_1_timeline': {},
                    're_execution_num': {},
                    'no_timeline_entity_id': []
                },
                'data': []
            }
        # Update
        no_fake_timelines['data'].append(timeline_data)
        no_fake_timelines['entities_num'] = len(no_fake_timelines['data'])

        no_fake_timelines['analytics']['docs_num_in_1_timeline'] = update_occurrences(no_fake_timelines['analytics']['docs_num_in_1_timeline'], self.analytics_docs_num)
        no_fake_timelines['analytics']['re_execution_num'] = update_occurrences(no_fake_timelines['analytics']['re_execution_num'], self.analytics_reexe_num)
        no_fake_timelines['analytics']['no_timeline_entity_id'].extend(self.no_timeline_entity_id)
        # save the json file.
        with open(file_path, 'w', encoding='utf-8') as F:
            json.dump(no_fake_timelines, F, indent=4, ensure_ascii=False, separators=(',', ': '))
            print(f'{name_to_save} is saved to {self.__json_file_name}.json')

    def set_file_to_save(self, json_file_name, out_dir):
        self.__json_file_name = json_file_name
        self.__out_dir = out_dir
