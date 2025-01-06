# load competitive programming textbooks into semantic memory
SCRIPT_DIR="$(dirname "$0")"
ROOT_DIR="$(git rev-parse --show-toplevel)"  # Get git root directory
PYTHONPATH="$ROOT_DIR" python "$SCRIPT_DIR/../main.py" \
--load_db \
--memory_sources comp_prog \
--result_dir results/comp_prog_sem \
--agent_type coala \
--verbose \
--debug_mode
