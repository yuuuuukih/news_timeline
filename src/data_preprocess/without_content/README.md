# process_data_without_content.py

This script aims to process the raw news category dataset to JSON format. This includes the addition of the year, month, and day information as properties.

## Dependencies
- Using kaggle dataset "News Category Dataset"
[News Category Dataset](https://www.kaggle.com/datasets/rmisra/news-category-dataset?resource=download)

```
kaggle datasets download -d rmisra/news-category-dataset
```

## How to run

To run the script, use the following command:
```sh
RAW_FILE_PATH=your_raw_file_path
OUT_DIR=your_output_directory
python process_data_without_content.py --raw_file_path $RAW_FILE_PATH --out_dir $OUT_DIR --file_name your_file_name.json
```
Replace "your_raw_file_path", "your_output_directory", and "your_file_name.json" with the path to your raw data file, your desired output directory, and your desired output filename respectively.

### Arguments

- `--raw_file_path`: The path to the raw data file. Defaults to `/mnt/mint/hara/datasets/news_category_dataset/raw/News_Category_Dataset_v3.json`.
- `--out_dir`: The directory where the output should be stored. Defaults to `/mnt/mint/hara/datasets/news_category_dataset/preprocessed/without_content`.
- `--file_name`: The filename of the output file. Defaults to `data.json`.

### Outputs

The formatted JSON file with the date split into separate year, month, and day fields.

### Example

```sh
RAW_FILE_PATH=/datasets/news_category_dataset/raw/News_Category_Dataset_v3.json
OUT_DIR=/datasets/news_category_dataset/preprocessed/without_content
$ python process_data_without_content.py --raw_file_path $RAW_FILE_PATH --out_dir $OUT_DIR --file_name formatted_data.json
Format completed.
Time info addition completed.
```

## Example of raw data

The original data which is being processed has the following structure:

```json
{
    "link": "https://www.huffpost.com/entry/covid-boosters-uptake-us_n_632d719ee4b087fae6feaac9",
    "headline": "Over 4 Million Americans Roll Up Sleeves For Omicron-Targeted COVID Boosters",
    "category": "U.S. NEWS",
    "short_description": "Health experts said it is too early to predict whether demand would match up with the 171 million doses of the new boosters the U.S. ordered for the fall.",
    "authors": "Carla K. Johnson, AP",
    "date": "2022-09-23"
},
```

## Processed data format

After being processed, the top-level object will have a 'name' and 'data' attributes. The 'data' attribute is an array of processed news category data, each formatted as:

```json
{
    "name": "News_Category_Dataset_v3 without content",
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
            "day": "23"
        },
    ]
}
```