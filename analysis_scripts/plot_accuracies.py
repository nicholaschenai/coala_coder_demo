"""
Script to plot accuracy comparisons across different methods and models.
Uses the EXPERIMENTS dictionary to load results from different experiment paths.
"""
import os

import matplotlib.pyplot as plt

from typing import Dict, Tuple, Any

from agent_expt_suite.eval_utils.mbpp_plus import calculate_accuracy, get_overall_status

from cognitive_base.utils import load_json

from experiment_paths import EXPERIMENTS

def load_experiment_results(model: str) -> Tuple[Dict[str, float], Dict[str, Any]]:
    """
    Load results for all methods for a given model
    
    Args:
        model: Model name (e.g., '4o_mini', '4o_0806')
        
    Returns:
        Tuple containing:
            - Dictionary mapping method names to accuracy values
            - Dictionary mapping method names to full evaluation results
    """
    results = {}
    eval_results = {}
    
    # Zero shot (hardcoded results)
    # Both models have the same result: 273/378 = 0.722
    results['zero_shot'] = 0.722
    
    # Load results for other methods from experiment paths
    for method in ['ReAct', 'RAG', 'CoALA']:
        if model in EXPERIMENTS[method]:
            folder_path = EXPERIMENTS[method][model]
            try:
                method_results = load_json(f'{folder_path}/samples_eval_results.json')
                results[method] = calculate_accuracy(method_results)
                eval_results[method] = method_results
            except (FileNotFoundError, KeyError) as e:
                print(f"Warning: Could not load results for {method} - {model}: {e}")
                results[method] = 0.0
    
    return results, eval_results

def plot_accuracies() -> Dict[str, Dict[str, Any]]:
    """
    Plot accuracy comparison for all methods and models
    
    Returns:
        Dictionary mapping models to dictionaries of evaluation results by method
    """
    models = ['4o_mini', '4o_0806']
    methods = ['zero_shot', 'ReAct', 'RAG', 'CoALA']
    
    # Hardcoded counts for zero-shot (both models have the same result)
    zero_shot_counts = {model: (273, 378) for model in models}  # (correct, total)
    
    # Collect all results
    all_results = {}
    all_eval_results = {}  # Store eval results for later comparison
    
    for model in models:
        all_results[model], eval_results = load_experiment_results(model)
        all_eval_results[model] = eval_results
    
    # Create plot
    plt.figure(figsize=(12, 7))
    bar_width = 0.2
    
    # Calculate positions for bars
    n_methods = len(methods)
    n_models = len(models)
    group_width = bar_width * n_methods
    group_positions = [i for i in range(n_models)]
    
    for i, method in enumerate(methods):
        accuracies = []
        for model in models:
            if method in all_results[model]:
                accuracies.append(all_results[model][method] * 100)
            else:
                accuracies.append(0)  # No data available
                
        # Calculate bar positions relative to group center
        bar_positions = [x - group_width/2 + bar_width * (i + 0.5) for x in group_positions]
        
        bars = plt.bar(bar_positions, accuracies, bar_width, 
                      label=method)
        
        # Add accuracy labels with counts on bars
        for j, (model, bar) in enumerate(zip(models, bars)):
            if method == 'zero_shot':
                correct, total = zero_shot_counts[model]
                acc = accuracies[j]
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                        f'{correct}/{total}\n({acc:.1f}%)', 
                        ha='center', va='bottom', fontsize=9)
            elif method in all_eval_results[model]:
                results = all_eval_results[model][method]
                total = len(results['eval'])
                correct = sum(1 for v in results['eval'].values() 
                            if get_overall_status([v[0]['base_status'], v[0]['plus_status']]) == 'pass')
                
                acc = accuracies[j]
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                        f'{correct}/{total}\n({acc:.1f}%)', 
                        ha='center', va='bottom', fontsize=9)
    
    plt.title('Model Performance by Method')
    plt.ylabel('Accuracy (%)')
    plt.xlabel('Model')
    plt.xticks(group_positions, [m.replace('_', ' ').upper() for m in models])
    plt.ylim(0, 100)  # Set y-axis from 0 to 100%
    
    # Add grid lines for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust legend position to avoid overlapping
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Adjust layout to accommodate legend
    plt.tight_layout()
    
    # Create reports/assets directory if it doesn't exist
    os.makedirs('report/assets', exist_ok=True)
    plt.savefig('report/assets/accuracy_comparison.png', bbox_inches='tight')
    plt.close()
    
    return all_eval_results


if __name__ == "__main__":
    eval_results = plot_accuracies()
