import sys
import json
from tqdm import tqdm
import random

import networkx as nx
import matplotlib.pyplot as plt

from typing import Literal
from create_dataset.type.no_fake_timelines import NoFakeTimeline, EntityTimelineData
from create_dataset.type.split_dataset import SplitDataset, ComInfo


class TimelinesSplitter:
    def __init__(self, timelines: NoFakeTimeline) -> None:
        self.G = nx.Graph()
        self.timelines = timelines
        self.timelines_data: list[EntityTimelineData] = timelines['data']
        self.N = len(self.timelines_data)

        self.load(self.timelines_data)

    def get_node_name(self, entity: EntityTimelineData) -> str:
        return f"{entity['entity_ID']}"

    def load(self, timelines: list[EntityTimelineData]):
        # Add nodes
        for entity in timelines:
            self.G.add_node(self.get_node_name(entity))
        # Add edges
        print('Now adding edges...')
        for i in tqdm(range(self.N)):
            for j in range(i+1, self.N):
                common_ids = len(set(timelines[i]['docs_info']['IDs']).intersection(set(timelines[j]['docs_info']['IDs'])))
                if common_ids > 0:
                    self.G.add_edge(self.get_node_name(timelines[i]), self.get_node_name(timelines[j]), weight=common_ids)
        print('Loding has finished.')

    def show(self):
        plt.figure(figsize=(10,10))
        pos = nx.spring_layout(self.G, k=0.2)
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw(self.G, pos, with_labels=True, node_size=700, node_color='skyblue', width=[2 if w > 0 else 1 for w in labels.values()])
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)
        plt.show()
        plt.savefig('test.jpg')
        print('Graph has showed')

    @classmethod
    def minimum_cut(cls, data):
        # Create a graph and load the data
        custom_graph = cls(data)
        # Remove nodes with no edges
        nodes_to_remove = [node for node in custom_graph.G.nodes if custom_graph.G.degree[node] == 0]
        custom_graph.G.remove_nodes_from(nodes_to_remove)
        # Randomly select 2 nodes as s and t
        nodes = list(custom_graph.G.nodes)
        s, t = random.sample(nodes, 2)
        '''
        (s, t) = (219, 226)
        '''
        # Calculate the minimum cut
        cut_value, partition = nx.minimum_cut(custom_graph.G, s, t, capacity="weight")
        # Get the nodes in the resulting partitions
        left_partition, right_partition = partition
        intersection = set(left_partition).intersection(set(right_partition))
        print(f"s: {s} | t: {t}")
        print(f"Removed: {len(nodes_to_remove)} | left: {len(left_partition)} | right: {len(right_partition)} | intersection: {len(intersection)}")

    def set_split_n(self, n: int):
        self.n = n

    def community(self):
        # Create a graph and load the data
        # custom_graph = cls(data)

        communities = list(nx.community.girvan_newman(self.G))
        communities = self._merge_single_element_sets(communities[self.n])

        node_colors = self._create_community_node_colors(self.G, communities)
        modularity = round(nx.community.modularity(self.G, communities), 6)

        plt.figure(figsize=(10,10))
        pos = nx.spring_layout(self.G, k=0.2) # k=0.17, 0.2
        labels = nx.get_edge_attributes(self.G, 'weight')
        title = f"Community Visualization of {len(communities)} communities with modularity of {modularity}"
        plt.title(title, fontsize=16)
        nx.draw(
            self.G,
            pos=pos,
            node_size=700,
            node_color=node_colors,
            with_labels=True,
            # font_size=20,
            font_color="black",
        )
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)
        plt.legend()
        plt.savefig(f'community_{self.n}.jpg')

        return communities

    # function to create node colour list
    def _create_community_node_colors(self, graph, communities):
        number_of_colors = len(communities[0])
        # colors = ["#D4FCB1", "#CDC5FC", "#FFC2C4", "#F2D140", "#BCC6C8"][:number_of_colors]
        colors = ["#ff9999", "#cc99ff", "#99ffff", "#ccff99", "#ff99cc", "#9999ff", "#99ffcc", "#ffff99", "#ff99ff", "#99ccff", "#99ff99", "#ffcc99"][:number_of_colors]
        node_colors = []
        for node in graph:
            current_community_index = 0
            for community in communities:
                if node in community:
                    node_colors.append(colors[current_community_index])
                    break
                current_community_index += 1
        return node_colors

    def _merge_single_element_sets(self, data):
        single_elements = {el for subset in data for el in subset if len(subset) == 1}
        other_elements = [subset for subset in data if len(subset) > 1]
        return tuple(other_elements + [single_elements])

    def get_community_info(self, communities) -> ComInfo:
        com_info: ComInfo = []
        for i, com in enumerate(communities):
            com = list(com)
            ent_num = len(com)

            ent_ids = []
            docs_ids = []
            total_num = 0
            for id in com:
                for entity_data in self.timelines_data:
                    entity_id = entity_data['entity_ID']
                    if int(id) == entity_id:
                        ent_ids.append(entity_id)
                        docs_ids.extend(entity_data['docs_info']['IDs'])
                        num_tl = entity_data['timeline_info']['timeline_num']
                        break
                total_num += num_tl
            # com_info.append({'com_id': i, 'ent_num': ent_num, 'timeline_num': total_num})
            com_info.append({'com_id': i, 'ent_num': ent_num, 'timeline_num': total_num, 'ent_ids': ent_ids, 'docs_ids': docs_ids})

        for one_com_info in com_info:
            print(f"{one_com_info['com_id']}: {one_com_info['ent_num']} entities, {one_com_info['timeline_num']} timelines")

        return com_info

    # 良いアルゴリズムを実装できなかったため、best_split_pattern_com_idをこちらが定数として定義する。
    def _get_best_split_pattern(self, com_info: ComInfo, diff: int) -> dict[Literal['train', 'val', 'test'], list[int]]:
        com_ids = [com['com_id'] for com in com_info]
        if diff == 7:
            com_ids_for_train = [1]
            com_ids_for_val = [0]
            com_ids_for_test = list(set(com_ids) - set(com_ids_for_train) - set(com_ids_for_val))
        if diff == 6:
            com_ids_for_train = [1]
            com_ids_for_val = [2, 3] if self.n == 1 else [3, 4] if self.n == 2 else [4, 5]
            com_ids_for_test = list(set(com_ids) - set(com_ids_for_train) - set(com_ids_for_val))
        best_split_pattern_com_id = {
            'train': com_ids_for_train,
            'val': com_ids_for_val,
            'test': com_ids_for_test
        }
        return best_split_pattern_com_id

    def _get_dataset_for_what(self, ent_ids: dict[str, list[int]], what=Literal['train', 'val', 'test']) -> SplitDataset:
        ent_ids_for_what = ent_ids[what]
        what_json: SplitDataset = {
            'name': f"{what}_dataset of {self.timelines['name']}",
            'description': f"{self.timelines['description']}",
            'entities_num': len(ent_ids_for_what),
            'timelines_num': 0,
            'split_n': self.n,
            'setting': self.timelines['setting'],
            'data': []
        }
        for entity_id in sorted(ent_ids_for_what):
            for entity_data in self.timelines_data:
                if entity_id == entity_data['entity_ID']:
                    what_json['data'].append(entity_data)
                    break
        return what_json

    def _delete_documents(self, intersection_docs_ids: list[int], what1_json: SplitDataset, what2_json: SplitDataset, min_docs: int = 4):
        print(f"{intersection_docs_ids=} -> ")
        for doc_id_1_2 in intersection_docs_ids:
            ent_id_1 = []
            for entity_data in what1_json['data']:
                if doc_id_1_2 in  entity_data['docs_info']['IDs']:
                    ent_id_1.append(entity_data['entity_ID'])

            ent_id_2 = []
            for entity_data in what2_json['data']:
                if doc_id_1_2 in  entity_data['docs_info']['IDs']:
                    ent_id_2.append(entity_data['entity_ID'])

            print(f"ent_id_1: {ent_id_1} | ent_id_2: {ent_id_2}")

            '''
            共通するdocumentを持つkeyword groups (entities)の数が同じ場合は、全体のデータ数が多い方から削除する。
            異なる場合は、共通するdocumentを持つkeyword groups (entities)の数が少ない方から削除する。
            '''
            if len(ent_id_1) == len(ent_id_2) == 1:
                target_what_json = what2_json if len(what1_json['data']) < len(what2_json['data']) else what1_json
            elif len(ent_id_1) == 1:
                target_what_json = what1_json
            elif len(ent_id_2) == 1:
                target_what_json = what2_json
            else:
                sys.exit('Error: len(ent_id_1) != 1 and len(ent_id_2) != 1')

            for entity_data in target_what_json['data']:
                # if keyword groups (entities) has the common document, delete it from the timeline.
                if doc_id_1_2 in entity_data['docs_info']['IDs']:
                    timeline_num = entity_data['timeline_info']['timeline_num']
                    for timeline_data in entity_data['timeline_info']['data']:
                        for doc in timeline_data['timeline']:
                            if doc['ID'] == doc_id_1_2:
                                timeline_data['timeline'].remove(doc)
                                entity_data['docs_info']['IDs'].remove(doc_id_1_2)
                                print(f"Delete a document (doc_id={doc_id_1_2}) from a timeline (entity_id={entity_data['entity_ID']})")
                                break
                        # if the number of documents in the timeline is less than min_docs, delete the timeline.
                        if len(timeline_data['timeline']) < min_docs:
                            entity_data['timeline_info']['data'].remove(timeline_data)
                            timeline_num -= 1
                            entity_data['timeline_info']['timeline_num'] -= 1
                            print(f"Delete a timeline (entity_id={entity_data['entity_ID']})")
                    # if the number of timelines in the keyword groups (entities) is 0, delete the keyword groups (entities).
                    if timeline_num == 0:
                        target_what_json['data'].remove(entity_data)
                        print(f"Delete a keyword group (entity_id={entity_data['entity_ID']})")

        return what1_json, what2_json

    def get_split_dataset(self, com_info: ComInfo, out_dir: str, diff: int, min_docs: int = 4, save_flaf: bool = True):
        best_split_pattern_com_id = self._get_best_split_pattern(com_info, diff)

        ent_ids = {
            'train': [],
            'val': [],
            'test': []
        }
        docs_ids = {
            'train': [],
            'val': [],
            'test': []
        }
        # Classify entity_id and docs_id into train, val, and test
        for what in ['train', 'val', 'test']:
            com_ids_for_what = best_split_pattern_com_id[what]
            ent_ids_for_what = ent_ids[what]
            docs_ids_for_what = docs_ids[what]
            for com_id in com_ids_for_what:
                for com in com_info:
                    if com['com_id'] == com_id:
                        ent_ids_for_what.extend(com['ent_ids'])
                        docs_ids_for_what.extend(com['docs_ids'])
                        break

        # Get the common documents
        intersection_docs_ids_all = list(set(docs_ids['train']).intersection(set(docs_ids['val'])).intersection(set(docs_ids['test'])))
        intersection_docs_ids_train_val = list(set(docs_ids['train']).intersection(set(docs_ids['val'])) - set(intersection_docs_ids_all))
        intersection_docs_ids_train_test = list(set(docs_ids['train']).intersection(set(docs_ids['test'])) - set(intersection_docs_ids_all))
        intersection_docs_ids_val_test = list(set(docs_ids['val']).intersection(set(docs_ids['test'])) - set(intersection_docs_ids_all))
        # print(f'intersection_docs_ids_train_val: {intersection_docs_ids_train_val}')
        # print(f'intersection_docs_ids_train_test: {intersection_docs_ids_train_test}')
        # print(f'intersection_docs_ids_val_test: {intersection_docs_ids_val_test}')
        # print(f'intersection_docs_ids_all: {intersection_docs_ids_all}')
        if len(intersection_docs_ids_all) != 0:
            sys.exit('Error: intersection_docs_ids_all is not empty.')

        train_json: SplitDataset = self._get_dataset_for_what(ent_ids, 'train')
        val_json: SplitDataset = self._get_dataset_for_what(ent_ids, 'val')
        test_json: SplitDataset = self._get_dataset_for_what(ent_ids, 'test')

        train_json, val_json = self._delete_documents(intersection_docs_ids_train_val, train_json, val_json, min_docs)
        train_json, test_json = self._delete_documents(intersection_docs_ids_train_test, train_json, test_json, min_docs)
        val_json, test_json = self._delete_documents(intersection_docs_ids_val_test, val_json, test_json, min_docs)

        # Update entities_num and timelines_num
        for what_json in [train_json, val_json, test_json]:
            what_json['entities_num'] = len(what_json['data'])
            what_json['timelines_num'] = sum([entity_data['timeline_info']['timeline_num'] for entity_data in what_json['data']])

        # Save
        if save_flaf:
            for what in ['train', 'val', 'test']:
                with open(f"{out_dir}/{what}.json", 'w') as F:
                    json.dump(eval(f"{what}_json"), F, indent=4, ensure_ascii=False, separators=(',', ': '))
                    print(f"Data is saved to {what}.json")


# def main():
#     parser = ArgumentParser()
#     parser.add_argument('--root_dir', default='/mnt/mint/hara/datasets/news_category_dataset/dataset/')
#     parser.add_argument('--diff', default=7, type=int)
#     parser.add_argument('--n', default=0, type=int)
#     parser.add_argument('--min_docs', default=4, type=int)
#     parser.add_argument('--do_not_save_split', default=True, action='store_false')
#     args = parser.parse_args()

#     file_path = os.path.join(args.root_dir, f"diff{args.diff}", f"timeline_diff{args.diff}.json")
#     out_dir = os.path.join(args.root_dir, f"diff{args.diff}")
#     with open(file_path, 'r') as F:
#         timelines: NoFakeTimeline = json.load(F)

    # ts = TimelinesSplitter(timelines)
    # ta.show()
    # TimelinesSplitter.minimum_cut(timelines['data'])
    # ts.set_split_n(args.n)
    # communities = ts.community()
    # print(communities)
    # com_info = ts.get_community_info(communities)
    # ts.get_split_dataset(com_info, out_dir, args.diff, args.min_docs, args.do_not_save_split)

# https://www.dogrow.net/python/blog47/