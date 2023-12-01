import sys
import json
from tqdm import tqdm
import random
from argparse import ArgumentParser

import networkx as nx
import matplotlib.pyplot as plt

sys.path.append('../')
from type.no_fake_timelines import NoFakeTimeline, EntityTimelineData

class TimelinesAnalyzer:
    def __init__(self, timelines_data: list[EntityTimelineData]) -> None:
        self.G = nx.Graph()
        self.timelines_data = timelines_data
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

    @classmethod
    def community(cls, data: list[EntityTimelineData], n=0):
        # Create a graph and load the data
        custom_graph = cls(data)

        communities = list(nx.community.girvan_newman(custom_graph.G))
        communities = custom_graph.merge_single_element_sets(communities[n])

        node_colors = custom_graph.create_community_node_colors(custom_graph.G, communities)
        modularity = round(nx.community.modularity(custom_graph.G, communities), 6)

        plt.figure(figsize=(10,10))
        pos = nx.spring_layout(custom_graph.G, k=0.2) # k=0.17, 0.2
        labels = nx.get_edge_attributes(custom_graph.G, 'weight')
        title = f"Community Visualization of {len(communities)} communities with modularity of {modularity}"
        plt.title(title, fontsize=16)
        nx.draw(
            custom_graph.G,
            pos=pos,
            node_size=700,
            node_color=node_colors,
            with_labels=True,
            # font_size=20,
            font_color="black",
        )
        nx.draw_networkx_edge_labels(custom_graph.G, pos, edge_labels=labels)
        plt.legend()
        plt.savefig(f'community_{n}.jpg')

        return communities

    # function to create node colour list
    def create_community_node_colors(self, graph, communities):
        number_of_colors = len(communities[0])
        # colors = ["#D4FCB1", "#CDC5FC", "#FFC2C4", "#F2D140", "#BCC6C8"][:number_of_colors]
        colors = ["#D4FCB1", "#CDC5FC", "#FFC2C4", "#F2D140", "#BCC6C8", "#FFCC99", "#FFCCCC", "#CCCCFF", "#CCFFCC", "#99FFCC"][:number_of_colors]
        node_colors = []
        for node in graph:
            current_community_index = 0
            for community in communities:
                if node in community:
                    node_colors.append(colors[current_community_index])
                    break
                current_community_index += 1
        return node_colors

    def merge_single_element_sets(self, data):
        single_elements = {el for subset in data for el in subset if len(subset) == 1}
        other_elements = [subset for subset in data if len(subset) > 1]
        return tuple(other_elements + [single_elements])



def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/no_fake_timelines.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/')
    parser.add_argument('--n', default=0, type=int)
    args = parser.parse_args()

    with open(args.file_path, 'r') as F:
        timelines: NoFakeTimeline = json.load(F)

    # ta = TimelinesAnalyzer(timelines['data'])
    # ta.show()
    # TimelinesAnalyzer.minimum_cut(timelines['data'])
    communities = TimelinesAnalyzer.community(timelines['data'], n=args.n)
    # print(communities)
    # for i in range(len(communities)):
    #         print(f"{i+1}. {len(communities[i])}")
    com_info = []
    for com in communities:
        com = list(com)
        ent_num = len(com)
        total_num = 0
        for id in com:
            for entity_data in timelines['data']:
                entity_id = entity_data['entity_ID']
                if int(id) == entity_id:
                    num_tl = entity_data['timeline_info']['timeline_num']
                    break
            total_num += num_tl
        com_info.append({'num': ent_num, 'timeline_num': total_num})

    print(com_info)




if __name__ == '__main__':
    main()

# https://www.dogrow.net/python/blog47/