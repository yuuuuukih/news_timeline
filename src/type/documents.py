from typing import TypedDict

class EntitiesInfo(TypedDict):
    num: int
    IDs: list[int]
    entities: list[list[str]]

class DocData(TypedDict):
    link: str
    headline: str
    category: str
    short_description: str
    authors: str
    date: str
    year: str
    month: str
    day: str
    content: str
    ID: int
    preprocessed_tokens: list[str]
    entities_info: EntitiesInfo

class Analytics(TypedDict):
    category: dict[str, int]
    entities_num: dict[str, int]

class Documents(TypedDict):
    name: str
    length: int
    description: str
    analytics: Analytics
    data: list[DocData]