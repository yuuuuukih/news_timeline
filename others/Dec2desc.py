import json

def main2():
    def correct_keys(d):
        if isinstance(d, dict):
            new_dict = {}
            for key, value in d.items():
                if key == 'short_Description':
                    new_key = 'short_description'
                else:
                    new_key = key
                new_dict[new_key] = correct_keys(value)  # 再帰的に値を処理
            return new_dict
        elif isinstance(d, list):
            # リストの中の辞書も処理するため、再帰的に処理
            return [correct_keys(item) for item in d]
        else:
            # その他のデータタイプは修正せずにそのまま返す
            return d

    # JSONファイルを読み込む
    with open('/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/input.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    # キーの修正を行う
    corrected_data = correct_keys(data)
    # 修正されたJSONファイルを書き出す
    with open('/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/corrected_file.json', 'w', encoding='utf-8') as file:
        json.dump(corrected_data, file, ensure_ascii=False, indent=4)