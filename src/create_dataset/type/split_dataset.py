from typing import TypedDict

from create_dataset.type.no_fake_timelines import EntityTimelineData

class SplitDataset(TypedDict):
    name: str
    description: str
    entities_num: int
    setting: str
    data: list[EntityTimelineData]

class OneComInfo(TypedDict):
    com_id: int
    ent_num: int
    timeline_num: int
    ent_ids: list[int]
    docs_ids: list[int]

ComInfo = list[OneComInfo]