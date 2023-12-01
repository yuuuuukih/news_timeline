# conda activate news_timeline_virtual_env
cd ~/news_timeline

# === Settings ===
# for BM25
THRESHOLD=0.5
K1=1.2
# for FP-growth
MIN_SUP=0.02
MIN_CONF=0.6

# === JSON file name ===
FP_GROWTH_ENTITIES_JSON="fp_growth_entities"
DOCUMENTS_JSON="documents"
ENTITIES_JSON="entities"
NO_FAKE_TIMELINES_JSON="no_fake_timelines"

# === Path ===
VERSION_DIR="/mnt/mint/hara/datasets/news_category_dataset/clustering/v3/"
FP_GROWTH_ENTITIES_PATH="${VERSION_DIR}${FP_GROWTH_ENTITIES_JSON}.json"
DOCUMENTS_PATH="${VERSION_DIR}${DOCUMENTS_JSON}.json"
ENTITIES_PATH="${VERSION_DIR}${ENTITIES_JSON}.json"

# === Run ===
echo "get_entities.py START"
python ./src/clustering/get_entities.py --out_dir $VERSION_DIR --min_sup $MIN_SUP --min_conf $MIN_CONF --th $THRESHOLD --k1 $K1 --json_file_name $FP_GROWTH_ENTITIES_JSON

cd ./src/create_dataset
echo "add_props_to_docs.py START"
python add_props_to_docs.py --out_dir $VERSION_DIR --entities_path $FP_GROWTH_ENTITIES_PATH --json_file_name $DOCUMENTS_JSON

echo "add_props_to_entities.py START"
python add_props_to_entities.py --out_dir $VERSION_DIR --file_path $FP_GROWTH_ENTITIES_PATH --docs_path $DOCUMENTS_PATH --json_file_name $ENTITIES_JSON

echo "generate_multiple_timelines.py START"
python generate_multiple_timelines.py \
    --out_dir $VERSION_DIR \
    --file_path $ENTITIES_PATH \
    --model_name "gpt-4" \
    --temp 0.8 \
    --min_docs 4 \
    --max_docs 8 \
    --top_tl 0.5 \
    --json_file_name $NO_FAKE_TIMELINES_JSON \
    --max_reexe_num 1


