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
3. Execute `data_preprocess/with_content/process_data_with_content.py`