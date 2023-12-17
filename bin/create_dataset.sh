cd ~/news_timeline

poetry run python src/create.py \
    --raw_file_path "/mnt/mint/hara/datasets/news_category_dataset/raw_data/news_category_dataset_v3.json" \
    --root_dir "/mnt/mint/hara/datasets/news_category_dataset/dataset" \
    --start_year 2019 \
    --end_year 2022 \
    --th 0.6 \
    --min_sup 0.003 \
    --min_conf 0.6 \
    --k1 1.2 \
    --m "items >= 2" \
    --model_name "gpt-4-1106-preview" \
    --temp 0.8 \
    --min_docs 4 \
    --max_docs 8 \
    --top_tl 0.5 \
    --judgement "diff" \
    --alpha 0.8 \
    --th_2_diff 0.007 \
    --diff 7 \
    --split_n 1 \
    --temp_for_fake_news 0.8 \
    --setting "rep1"