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
1. Clone the repository with the required submodules:

```bash
git clone https://github.com/nicholaschenai/coala_coder_demo.git
cd coala_coder_demo
git submodule update --init cognitive_base agent_expt_suite
```

**Note:** The `final_results` submodule contains experimental results and is quite large (~1 GB). It is not required for running experiments since results will be generated in your local `results/` folder. 

If you want to access the pre-computed experimental results, you can clone it separately:
```bash
git submodule update --init final_results
```

2. Create and activate the conda environment using the provided environment.yml:

```bash
conda env create -f environment.yml
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
export AZURE_OPENAI_DEPLOYMENT_NAME="{'gpt-4o-2024-08-06': 'YOUR_DEPLOYMENT_NAME_HERE', 'gpt-4o-mini-2024-07-18': 'YOUR_DEPLOYMENT_NAME_HERE'}"
```

### Preparing the semantic memory
The semantic memory consists of competitive programming textbooks. 
This is used for RAG and CoALA.

A checkpoint has been provided in `final_results/comp_prog_sem/ckpt` for convenience.

If you still want to load the competitive programming textbooks into semantic memory from scratch, you can do so by running:

```bash
bash scripts/load_comp_prog_coala.sh
```

it will be saved in `results/comp_prog_sem/`, where the checkpoint will be saved in `ckpt`.

NOTE: all experiments that use only the semantic memory below (RAG, CoALA training) uses the provided checkpoint in `final_results/comp_prog_sem/ckpt`. 
If you want to use the one loaded from scratch, change the `--clone_ckpt` argument to point to `results/comp_prog_sem/ckpt`

## Reproducing experiments
See [REPRODUCTION.md](REPRODUCTION.md)

## Data outputs
Experiment outputs will be saved in the following locations:
- Logs: `log_files/`
- Results: `results/`

### Test Mode Structure
Example structure of a result folder for **test mode** experiments:
```
coala_test_k_1_4o_0806/
├── args.json                  # Experiment configuration and hyperparameters
├── samples_eval_results.json  # MBPP Plus evaluation results
├── samples.jsonl              # Agent output used for evaluation
├── result_dict.json           # Public test case execution result
├── ckpt/                      # Checkpoint directory containing:
│   ├── skill/               # Learned skills, executable code (procedural)
│   ├── non_func/            # Non-executable code (procedural)
│   ├── episodic/            # Episodic memory
│   ├── reflections/         # Reflection memory (semantic)
│   ├── summaries/           # Summary memory (semantic)
│   └── semantic/            # Semantic memory of competitive programming textbooks
└── test_outputs/             # Logs and final output per problem
    └── {problem_id}/         # Each folder named after the problem ID containing:
        ├── logfile.log        # Raw logs
        ├── messages.json     # Canonical messages (see CoalaMessageThread and agent for definition)
        ├── output_i.json     # Outputs for attempt i
        └── output.json       # Final output
```

### Train Mode Structure
Example structure of a result folder for **train mode** experiments, which is similar to the test mode structure but with some differences:
```
coala_train_apps_k_1_4o_0806/
├── args.json
├── ckpt/
└── train_outputs/             # Training logs and outputs per problem
    └── {problem_id}/
        ├── ...                # Same files as test mode
        └── training_data.json # Result of reflections, summaries, and skill descriptions
```

**Key differences in train mode:**
- No evaluation files (`samples_eval_results.json`, `samples.jsonl`, `result_dict.json`)
- Uses `train_outputs/` instead of `test_outputs/`
- Each problem folder contains an additional `training_data.json` file with learning artifacts 

## Project Structure
```
.
├── agent_expt_suite/   # tools for running experiments with agents
├── analysis_scripts/   # scripts for analyzing results
├── cognitive_base/     # Cognitive architecture primitives
├── config/             # argparsers with configs. 
├── data_tools/         # tools for custom data processing on APPS
├── docs/               # steps to reproduce experiments
├── final_results/      # Experiment outputs
├── report/             # Analysis of results
└── scripts/            # Running scripts for train/test
```

## Other resources
- [CoALA paper](https://arxiv.org/abs/2309.02427)
- Notes on AI with a focus on [cognitive architectures](https://github.com/nicholaschenai/agi-potential-notes)
- Literature review on [AI for code](https://github.com/nicholaschenai/ai-for-code)
- Reimplementation of Voyager (Wang _et. al._ 2023) for [coding tasks](https://github.com/nicholaschenai/voyager_coder_experiments)
- Library of cognitive architecture [primitives](https://github.com/nicholaschenai/cognitive_base)

## License
TODO

