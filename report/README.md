# An implementation of CoALA for coding tasks
Work in progress. This page is for the code and scripts currently released in this repo.

Unreleased experiments in [APPENDIX.md](APPENDIX.md)

## Abstract

## Introduction

### Cognitive architectures
- Models of human cognition
- Explicit instantiation of processes like
    - Perception
    - Memory
    - Planning
- Cannonical example: Soar `[1]`

### CoALA
Cognitive architectures for language agents `[2]`: see this [summary](https://github.com/nicholaschenai/agi-potential-notes/blob/main/papers/coala.md).

Outline of a coding agent from the CoALA paper:

> For example, a future coding agent could maintain human-provided programming knowledge (semantic) such
> as manuals, textbooks, problems, and examples, as well as its problem solutions and test records (episodic),
> reflections, and summaries on top of these experiences (semantic), and a gradually expanding code library
> that stores useful methods, e.g., QuickSort, GCD, LCA (procedural). 

#### Implementation details
- Episodic: (Task, Previous Critique, Thought Process and Code, Environment Feedback, Result) tuple for each transition
- Semantic:
    - Vector DB of competitive programming textbooks curated in `[3]`
    - Summaries at the end of each training episode
    - Reflections at the end of each training episode by comparing to the correct solution
- Procedural:
    - Voyager `[4]` style code library for callable functions
    - If not callable (eg class), stored as retrievable text

### AI for code
For an overview of AI for code, see this [literature review](https://github.com/nicholaschenai/ai-for-code)

## Experiments

### Benchmarks
#### MBPP Plus
MBPP `[5]` is a crowdsourced benchmark of basic programming problems and solutions.
MBPP Plus `[6]` is a coding benchmark based off MBPP with more test cases per example, and filtered / edited for correctness.

From the problem statement, the AI is expected to write a function that satisfies the test cases.

#### APPS
APPS `[7]` is a benchmark of 10k problems curated from the web (eg Leetcode, Codeforces, etc), with programmatically extracted test cases and multiple solutions per problem. It is further split into introductory, interview (LC style), and competition levels.

Some practical details [here](https://github.com/nicholaschenai/ai-for-code/blob/main/practical-details/APPS-practical.md)

### Baselines
- Zero shot pass@1 (see [website](https://evalplus.github.io/leaderboard.html))
- ReAct `[8]` (Current implementation of CoALA without long-term memory)
- RAG (Current implementation of CoALA with competitive programming textbooks only as long-term memory)

### Models
- GPT-4o-0806 as the baseline large model
- GPT 4o Mini (July 2024) as the baseline smaller model
- Ada 002 embeddings

### Training details
APPS intermediate for training, random sampled after filtering for execution correctness.

Our base experiments use 100 training problems.

CoALA starts off with the competitive programming textbooks as long-term memory, and builds up the various other long term memories over training.

### Eval details
- After the memories are built up from training, we evaluate on MBPP Plus.
- Each MBPP Plus task comes with one public test case. During evaluation, the for loop in the pseudocode is run for the one public test case and the success is determined by the assertion. The answer at the end of the loop (be it from successsful assertion or all tries) is used for evaluation on the private test cases.
- As MBPP is an old benchmark, it is possible that LLMs have seen the dataset before. As such, we only look at the **relative change** from zero-shot pass@1 performance as an indicator.

Tuning retrieval k:

Before evaluation, we perform a search on the optimal retrieval k for each model, 
and use the k corresponding to the best performance on the APPS training set for evaluation.

| Model | k=3 | k=2 | k=1 |
|-------|-----|-----|-----|
| 4o mini | **77%** | 76% | 73% |
| 4o 0806 | 72% | 78% | **80%** |

Based on these results, we pick k=3 for 4o mini and k=1 for 4o 0806.

## Results
### Accuracy comparison


| Model | Zero shot | ReAct | RAG | CoALA |
|-------|-----------|--------|-----|--------|
| 4o mini | 72.2% | **74.9%** | 72.8% (k=3) | 73.3% (k=3) |
| 4o 0806 | 72.2% | 76.5% | **77.5%** (k=1) | 77.0% (k=1) |


## Discussion
### Qualitative analysis
#### Memories have a big influence on 4o mini
- Indentations in APPS influence 4o mini to write code that triggers unexpected indentation errors on MBPP Plus
- Practice of calling the function (especially naming it as `main`) to read and write from IO in APPS influences 4o mini to do the same even though in MBPP Plus, the function name is expected to be that given by the problem statement and not called
- Usually recovers after seeing the warning message of wrong function / indentation, but there were a few occasions where it could not recover within the maximum number of retries

## Future Work

## Conclusion

## References
1. Laird, J.E., 2022. Introduction to SOAR. arXiv preprint arXiv:2205.03854.
2. Sumers, T.R., Yao, S., Narasimhan, K. and Griffiths, T.L., 2023. Cognitive architectures for language agents. arXiv preprint arXiv:2309.02427.
3. Shi, Q., Tang, M., Narasimhan, K. and Yao, S., 2024. Can Language Models Solve Olympiad Programming?. arXiv preprint arXiv:2404.10952.
4. Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao, C., Zhu, Y., Fan, L. and Anandkumar, A., 2023. Voyager: An open-ended embodied agent with large language models. arXiv preprint arXiv:2305.16291.
5. Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski, H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q. and Sutton, C., 2021. Program synthesis with large language models. arXiv preprint arXiv:2108.07732.
6. Liu, J., Xia, C.S., Wang, Y. and Zhang, L., 2024. Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation. Advances in Neural Information Processing Systems, 36.

7. Hendrycks, D., Basart, S., Kadavath, S., Mazeika, M., Arora, A., Guo, E., Burns, C., Puranik, S., He, H., Song, D. and Steinhardt, J., 2021. Measuring coding challenge competence with apps. arXiv preprint arXiv:2105.09938.
8. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. and Cao, Y., 2022. React: Synergizing reasoning and acting in language models. arXiv preprint arXiv:2210.03629.


## Appendix
[APPENDIX.md](APPENDIX.md)
