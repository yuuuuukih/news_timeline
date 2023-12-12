from typing import TypedDict

# ====== From ./documents.py because of the import path (ModuleNotFoundError) ======
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
# ====== Up to here ======

class DocsInfo(TypedDict):
    IDs: list[int]
    docs: list[DocData]

class EntityData(TypedDict):
    freq: int
    items: list[str]
    ID: int
    docs_info: DocsInfo

class EntitiesSection(TypedDict):
    comments: str
    The_number_of_entities: int # The number of entities
    list: list[EntityData]

class Hparms(TypedDict):
    threshold: float
    min_support: float
    min_confidence: float
    k1: float

class WordsRemovedInfo(TypedDict):
    The_number_of_words: int
    list: list[str]

class EntitiesData(TypedDict):
    preprocess: dict[str, bool]
    hparms: Hparms
    words_removed_by_Okapi_BM25_TF_IDF: WordsRemovedInfo # words removed by Okapi BM25 / TF-IDF
    entities: EntitiesSection

class Entities(TypedDict):
    name: str
    description: str
    year: str
    The_number_of_documents: int # The number of documents
    data: list[EntitiesData]



