from typing import TypedDict

from create_dataset.type.no_fake_timelines import EntityTimelineData, Setting

class SplitDataset(TypedDict):
    name: str
    description: str
    entities_num: int
    timelines_num: int
    split_n: int
    setting: Setting
    data: list[EntityTimelineData]

class OneComInfo(TypedDict):
    com_id: int
    ent_num: int
    timeline_num: int
    ent_ids: list[int]
    docs_ids: list[int]

ComInfo = list[OneComInfo]