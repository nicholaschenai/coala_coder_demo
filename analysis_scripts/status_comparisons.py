"""
script to get pairwise status comparisons (correct in 1 and wrong in the other) and save them
"""
import logging

from pprint import pp

from agent_expt_suite.eval_utils.experiment_config import ExperimentConfig
from agent_expt_suite.eval_utils.run_single_comparison import run_single_comparison

from experiment_paths import EXPERIMENTS

logger = logging.getLogger(__name__)


def setup_logging(log_level: str = "INFO") -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('log_files/multi_experiment_analysis.log')
        ]
    )

if __name__ == "__main__":
    setup_logging()
    output_dir = "./report/analysis_outputs"

    expt_cfg = ExperimentConfig(
        experiment_paths=EXPERIMENTS, 
        output_dir = output_dir
    )
    comparisons = expt_cfg.get_all_comparisons()
    
    for comparison in comparisons:
        pp(comparison)
        run_single_comparison(comparison)

    