import os
import json
from tqdm import tqdm
from argparse import ArgumentParser

# import matplotlib
# matplotlib.use('TkAgg')

import networkx as nx
import matplotlib.pyplot as plt

# import tkinter as Tk

# la = Tk.Label(None, text='Hello World!', font=('Times', '18'))
# la.pack()
# la.mainloop()

class TimelinesAnalyzer:
    def __init__(self, timelines_data) -> None:
        self.G = nx.Graph()
        self.timelines_data = timelines_data
        self.N = len(self.timelines_data)

        self.load(self.timelines_data)

    def get_node_name(self, entity):
        return f"{entity['entity_ID']}: {entity['entity_items']}"

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
        pos = nx.spring_layout(self.G)
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw(self.G, pos, with_labels=True, node_size=700, node_color='skyblue', width=[2 if w > 0 else 1 for w in labels.values()])
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)
        plt.show()
        print('Graph has showed')

def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/no_fake_timelines_old3.json')
    parser.add_argument('--out_dir', default='/mnt/mint/hara/datasets/news_category_dataset/clustering/v1/')
    parser.add_argument('--json_file_name', default='no_fake_timelines')
    args = parser.parse_args()

    with open(args.file_path, 'r') as F:
        timelines = json.load(F)

    ta = TimelinesAnalyzer(timelines['data'])
    ta.show()

if __name__ == '__main__':
    main()

# https://www.dogrow.net/python/blog47/