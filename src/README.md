# src directory

## Files
- create.py: The main file of this repository. The explanation of props is below.
- doc_length.py: You can check the data about the length of documents.
- statistics.py: You can check the top-30 of keyword groups and the number of fake news.

## create.py
Explain about important properties you can decide when executing create.py

- --raw_file_path: Path to the raw dataset file ([News Category Dataset](https://www.kaggle.com/datasets/rmisra/news-category-dataset?resource=download)).
- --root_dir: Path to the working directory.

- --start_year: Year in which the dataset range to be used starts.
- --end_year: Year in which the dataset range to be used ends.

- --th: Threshold for BM25.
- --min_sup: min sup for FP-growth.
- --min_conf: min conf for FP-growth.
- --k1: k1 value for BM25.

- --model_name: The model name of OpenAI GPT (e.g., gpt-4, gpt-4-1106-preview, gpt-3.5-turbo). You cannot use the different model in one execution (Refer to this model at the time of execution of all gpts, regardless of their use).
- --temp: Temperature for generating stories.
- --min_docs: The min number of documents in 1 timeline.
- --max_docs: The max number of documents in 1 timeline.
- --top_tl: $k_i \leq [[\frac{l_i}{n_{\max}}] * top_{tl}]$
- --judgement: Specifies the value to be used for the stop condition when adding a document to the timeline
    - (Default) diff: The difference of ROUGE-2 score ($R_{2, i+1} - R_{2, i}$ > th_2_diff).
    - rate: The ratio of ROUGE-2 score ($R_{2, i+1} / R_{2, i}$ > th_2_rate).
    - value: ROUGE-(1, 2, l) score ($R_{1, i}$ > th_1 or $R_{2, i}$ > th_2 or $R_{l, i}$ > th_l).
- --alpha: ROUGE score = 1/(alpha * (1/Precision) + (1 - alpha) * (1/Recall))
    - ref: [sumeval](https://github.com/chakki-works/sumeval)
- --diff: Only for dir name. (e.g., th_2_diff=0.007 -> 7, th_2_diff=0.006 -> 6)
- --split_n: This is used for community abstraction in src/create_dataset/split/split_dataset.py

- --temp_for_fake_news: Temperature for generating fake news.
- --setting: The setting of fake news (e.g., replacing+3, inserting+1, ...).

