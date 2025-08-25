# CoALA train

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

Now, we also ablate episodic memory to see if it is necessary for the performance of CoALA.
```bash
bash scripts/coala_train_apps_k_3_disable_episodic_4o_mini.sh
bash scripts/coala_train_apps_k_1_disable_episodic_4o_0806.sh
```
