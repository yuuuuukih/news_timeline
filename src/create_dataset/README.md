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
            "U.S. NEWS": 1208,
            ...
        },
        "entities num": {
            "0": 4491,
            ...
        }
    },
    "data": [
        {
            "link": "xxx",
            "headline": "xxx",
            "category": "xxx",
            "short_description": "xxx",
            "authors": "xxx",
            "date": "xxx",
            "year": "xxx",
            "month": "xxx",
            "day": "xxx",
            "content": "xxx",
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
                                    "link": "xxx",
                                    "headline": "xxx",
                                    "category": "xxx",
                                    "short_description": "xxx",
                                    "authors": "xxx",
                                    "date": "xxx",
                                    "year": "xxx",
                                    "month": "xxx",
                                    "day": "xxx",
                                    "content": "xxx",
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

- no_fake_timelines.json
```
{
    'name': 'no_fake_timelines',
    'description': 'Timeline dataset without fake news.',
    'date': 'xxxx-xx-xx xx:xx:xx.xxxxxx',
    'setting': {
        'model': 'gpt-4',
        'temperature': {
            '1st_response': 0.8,
            '2nd_response': 0,
        },
        'docs_num_in_1timeline': {
            'min': 4,
            'max': 8
        },
        'top_tl': args.top_tl,
        'max_reexe_num': 1
    },
    analytics: {
        'docs_num_in_1timeline': {
            '0': x,
            '4': x,
            ...
        },
        're_execution_num': {
            '-1': x,
            '0': x,
            ...
        },
        'no_timeline_entity_id': [
            x, ...
        ]
    },
    'data': [
        {
            'entity_ID': xxx,
            'entity_items': ['xxx', 'xxx', ...],
            'docs_info': {
                'IDs': [xxx, xxx, ...]
            },
            'timeline_info': {
                'timeline_num': x,
                'data': [
                    {
                        'reexe_num': x,
                        'docs_num': x,
                        'story': 'xxxxxxx',
                        'timeline': [
                            {
                                'ID': xxx,
                                'is_fake': false,
                                'document': 'xxx: xxx',
                                'headline': 'xxx',
                                'short_description': 'xxx',
                                'date': 'xxxx-xx-xx',
                                'content': 'xxxxxx',
                                'reason': 'xxxxxx'
                            }, ...
                        ]
                    }, ...
                ]
            }
        }, ...
    ]
}
```

# Files
## add_props_to_docs.py
- Create documents.json which has some props (e.g., entity information) added.

## add_props_to_entities.py
- Create entities.json which has documents information added.

## generate_timeline.py
- Generate timelines about ONE entities pair.
- Input: ONE entities pair (e.g., ["russia", "ukraine"]) containing documents information.
- Output:
```
[
    {
        "story": xxx,
        "timeline": [
            {
                "ID": xxx,
                "document": "headline: short_description",
                "headline": "xxx",
                "short_description": "xxx",
                "date": '0000-00-00',
                "content": "xxx"
                "reason": "xxx",
            }, ...
        ]
    }, ...
]
```


# Prompts
## story
```
"# INSTRUCTIONS\n"
"Generate the best story based on the following constraints and input statements.\n"

"# CONSTRAINTS\n"
f"- Generate stories based on the {number of documents} documents (consisting of headline and short description) in the INPUT STATEMENTS below.\n"
f"- The story must be about {keyword group}.\n"
"- It must be less than 100 words.\n"

"# INPUT STATEMENTS\n"
"Document ID -> {doc_ID}, documents -> {headline}: {short_description}\n"

"# OUTPUT STORY\n"
```

## pick n documents
```
"# INSTRUCTIONS\n"
f"Select \" at least {n_min}\", and \"at most {n_max}\" documents that are most relevant to the above story.\n"
"Please follow these two conditions and generate by using the following OUTPUT FORMAT.\n"

"# CONDITIONS\n"
f"1. First of all, please generate how many documents you have picked out of {4,5,6,7,8}.\n"
"2. generate the Document ID, the headline: short_description of the document.\n"
"3. generate REASONS why you chose this document and clearly point out the STATEMENT in the story you generated which is most relevant to this document.\n"

"# OUTPUT FORMAT\n"
"1. Number of documents -> \n"
"2. ID -> , document -> \n"
"3. REASONS and STATEMENT -> \n"
```

## fake news
```
"# INSTRUCTIONS\n"
f"Below are {n} documents about {keyword group}. Each document contains time information (YYYY-MM-DD), forming a timeline.\n"
"Generate ONE fake news based on the following constraints and input documents.\n"

"# INPUT DOCUMENTS\n"
f"document ID. {doc['ID']}\n"
f"headline: {doc['headline']}\n"
f"short_description: {doc['short_description']}\n"
f"date: {doc['date']}\n"
f"content: {doc['content']}\n"

"# CONSTRAINTS\n"
"- It needs to contain headline, short_description, date (YYYY-MM-DD), and content properties.\n"
"- In a step-by-step manner, first generate the content and date of fake news, and then generate the headline and short description."
"Additionally, explain why you generate such fake news and which parts of the fake news meet the following constraints"
f"- The date of the fake news must be within a period that is later than the oldest date among the {n} documents and earlier than the newest date.\n"

...
```