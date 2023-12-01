# extract_data_by_keywords.py

This script is designed to extract data from the articles that contain all specified keywords in their headline and short_description. It also creates log files to record information about these searches.

## How to run

To run the script, use the following command:
```sh
FILE_PATH=your_file_path
OUT_DIR=your_output_directory
python extract_data_by_keywords.py --file_path $FILE_PATH --out_dir $OUT_DIR --keywords keyword1 keyword2 ... --save
```
Replace "your_file_path", "your_output_directory", "keyword1 keyword2 ..." respectively with the path to your data file, your desired output directory, and the keywords you want to search. "keyword1 keyword2 ..." are the relevant keywords. The script will only select articles that contain all specified keywords in their headline and short_description.

### Arguments

- `--file_path`: The path to the data file. Defaults to `/mnt/mint/hara/datasets/news_category_dataset/preprocessed/with_content/2019_2022.json`.
- `--out_dir`: The directory where the output log files should be stored. Defaults to `/mnt/mint/hara/datasets/news_category_dataset/preprocessed/keywords/2019_2022`.
- `--keywords`: Keywords to be used for extraction. Users can pass multiple keywords, and the script will only select those articles that contain all the provided keywords in their headline and short_description.
- `--save`: A flag indicating whether the script should save the log of extracted data. If this flag is present, the script will save a JSON and a Markdown log file in the output directory specified by `--out_dir`.

### Outputs

The script creates two log files to track information about the search performed:

- A JSON file `keywords.json` containing a log of all the searches, their IDs, and the amount of data extracted.
- A Markdown file `README.md` rendering the same information in a readable format.

- `keywords.json`:

This is a JSON file containing a log of all the searches, their IDs, and the amount of data extracted. Below is a sample format of the output JSON file:

```json
{
    "name": "Keywords Log",
    "description": "This log contains information about keyword searches and their corresponding results from the dataset between 2019 and 2022.",
    "database": "2019_2022.json",
    "log": [
        {
            "id": 0,
            "name": "coronavirus vaccine",
            "keywords": ["omicron", "COVID"],
            "length": 6,
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
                }, { ... }
                // Other articles
            ]
        }, { ... }
        // Other searches
    ]
}
```
In the `log` array, each entry represents a keyword search, providing information about the ID of the search (generated automatically), the space-separated keywords string used for the search (`name`), the list of keywords, the number of results (`length`), and the actual articles data (`data`).

- `README.md`:

This is a Markdown file that represents the same information as `keywords.json` but in a readable format. Below is a sample format of the README.md file:

```
# Keyword Search Results
This file contains the results of keyword searches along with their corresponding IDs and the number of matches.

| ID | Keywords | Number of Results |
| -- | -------- | ----------------- |
| 0 | omicron, COVID | 6 |
```

If the `--save` flag is present, a JSON file with the extracted data will also be saved in the output directory.

Both logs are designed as continuous logs, meaning that each search made will append its results to the existing log (if it exists). If the same keyword combination is used in multiple searches, the log will not create a duplicate entry.

### Note

The scripts only print the length of the extracted data, not the data itself, when `--save` flag is not used. To actually get the extracted data, use the `--save` flag when running the script.

# Keyword Search Results
This file contains the results of keyword searches along with their corresponding IDs and the number of matches.

| ID | Keywords | Number of Results |
| -- | -------- | ----------------- |
| 0 | omicron, COVID | 6 |
| 1 | donald, trump, politics | 3 |
| 2 | vaccine, COVID, U.S. | 7 |
| 3 | COVID, million, U.S. | 7 |
| 4 | COVID, million, have | 6 |
| 5 | Biden, health | 9 |
| 6 | coronavirus, vaccine | 26 |
