# Hyperparameter tuning
Before evaluation, we perform a search on some hyperparameters on the training set.

## Tuning retrieval k

We perform a search on the optimal retrieval k for each model corresponding to the best performance on the APPS training set

| Model | k=3 | k=2 | k=1 |
|-------|-----|-----|-----|
| 4o mini | **77%** | 76% | 73% |
| 4o 0806 | 72% | 78% | **80%** |

Based on these results, we pick k=3 for 4o mini and k=1 for 4o 0806.

We also use the same $k$ (per model) for the RAG baseline for consistency.

## Ablating episodic memory

Using the best k, we ablate episodic memory to see if it is necessary for the performance of CoALA.

| Model | with episodic | without episodic |
|-------|-----|-----|
| 4o mini | 77% | **78%** |
| 4o 0806 | **80%** | 78% |

From this, we do not use episodic memory for 4o mini but retain it for 4o 0806.