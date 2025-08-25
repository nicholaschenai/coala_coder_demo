# Experiments

## Benchmarks
### MBPP Plus
MBPP `[5]` is a crowdsourced benchmark of basic programming problems and solutions.
MBPP Plus `[6]` is a coding benchmark based off MBPP with more test cases per example, and filtered / edited for correctness (378 problems). 

From the problem statement, the AI is expected to write a function that satisfies the test cases.

### APPS
APPS `[7]` is a benchmark of 10k problems curated from the web (eg Leetcode, Codeforces, etc), with programmatically extracted test cases and multiple solutions per problem. It is further split into introductory, interview (LC style), and competition levels.

Some practical details [here](https://github.com/nicholaschenai/ai-for-code/blob/main/practical-details/APPS-practical.md)

## Baselines
- Zero shot pass@1 (see [EvalPlus](https://evalplus.github.io/leaderboard.html))
- ReAct `[8]` (Current implementation of CoALA without long-term memory)
- RAG (Current implementation of CoALA with competitive programming textbooks only as long-term memory)

## Models
- GPT-4o-0806 as the baseline large model
- GPT 4o Mini (July 2024) as the baseline smaller model
- Ada 002 embeddings

## CoALA Training details
APPS intermediate for training, random sampled after filtering for execution correctness.

CoALA starts off with the competitive programming textbooks as long-term memory, 
and builds up the various other long term memories over training.

Our base experiments use 100 training problems.

## Eval details
- After the memories are built up from training, we evaluate on MBPP Plus.
- Each MBPP Plus task comes with one public test case. During evaluation, the for loop in the pseudocode is run for the one public test case and the success is determined by the assertion. The answer at the end of the loop (be it from successsful assertion or all tries) is used for evaluation on the private test cases.
- As MBPP is an old benchmark, it is possible that LLMs have seen the dataset before. As such, we only look at the **relative change** from zero-shot pass@1 performance as an indicator.

## Hyperparameter search
Before evaluation, we perform a search on some hyperparameters (see [appendix_hyperparam.md](appendix_hyperparam.md)).