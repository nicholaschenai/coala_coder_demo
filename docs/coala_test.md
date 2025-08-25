# CoALA Test

Now we proceed to use the memories for evaluation:
(minor caveat: manually delete the episodic/episode_state.json file before running the script to start fresh else it will count episodes from training)

We use the k corresponding to the best performance on APPS for each model.

GPT-4o-mini:
```bash
bash scripts/coala_test_k_3_disable_episodic_4o_mini.sh
```

GPT-4o-08-06:
```bash
bash scripts/coala_test_k_1_4o_0806.sh
```