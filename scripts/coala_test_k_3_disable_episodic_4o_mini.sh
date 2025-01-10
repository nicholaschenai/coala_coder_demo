# CoALA testing on MBPP plus dataset
small_model="gpt-4o-mini-2024-07-18"
large_model="gpt-4o-2024-08-06"
result_dir="results/coala_test_k_3_disable_episodic_4o_mini"

SCRIPT_DIR="$(dirname "$0")"
ROOT_DIR="$(git rev-parse --show-toplevel)"  # Get git root directory

PYTHONPATH="$ROOT_DIR" python "$SCRIPT_DIR/../main.py" \
--test_dataset_name MBPP_Plus \
--do_test --eval_later --use_public_tests \
--resume \
--result_dir $result_dir \
--agent_type coala \
--retrieval_top_k 3 \
--verbose \
--max_display_tests 10 --max_display_chars 1000 \
--clone_ckpt results/coala_train_apps_k_3_disable_episodic_4o_mini/ckpt \
--disable_episodic \
--model_name $small_model
# --debug_mode \
# --max_test_iter 20

evalplus.evaluate --dataset mbpp --samples "${result_dir}/samples.jsonl"

bash "$SCRIPT_DIR/postprocess.sh" "$result_dir"
