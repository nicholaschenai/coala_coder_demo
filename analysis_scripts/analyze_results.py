"""
script to analyze results and generate plots for the report
"""
import os

import matplotlib.pyplot as plt

from typing import Optional

import agent_expt_suite.eval_utils.generic as g

from experiment_paths import EXPERIMENTS, SELECTED_TRAIN_EXPERIMENTS, ALL_TRAIN_EXPERIMENTS


def get_cumulative_success_rates(folder):
    """Get success rates for a folder or return placeholder data if folder doesn't exist"""
    try:
        data = g.get_successes_by_attempts(folder)
        mode = list(data.keys())[0]
        return data[mode]['cumulative_success_rate']
    except:
        print(f"Warning: Could not load data for {folder}, using placeholder")
        # Return placeholder data - 4 attempts with increasing success rate
        return [0 for i in range(4)]

def plot_experiment_success_rates(
        experiments_dict: Optional[dict] = None, 
        save_dir: str = 'report/assets', 
        save_name: str = 'success_rates_by_attempts.png', 
        y_axis_abs: bool = False
    ):
    """Create 2x2 plot of success rates by attempts for all experiments"""
    print("Plotting experiment success rates...")
    if experiments_dict is None:
        experiments_dict = EXPERIMENTS.copy()

    # Create 2x2 subplot
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.ravel()

    # Plot each experiment
    for idx, (exp_name, folders) in enumerate(experiments_dict.items()):
        ax = axes[idx]
        print(f"\n{exp_name}:")
        for model, folder in folders.items():
            print(f"\n{model}:")
            success_rates = get_cumulative_success_rates(folder)
            line = ax.plot(range(1, len(success_rates) + 1), success_rates, 
                   marker='o', label=model, linewidth=2,
                   linestyle='-' if model == '4o_0806' else '--')[0]
            
            # Add value labels next to each point
            for x, y in zip(range(1, len(success_rates) + 1), success_rates):
                ax.annotate(f'{y:.4f}', 
                          (x, y),
                          xytext=(0, 10),  # 5 points horizontal offset
                          textcoords='offset points',
                          va='center')
        
        ax.set_title(exp_name)
        ax.set_xlabel('Attempt')
        ax.set_ylabel('Cumulative Success Rate')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        
        # Set x-axis to show only integers
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        
        if y_axis_abs:
            ymin, ymax = 0, 1
        else:
            ymin, ymax = ax.get_ylim()
        # Add small padding to y-axis limits for better visualization
        padding = (ymax - ymin) * 0.05  # 5% padding
        # Add extra padding on right for value labels
        ax.set_ylim(ymin - padding, ymax + padding)
        ax.margins(x=0.15)  # Add horizontal padding for labels

    plt.tight_layout()
    
    # Create directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, save_name), bbox_inches='tight', dpi=300)
    plt.close()

def analyze_skill_library_usage(coala_experiments=None):
    """Analyze skill library usage for CoALA experiments"""
    if coala_experiments is None:
        coala_experiments = {k: v for k, v in EXPERIMENTS.items() if k.startswith('CoALA')}
    
    print("\nSkill Library Usage Analysis:")
    print("=" * 50)
    
    for exp_name, folders in coala_experiments.items():
        print(f"\n{exp_name}:")
        print("-" * 20)
        
        for model, folder in folders.items():
            try:
                raw_result = g.get_skill_library_usage(folder)
                mode = list(raw_result.keys())[0]
                results = raw_result[mode]
                print(f"\n{model}:")
                print(f"Total tasks: {results['total_tasks']}")
                print(f"Used in any attempt: {results['used_in_any_attempt']} ({results['used_in_any_attempt']/results['total_tasks']*100:.2f}%)")
                print(f"Used in last attempt: {results['used_in_last_attempt']} ({results['used_in_last_attempt']/results['total_tasks']*100:.2f}%)")
                print(f"Tasks using skills in any attempt: {results['used_in_any_attempt_tasks']}")
                print(f"Tasks using skills in last attempt: {results['used_in_last_attempt_tasks']}")
            except Exception as e:
                print(f"{model}: Could not analyze folder {folder} - {str(e)}")


if __name__ == "__main__":
    experiments_dict = EXPERIMENTS.copy()
    experiments_dict['CoALA Test'] = experiments_dict.pop('CoALA')
    experiments_dict.update(SELECTED_TRAIN_EXPERIMENTS)
    plot_experiment_success_rates(experiments_dict)

    coala_experiments = ALL_TRAIN_EXPERIMENTS.copy()
    coala_experiments['CoALA Test'] = EXPERIMENTS['CoALA']
    analyze_skill_library_usage(coala_experiments)
