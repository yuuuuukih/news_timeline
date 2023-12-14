from collections import Counter

def update_occurrences(original_dict: dict[str, int], new_occurrences: list[int]) -> dict[str, int]:
    def count_occurrences(lst: list[int]) -> dict[str, int]:
        return {str(k): v for k, v in sorted(Counter(lst).items())}

    def add_dicts(dict1: dict[str, int], dict2: dict[str, int]):
        result = dict1.copy()
        for key, value in dict2.items():
            if key in result.keys():
                result[key] += value
            else:
                result[key] = value

        sorted_result = {k: result[k] for k in sorted(result, key=int)}
        return sorted_result

    updated = add_dicts(original_dict, count_occurrences(new_occurrences))
    return updated

'''
original_dict = {
    '1': 1,
    '2': 1,
    '3': 2,
    '4': 1
}
new_occurrences = [2, 5, 10, 2, 4]
->
updated = {
    '1': 1,
    '2': 3,
    '3': 2,
    '4': 2,
    '5': 1,
    '10': 1
}
'''