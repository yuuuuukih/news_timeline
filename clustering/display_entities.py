import json
from tabulate import tabulate

def display_json_as_table(json_data):
    # Display the 'entities' section as a table for each element inside 'data'
    for item in json_data['data']:
        preprocess = item['preprocess']
        hparm = item['hparm']
        removed = item['words removed by Okapi BM25 / TF-IDF']
        entities = item['entities']

        '''
        ======================================================
        '''
        print(f"Preprocess: {' | '.join([f'{k}: {v}' for k, v in preprocess.items()])}")
        print(f"Hparm: {' | '.join([f'{k}: {v}' for k, v in hparm.items()])}")
        print(f"Removed words ({removed['The number of words']}): {removed['list']}")
        print(f"Entities ({entities['The number of entities']})")
        '''
        ======================================================
        '''

        # Create a new table data list for each element
        table_data = []
        # Add header row for this section
        header = ["ID", "items", "freq"]
        table_data.append(header)
        # # Add each entity from the 'list' to the table with text wrapping
        for el in entities['list']:
            table_data.append([el['ID'], el['items'], el['freq']])
        # Output the table for this section
        print(tabulate(table_data, headers="firstrow", tablefmt="pretty"))


if __name__ == '__main__':
    PATH_JSON = '/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/fp_growth_entities.json'
    with open(PATH_JSON, 'r') as json_file:
            json_data = json.load(json_file)

    display_json_as_table(json_data)
