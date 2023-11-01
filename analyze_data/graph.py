import os
import json
from tqdm import tqdm
import random
from argparse import ArgumentParser

import networkx as nx
import matplotlib.pyplot as plt


class TimelinesAnalyzer:
    def __init__(self, timelines_data) -> None:
        self.G = nx.Graph()
        self.timelines_data = timelines_data
        self.N = len(self.timelines_data)

        self.load(self.timelines_data)

    def get_node_name(self, entity):
        return f"{entity['entity_ID']}"
        # return f"{entity['entity_ID']}: {entity['entity_items']}"

    def load(self, timelines):
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


def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/no_fake_timelines.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/')
    parser.add_argument('--json_file_name', default='no_fake_timelines')
    args = parser.parse_args()

    with open(args.file_path, 'r') as F:
        timelines = json.load(F)

    # ta = TimelinesAnalyzer(timelines['data'])
    # ta.show()
    TimelinesAnalyzer.minimum_cut(timelines['data'])

if __name__ == '__main__':
    main()

# https://www.dogrow.net/python/blog47/