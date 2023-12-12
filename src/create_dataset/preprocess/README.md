# How to preprocess the data.

## Dataset
- Using kaggle dataset "News Category Dataset"
[News Category Dataset](https://www.kaggle.com/datasets/rmisra/news-category-dataset?resource=download)

```
kaggle datasets download -d rmisra/news-category-dataset
```

### The number of data per year
| Year | Count |
|------|-------|
| 2012 | 31355 |
| 2013 | 34583 |
| 2014 | 32339 |
| 2015 | 32006 |
| 2016 | 32098 |
| 2017 | 29889 |
| 2018 | 9734  |
| 2019 | 2005  |
| 2020 | 2054  |
| 2021 | 2066  |
| 2022 | 1398  |

## How to preprocess
1. Download the above dataset.
2. Execute `python data_preprocess/without_content/process_data_without_content.py`
3. Execute `python data_preprocess/with_content/process_data_with_content.py`

# process_data_without_content.py

This script aims to process the raw news category dataset to JSON format. This includes the addition of the year, month, and day information as properties.

## Dependencies
- Using kaggle dataset "News Category Dataset"
[News Category Dataset](https://www.kaggle.com/datasets/rmisra/news-category-dataset?resource=download)

```
kaggle datasets download -d rmisra/news-category-dataset
```

## Processed data format

After being processed, the top-level object will have a 'name' and 'data' attributes. The 'data' attribute is an array of processed news category data, each formatted as below.
The preprocessed data will include the original data, with an additional "content" field added to each data entry. The output file is formatted as follows:

```json
{
    "name": "News_Category_Dataset_v3 with content (2019 - 2022)",
    "length": 100,
    "data": [
        {
            "link": "https://www.huffpost.com/entry/covid-boosters-uptake-us_n_632d719ee4b087fae6feaac9",
            "headline": "Over 4 Million Americans Roll Up Sleeves For Omicron-Targeted COVID Boosters",
            "category": "U.S. NEWS",
            "short_description": "Health experts said it is too early to predict whether demand would match up with the 171 million doses of the new boosters the U.S. ordered for the fall.",
            "authors": "Carla K. Johnson, AP",
            "date": "2022-09-23",
            "year": "2022",
            "month": "09",
            "day": "23",
            "content": "The content of the article obtained by scraping..."
        },
        // Other articles
    ]
}
```
This represents one article. The "data" key will contain a list of such articles. The "length" key represents the number of articles. The name represents the name of the dataset along with the period it covers.

### Note
Please be aware that web scraping is subject to the terms of use of the website being scraped. Always respect the website's robots.txt file and consider the legal implications.