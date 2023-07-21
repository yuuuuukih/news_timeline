# process_data_with_content.py

This script is designed to retrieve contents of articles by scraping. It uses the BeautifulSoup library to parse the HTML contents and get the text of articles.

## How to run

To run the script, use the following command:
```sh
FILE_PATH=your_file_path
OUT_DIR=your_output_directory
python process_data_with_content.py --file_path $FILE_PATH --out_dir $OUT_DIR --file_name your_file_name.json --start_year your_start_year --end_year your_end_year
```
Replace "your_file_path", "your_output_directory", "your_file_name.json", "your_start_year", and "your_end_year" respectively with the path to your data file, your desired output directory, your desired output filename, and the start and end years defining the range of articles to be processed.

### Arguments

- `--file_path`: The path to the data file. Defaults to `/mnt/mint/hara/datasets/news_category_dataset/preprocessed/without_content/data.json`.
- `--out_dir`: The directory where the output should be stored. Defaults to `/mnt/mint/hara/datasets/news_category_dataset/preprocessed/with_content`.
- `--file_name`: The filename of the output file. Defaults to `data.json`.
- `--start_year`: Start year of the range of data to be processed. Defaults to 2012.
- `--end_year`: End year of the range of data to be processed. Defaults to 2022.

### Outputs

The output JSON file will include the original data, with an additional "content" field added to each data entry. The output file is formatted as follows:

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