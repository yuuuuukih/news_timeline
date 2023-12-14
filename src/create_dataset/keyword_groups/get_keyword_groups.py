import sys
import copy

from create_dataset.keyword_groups.text_process.preprocess import TextProcessor
from create_dataset.keyword_groups.fp_growth.fp_growth import fp_growth
from create_dataset.type.documents import Documents
from create_dataset.type.entities import Entities

class KeywordGroupsGetter:
    def __init__(
            self, preprocessed_data: dict,
            th: float, min_sup: float, min_conf: float, k1: float,
            rm_stopwords: bool, lemmatize: bool, rm_single_char: bool, rm_non_noun_verb: bool, rm_non_noun: bool, rm_duplicates: bool, tfidf: bool, bm25: bool,
            m:  str, max_for_removed_words: int, table_show: bool
        ) -> None:
        self.preprocessed_data = preprocessed_data
        self.th = th
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.k1 = k1
        self.rm_stopwords = rm_stopwords
        self.lemmatize = lemmatize
        self.rm_single_char = rm_single_char
        self.rm_non_noun_verb = rm_non_noun_verb
        self.rm_non_noun = rm_non_noun
        self.rm_duplicates = rm_duplicates
        self.tfidf = tfidf
        self.bm25 = bm25
        self.m = m
        self.max_for_removed_words = max_for_removed_words
        self.table_show = table_show

        # get keyword groups (entities)
        self.corpus: list[str] = [f"{doc['headline']} {doc['short_description']}" for doc in self.preprocessed_data['data']]
        self._process_data()
        self._add_props_to_fp_growth_keyword_groups()

    def _process_data(self):
        '''
        Process data
        '''
        # Instantiation and tokenize
        tp = TextProcessor(self.corpus)

        # Lemmatize
        if self.lemmatize:
            tp.lemmatize()

        # Remove stop words
        if self.rm_stopwords:
            tp.remove_stop_words()

        # Remove single character
        if self.rm_single_char:
            tp.remove_single_character()

        # Remove non noun and verb
        if self.rm_non_noun_verb:
            tp.remove_non_noun_verb()

        # Remove non noun
        if self.rm_non_noun:
            tp.remove_non_noun()

        # TF-IDF
        if self.tfidf:
            removed_words = tp.tfidf(threshold=self.th, show_removed_wods=False, num_of_words_to_display=self.max_for_removed_words)

        # Okapi BM25
        if self.bm25:
            removed_words = tp.bm25(threshold=self.th, k1=self.k1, show_removed_wods=False, num_of_words_to_display=self.max_for_removed_words)

        # Remove dupulicates
        if self.rm_duplicates:
            tp.remove_dupulicates()

        # Add doc ID
        corpus_with_docID = tp.add_doc_id(tp.tokenized_corpus)

        # FP-growth
        output = fp_growth(corpus_with_docID, min_support=self.min_sup, min_confidence=self.min_conf, show=self.table_show)

        # Filter
        filtered_output = []
        for entities in output:
            # --m examples: "items >= 2", "items >= 2 and freq < 50"
            if len(entities['items']) >= 2:
                filtered_output.append(entities)

        # 1. Sort the words in alphabetical order
        for entities in filtered_output:
            entities['items'].sort()
        # 2. Sort firstly in the order of words, and then in the order of frequency
        sorted_output = sorted(filtered_output, key=lambda x: (x['freq'], x['items']))
        # 3. Assign entity_id
        for i, entities in enumerate(sorted_output):
            entities['ID'] = i

        # Produciton
        formatted_output = {
            "preprocess": {
                "Remove stop words": self.rm_stopwords,
                "Lemmatize": self.lemmatize,
                "Remove single character": self.rm_single_char,
                "Remove non noun and verb": self.rm_non_noun_verb,
                "Remove non noun": self.rm_non_noun,
                "Remove dupulicates": self.rm_duplicates,
                "TF-IDF": self.tfidf,
                "Okapi BM25": self.bm25
            },
            "hparms": {
                "threshold": self.th,
                "min_support": self.min_sup,
                "min_confidence": self.min_conf,
                "k1": None if self.bm25 == False else self.k1
            },
            "words_removed_by_Okapi_BM25_TF_IDF": {
                "The_number_of_words": len(removed_words),
                "list": removed_words
            },
            "entities": {
                "comments": self.m,
                "entities_num": {
                    'sum': len(filtered_output),
                    'distribution': {}
                },
                "list": sorted_output
            }
        }

        self.fp_growth_keyword_groups = {
            'name': 'Keyword Groups',
            'description': 'This file contains the results of FP-growth with hyper parameters.',
            'year': f"{self.preprocessed_data['range']['start_year']}-{self.preprocessed_data['range']['end_year']}",
            'The_number_of_documents': self.preprocessed_data['length'],
            'category': {},
            'data': [formatted_output]
        }

    def _count_elements(self, list) -> dict[str, int]:
        count_dict = {}
        for item in list:
            if str(item) not in count_dict.keys():
                count_dict[str(item)] = list.count(item)
        return count_dict

    def _add_props_to_fp_growth_keyword_groups(self):
        preprocessed_data: Documents = copy.deepcopy(self.preprocessed_data)
        data_list = preprocessed_data['data']
        fp_growth_keyword_groups: Entities = copy.deepcopy(self.fp_growth_keyword_groups)
        entities_list = fp_growth_keyword_groups['data'][0]['entities']['list']

        '''
        ID prop
        '''
        for i, doc in enumerate(data_list):
            doc['ID'] = i

        '''
        preprocessed_tokens prop
        '''
        # Preprocess
        tp = TextProcessor(self.corpus)
        tp.lemmatize()
        tp.remove_stop_words()
        tp.remove_single_character()
        tp.remove_non_noun()
        #NO BM25
        tp.remove_dupulicates()
        for doc, tokenized_doc in zip(data_list, tp.tokenized_corpus):
            doc['preprocessed_tokens'] = tokenized_doc

        '''
        entities_info prop
        '''
        for doc in data_list:
            entities_info_prop = {'num': -1, 'IDs': [], 'entities': []}
            for entities in entities_list:
                if set(entities['items']) <= set(doc['preprocessed_tokens']):
                    entities_info_prop['IDs'].append(entities['ID'])
                    entities_info_prop['entities'].append(entities['items'])
            entities_info_prop['num'] = len(entities_info_prop['IDs'])
            doc['entities_info'] = entities_info_prop

        '''
        Analytics prop
        '''
        category_list = []
        entities_num_list = []
        for doc in data_list:
            category_list.append(doc['category'])
            entities_num_list.append(doc['entities_info']['num'])

        preprocessed_data['analytics'] = {
            'category': self._count_elements(category_list),
            'entities_num': {k: v for k, v in sorted(self._count_elements(entities_num_list).items(), key=lambda item: int(item[0]))}
        }
        fp_growth_keyword_groups['category'] = self._count_elements(category_list)
        fp_growth_keyword_groups['data'][0]['entities']['entities_num']['distribution'] = {k: v for k, v in sorted(self._count_elements(entities_num_list).items(), key=lambda item: int(item[0]))}

        '''
        docs_info prop
        '''
        for entities in entities_list:
            docs_info_prop = {'IDs': [], 'docs': []}
            my_entity_ID = entities['ID']

            for doc in preprocessed_data['data']:
                if my_entity_ID in doc['entities_info']['IDs']:
                    """
                    今回の場合は、documents.json時に、documentのIDをdateが新しい順（降順）となってしまっているため、
                    entities.jsonにする際に、entity毎のdocumentを昇順に並べ替える。
                    """
                    docs_info_prop['IDs'].insert(0, doc['ID'])
                    docs_info_prop['docs'].insert(0, doc)

            # validation
            if entities['freq'] != len(docs_info_prop['IDs']):
                sys.exit('数があっていません！')

            entities['docs_info'] = docs_info_prop

        # Set
        self.keyword_groups = fp_growth_keyword_groups

    def get_fp_growth_keyword_groups(self):
        return self.fp_growth_keyword_groups

    def get_keyword_groups(self):
        return self.keyword_groups
