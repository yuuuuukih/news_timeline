'''
Extract data from keywords.
'''

import os
import json
from argparse import ArgumentParser

"""
Convert all lowercase characters in the list of strings to lowercase.

Parameters:
    input_list (list): A list containing elements of type string.

Returns:
    list: A new list with all lowercase strings, while preserving non-string elements.
"""
def lowercase_strings_in_list(input_list):
    return [item.lower() for item in input_list if isinstance(item, str)]


# Get articles that contain all keywords in the headline and short_description.
def get_articles_by_keywords(data, keywords):
    matching_data = []
    for entry in data:
        headline_desc = entry['headline'].lower() + ' ' + entry['short_description'].lower() # Combine the headline and short_description
        keywords = lowercase_strings_in_list(keywords)
        if all(keyword in headline_desc for keyword in keywords):
            matching_data.append(entry)

    return matching_data

# Save
def save_log(output, out_dir):
    json_name, md_name = 'keywords', 'README'

    keywords_json = os.path.join(out_dir, f'{json_name}.json')
    keywords_md = os.path.join(out_dir, f'{md_name}.md')
    keywords_cd_md = os.path.abspath(f'{md_name}.md')
    keywords = output['keywords']

    '''
    Template is generated if keywords.json (KEYWORDS.md) is not available.
    '''
    for md in [keywords_md, keywords_cd_md]:
        if not os.path.exists(md):
            with open(md, 'w') as md_file:
                md_file.write('# Keyword Search Results\n')
                md_file.write('This file contains the results of keyword searches along with their corresponding IDs and the number of matches.\n\n')
                md_file.write('| ID | Keywords | Number of Results |\n')
                md_file.write('| -- | -------- | ----------------- |\n')


    if not os.path.exists(keywords_json):
        log_data = {
            'name': 'Keywords Log',
            'description': 'This log contains information about keyword searches and their corresponding results from the dataset between 2019 and 2022.',
            'database': '2019_2022.json',
            'log': []
        }
    else:
        with open(keywords_json, 'r') as json_file:
            log_data = json.load(json_file)


    '''
    Check to see if the keyword combination already exists.
    '''
    existing_entry = next((entry for entry in log_data['log'] if set(lowercase_strings_in_list(entry['keywords'])) == set(lowercase_strings_in_list(keywords))), None)
    if existing_entry:
        print(f"This combination of keywords is already saved in {json_name}.json.")
    else:
        output['id'] = len(log_data['log'])
        log_data['log'].append(output)

        # save the json file.
        with open(keywords_json, 'w', encoding='utf-8') as json_file:
            json.dump(log_data, json_file, indent=4, ensure_ascii=False)
            print(f'Data saved to {json_name}.json')

        # save the md file.
        for md in [keywords_md, keywords_cd_md]:
            with open(md, 'a') as md_file:
                md_file.write(f"| {output['id']} | {', '.join(keywords)} | {output['length']} |\n")
                print(f'Data is saved to {md_name}.md')


def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/preprocessed/with_content/2019_2022.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/preprocessed/keywords/2019_2022')
    parser.add_argument('--keywords', nargs='+')
    parser.add_argument('--save', default=False, action='store_true')
    args = parser.parse_args()

    sp_keywords = ' '.join(args.keywords) # Join the keywords with space.

    # Open the dataset
    with open(args.file_path, 'r') as F:
        data = json.load(F)

    # Get the articles by keywords.
    results = get_articles_by_keywords(data['data'], args.keywords)
    output = {'id': -1, 'name': sp_keywords, 'keywords': args.keywords, 'length': len(results), 'data': results}

    # Save
    if args.save:
        try:
            save_log(output, args.out_dir)
        except IOError as e:
            print(f"Error saving data: {e}")
    else:
        print(output['length'])


if __name__ == '__main__':
    main()