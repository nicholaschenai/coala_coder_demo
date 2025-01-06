# An analysis of CoALA for coding tasks
(Currently work in progress)

## About
This repo contains an attempt at implementing the CoALA (Sumers _et. al._ 2023) agent for coding tasks.

We train on APPS and evaluate on MBPP Plus.

It is also benchmarked against these base agents:

1. ReAct
2. RAG (Retrieval-Augmented Generation) from semantic memory (competitive programming textbooks)

See the [report](report/README.md) for more details (work in progress).

## Installation

### Setup Instructions
1. Clone the repository with submodules:

```bash
git clone --recursive https://github.com/nicholaschenai/coala_coder_demo.git
cd coala_coder_demo
```

2. Create and activate the conda environment using the provided environment.yml:

```bash
conda env create -f environment.yml python=3.10
conda activate coala_coder_demo
```

3. Set up API keys as described below

For OpenAI:

```bash
export OPENAI_API_KEY="YOUR_KEY_HERE"
```

Azure OpenAI:

```bash
export AZURE_OPENAI_API_KEY="YOUR_KEY_HERE"
export AZURE_OPENAI_ENDPOINT="ENDPOINT_URL_HERE"
export OPENAI_API_VERSION="2023-07-01-preview"
export AZURE_OPENAI_DEPLOYMENT_NAME="{'gpt-4-1106-preview': 'YOUR_DEPLOYMENT_NAME_HERE', 'gpt-4o-mini-2024-07-18': 'YOUR_DEPLOYMENT_NAME_HERE'}"
```

## Reproducing experiments

### Baseline ReAct
GPT-4o mini:
```bash
bash scripts/react_test_4o_mini.sh
```

GPT-4o-08-06:
```bash
bash scripts/react_test_4o_0806.sh
```

### Preparing the semantic memory

A checkpoint has been provided in `final_results/comp_prog_sem/ckpt` for convenience.

If you still want to load the competitive programming textbooks into semantic memory from scratch, you can do so by running:

```bash
bash scripts/load_comp_prog_coala.sh
```

it will be saved in `results/comp_prog_sem/`, where the checkpoint will be saved in `ckpt`.

NOTE: all experiments that use only the semantic memory below (RAG, CoALA training) uses the provided checkpoint in `final_results/comp_prog_sem/ckpt`. 
if you want to use the one loaded from scratch, change the `--clone_ckpt` argument to point to `results/comp_prog_sem/ckpt`

### CoALA train

First run training to get the checkpoint with various memories.
We run with different retrieval k to tune it via train accuracies.

GPT-4o-mini
```bash
bash scripts/coala_train_apps_k_1_4o_mini.sh
bash scripts/coala_train_apps_k_2_4o_mini.sh
bash scripts/coala_train_apps_k_3_4o_mini.sh
```

GPT-4o-08-06
```bash
bash scripts/coala_train_apps_k_1_4o_0806.sh
bash scripts/coala_train_apps_k_2_4o_0806.sh
bash scripts/coala_train_apps_k_3_4o_0806.sh
```

Note that when loading the APPS dataset for the first time, 
there will be an initial process to execute the solutions 
to the problems to verify that the solutions are correct. 

We have provided the precomputed result in data_tools/cache (will be loaded by default),
but if that is deleted, the process will take a while.

Then proceed to use the memories for evaluation:
(minor caveat: manually delete the episodic/episode_state.json file before running the script to start fresh else it will count episodes from training)

### CoALA test
We use the k corresponding to the best performance on APPS for each model.

GPT-4o-mini:
```bash
bash scripts/coala_test_k_3_4o_mini.sh
```

GPT-4o-08-06:
```bash
bash scripts/coala_test_k_1_4o_0806.sh
```

### RAG baseline
We use the k corresponding to the best performance on APPS for each model.
To run the RAG agent with GPT-4o-mini:

```bash
bash scripts/rag_test_k_3_4o_mini.sh
```

GPT-4o-08-06:
```bash
bash scripts/rag_test_k_1_4o_0806.sh
```

### Data analysis
**TODO**

<!-- Plot accuracies, get error analysis:

```bash
python scripts/results_analysis.py
``` -->


### Data outputs
**TODO**

Experiment outputs will be saved in the following locations:
- Logs: `logs/`
- Results: `results/`

Example structure of a result folder
```
coala_test_k_3_4o_0806/
├── args.json                  # Experiment configuration and hyperparameters
├── samples_eval_results.json  # MBPP Plus evaluation results
├── samples.jsonl              # Agent output used for evaluation
├── result_dict.json          # Public test case execution result
├── ckpt/                     # Checkpoint directory containing:
│   ├── skill/               # Learned skills, executable code (procedural)
│   ├── non_func/            # Non-executable code (procedural)
│   ├── episodic/            # Episodic memory
│   ├── reflections/         # Reflection memory (semantic)
│   ├── summaries/           # Summary memory (semantic)
│   └── semantic/            # Semantic memory of competitive programming textbooks
├── test_outputs/             # logs and final output per problem
```

<!-- Accuracy plot saved in `report/assets/accuracy_comparison.png`
Error analysis saved in `report/assets/4o_mini_status_differences.csv` and `report/assets/4_1106_status_differences.csv` -->

## Project Structure
```
.
├── cognitive_base/      # Cognitive architecture primitives
├── agent_expt_suite/    # tools for running experiments with agents
├── data_tools/         # tools for custom data processing on APPS
├── report/             # Documentation and analysis
├── scripts/            # Running scripts
└── final_results/      # Experiment outputs
```

## Other resources
- [CoALA paper](https://arxiv.org/abs/2309.02427)
- Notes on AI with a focus on [cognitive architectures](https://github.com/nicholaschenai/agi-potential-notes)
- Literature review on [AI for code](https://github.com/nicholaschenai/ai-for-code)
- Reimplementation of Voyager (Wang _et. al._ 2023) for [coding tasks](https://github.com/nicholaschenai/voyager_coder_experiments)
- Library of cognitive architecture [primitives](https://github.com/nicholaschenai/cognitive_base)

## License
TODO

