from typing import TypedDict, Literal
from create_dataset.type.no_fake_timelines import Setting, Analytics

class DocForDataset(TypedDict):
    ID: int
    is_fake: bool
    headline: str
    short_description: str
    date: str
    content: str

class TimelineDataInfo(TypedDict):
    entity_id: int
    entity_items: list[str]
    setting: Literal['none', 'rep0', 'rep1','rep2','rep3', 'ins0', 'ins1', 'ins2']
    timeline: list[DocForDataset]

class NoFakeTimelinesInfo(TypedDict):
    entities_num: int
    setting: Setting
    analytics: Analytics

class FakeNewsDataset(TypedDict):
    name: str
    description: str
    docs_num_in_1_timeline: dict[str, int]
    no_fake_timelines_info: NoFakeTimelinesInfo
    data: list[TimelineDataInfo]