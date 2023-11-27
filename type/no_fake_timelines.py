from typing import TypedDict

class Doc(TypedDict):
    ID: int
    is_fake: bool
    document: str
    headline: str
    short_description: str
    date: str
    content: str
    reason: str

class TimelineData(TypedDict):
    reexe_num: int
    docs_num: int
    story: str
    timeline: list[Doc]

class TimelineInfo(TypedDict):
    timeline_num: int
    data: list[TimelineData]

class DocsInfo(TypedDict):
    IDs: list[int]

class EntityTimelineData(TypedDict):
    entity_ID: int
    entity_items: list[str]
    docs_info: DocsInfo
    timeline_info: TimelineInfo

class Analytics(TypedDict):
    docs_num_in_1timeline: dict[str, int]
    re_execution_num: dict[str, int]
    no_timeline_entity_id: list[int]

class Temperature(TypedDict):
    _1st_response: float # 1st_response
    _2nd_response: float # 2nd_response

class DocsNumIn1timeline(TypedDict):
    min: int
    max: int

class Setting(TypedDict):
    model: str
    temperature: Temperature
    docs_num_in_1timeline: DocsNumIn1timeline
    top_tl: float
    max_reexe_num: int

class NoFakeTimeline(TypedDict):
    name: str
    description: str
    date: str
    entities_num: int
    setting: Setting
    analytics: Analytics
    data: list[EntityTimelineData]
