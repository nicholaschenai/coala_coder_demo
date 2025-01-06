# ReAct, still uses coala agent architecture but no memory
small_model="gpt-4o-mini-2024-07-18"
large_model="gpt-4o-2024-08-06"
result_dir="results/react_test_4o_0806"

SCRIPT_DIR="$(dirname "$0")"
ROOT_DIR="$(git rev-parse --show-toplevel)"  # Get git root directory

PYTHONPATH="$ROOT_DIR" python "$SCRIPT_DIR/../main.py" \
--test_dataset_name MBPP_Plus \
--do_test --eval_later --use_public_tests \
--resume \
--result_dir $result_dir \
--agent_type react \
--retrieval_top_k 3 \
--verbose \
--max_display_tests 10 --max_display_chars 1000 \
--model_name $large_model
# --debug_mode \
# --max_test_iter 20

evalplus.evaluate --dataset mbpp --samples "${result_dir}/samples.jsonl"

bash "$SCRIPT_DIR/postprocess.sh" "$result_dir"
