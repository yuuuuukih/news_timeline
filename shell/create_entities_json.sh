cd ~/news_timeline

# Settings
THRESHOLD=0.5
MIN_SUP=0.02
MIN_CONF=0.6
K1=1.2

# JSON file name
FP_GROWTH_ENTITIES_JSON="fp_growth_entities"
DOCUMENTS_JSON="documents"

# Path
VERSION_DIR="/mnt/mint/hara/datasets/news_category_dataset/clustering/v2/"
FP_GROWTH_ENTITIES_PATH="${VERSION_DIR}${FP_GROWTH_ENTITIES_JSON}.json"
DOCUMENTS_PATH="${VERSION_DIR}${DOCUMENTS_JSON}.json"

# Run
echo "get_entities.py START"
python ./clustering/get_entities.py --out_dir $VERSION_DIR --min_sup $MIN_SUP --min_conf $MIN_CONF --th $THRESHOLD --k1 $K1

cd create_dataset
echo "add_props_to_docs.py START"
python add_props_to_docs.py --out_dir $VERSION_DIR --entities_path $FP_GROWTH_ENTITIES_PATH

echo "add_props_to_entities.py START"
python add_props_to_entities.py --out_dir $VERSION_DIR --file_path $FP_GROWTH_ENTITIES_PATH --docs_path $DOCUMENTS_PATH
