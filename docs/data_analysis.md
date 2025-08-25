# Data analysis

Plot accuracies of strategies on benchmarks:
```bash
PYTHONPATH=. python analysis_scripts/plot_accuracies.py
```
Accuracy plot saved in `report/assets/accuracy_comparison.png`

To get error analysis (get fail to pass and vice versa when comparing between two different strategies):
```bash
PYTHONPATH=. python analysis_scripts/status_comparisons.py
```
Error analysis saved in `report/analysis_outputs/status_differences_<STRATEGY_NAME_1>_vs_<STRATEGY_NAME_2>_<MODEL_NAME>.csv`


Cumulative success rates for attempts, skill library usage:
```bash
PYTHONPATH=. python analysis_scripts/analyze_results.py
```
