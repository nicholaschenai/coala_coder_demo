# CoALA training on APPS dataset
# Initialize with semantic memory (competitive programming textbooks)
# NOTE: uses the provided checkpoint in `final_results/comp_prog_sem/ckpt`
# this time we set k=2
small_model="gpt-4o-mini-2024-07-18"
large_model="gpt-4o-2024-08-06"
result_dir="results/coala_train_apps_k_2_4o_mini"

SCRIPT_DIR="$(dirname "$0")"
ROOT_DIR="$(git rev-parse --show-toplevel)"  # Get git root directory

PYTHONPATH="$ROOT_DIR" python "$SCRIPT_DIR/../main.py" \
--train_dataset_name APPS --dataset_type hf \
--do_train \
--load_train \
--resume \
--result_dir $result_dir \
--agent_type coala \
--retrieval_top_k 2 \
--verbose \
--max_display_tests 10 --max_display_chars 1000 \
--clone_ckpt final_results/comp_prog_sem/ckpt \
--model_name $small_model \
--max_train_iter 100  --save_every 20
# --max_train_iter 10  --save_every 5 \
# --debug_mode
# --no_skill_files \

bash "$SCRIPT_DIR/postprocess.sh" "$result_dir"
