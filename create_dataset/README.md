# Dataset
## JSON data structure
- documents.json
```
{
    "name": "News_Category_Dataset_v3 with content (2019 - 2022),
    "length": 7523,
    "description": "This dataset is /datasets/news_category_dataset/preprocessed/with_content/2019_2022.json with the analytics and docs of ID, preprocessed_tokens, entities_info properties added."
    "analytics": {
        "category": {
            "U.S. NEWS: 1208,
            ...
        },
        "entities num": {
            "0": 4491,
            ...
        }
    },
    "data": [
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
```

- entities.json
```
{
    "name": "Entities Log",
    "description": "This file contains the results of previous runs of get_entities.py with hyper parameters.",
    "year": "2019-2022",
    "The number of documents": 7523,
    "data": [
        {
            "preprocess": {
                "Remove stop words": true,
                ...
            },
            "hparms": {
                "threshold": 0.6,
                "min_support": 0.003,
                "min_confidence": 0.6,
                "k1": 1.2
            },
            "words removed by Okapi BM25 / TF-IDF": {
                "The number of words": 298,
                "list": ["xxx", ...]
            },
            "entities": {
                "comments": "items >= 2",
                "The number of entities": 262,
                "list": [
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
                    ...
                ]
            }
        }
    ]
}
```
