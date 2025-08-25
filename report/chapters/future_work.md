# Future Work

## Component-wise Evaluation of Cognitive Architectures

Our implementation revealed a challenge in evaluating complex cognitive architectures: 
when multiple components interact (learning, retrieval, reasoning), 
it becomes difficult to isolate which mechanisms contribute to performance changes. 
The domain mismatch between memories (APPS, competitive programming) and test sets (MBPP Plus) further complicates assessment, 
making it unclear whether differences stem from memory systems or domain transfer issues.

Future work should adopt targeted experimental approaches, 
testing individual components on benchmarks designed to isolate their contributions. 
For example, 
the LoCoMo benchmark `[12]` evaluates question-answering over extended conversational histories, 
providing direct assessment of memory mechanisms. 

As noted in our lessons learned, the temptation to implement multiple innovations simultaneously makes ablation studies and debugging significantly more challenging. 
By testing on the least complex domain that can still discern meaningful improvements, 
we can iteratively refine each component before integrating them into more complex agent tasks.

---

## Memory Systems Enhancement

Our experiments with memory systems in LLM-based agents have revealed challenges that have been studied for decades in traditional cognitive architecture research. 
Established frameworks like Soar have developed sophisticated approaches to memory representation, retrieval, and management that could address many of the limitations we encountered. 
Future work should integrate these well-established cognitive principles with modern LLM capabilities to create more effective agent architectures. 
The following subsections outline a combination of insights from our experiments, 
and also insights from traditional cognitive architecture research.

### Procedural Memory: Modular Code Components Over Monolithic Solutions

Our current implementation stores entire successfully executed code blocks in procedural memory, following the approach used in systems like Voyager. 
However, our [previous experiments](https://github.com/nicholaschenai/voyager_coder_experiments/tree/main/report) revealed significant limitations with this monolithic storage approach. 
We direct the reader to the previous experiments for a discussion of why this is so, 
and reiterate here the recommendation to adopt a more modular approach to code storage, 
such as refactoring successful code into modular blocks and storing the modular blocks as skills.

This is especially so in our case where we only had one function in the skills library, 
and mostly classes stored in the rest of the procedural memory.

### Improved Memory Retrieval Mechanisms

Our current implementation relies primarily on embedding-based retrieval, 
which might be insufficient for code-related memories. 
Future work should implement retrieval approaches that augments existing vector-based retrieval with:

- Base-level activations: As implemented in Soar, 
base-level activation biases retrieval using recency and frequency of previous memory accesses. 
This could help prioritize frequently useful code patterns over rarely used ones.

- Spreading activation: As in Soar, this cognitive mechanism biases retrieval toward concepts linked to other concepts currently in working memory. 

- Keyword-based retrieval: During skill description generation, keywords are already extracted but remain unused for matching. Incorporating these keywords into the retrieval process could improve precision. Additionally, keyword-based search from the initial solution can be used, just like in USACO Bench

- Temporal organization for episodic memory: Implementing temporal indexing of episodic memories to exploit the recency bias and contiguity effects observed in human memory systems, where retrieving one memory activates temporally adjacent memories.

### Memory Quality and Filtering

Currently, the system retrieves a fixed number of memories regardless of their relevance scores. 
This approach can introduce noise into the agent's working memory, 
potentially leading to incorrect solutions. 
Our experiments (both in this and previous work) demonstrated that irrelevant memories can displace more relevant information and adversely affect performance. 
The ease of LLMs in generating reasoning traces exacerbates this problem by 
leading to rapid accumulation of memories, many of which may be of low value. 
In fact, in our prior experiments, 
it is easy to have thousands of memory chunks after training. 
Cognitive architecture research offers several principles for addressing this:

- Selective learning: For procedural memory, rather than storing all successful solutions (as in Voyager), 
adopt more stringent criteria similar to Soar's approach, 
which only learns skills when the system encounters and resolves an impasse. 
This selective approach ensures only non-trivial skills are learned.

- Thresholding: Only retrieve memories above a certain relevance threshold to prevent low-quality memories from influencing the agent's reasoning, 
mimicking the activation thresholds in biological memory systems.

- Context-aware filtering: Develop mechanisms to assess whether retrieved memories are genuinely applicable to the current task, 
similar to how production rules in Soar have specific conditions that must be met before they are applied.

- Memory pruning strategies: Implement mechanisms to identify and remove or deprioritize low-value chunks that consistently fail to contribute to task success.

However, this approach presents a trade-off: sometimes seemingly unrelated memories can serve as creative inspiration for novel solutions. 
The challenge lies in distinguishing between harmful noise and potentially useful analogies.

### Specialized Episodic Memory
Cognitive architecture research has established distinct properties for different memory systems. 
In prior experiments, episodic memories showed the lowest information density and often decreased accuracy through displacement effects. 
Future work can implement these properties known about episodic memories:

Episodic memories should be temporally organized, with retrieval influenced by:
- Recency bias: More recent memories are more easily accessible
- Similarity-based retrieval: Partial state-based matching allows retrieval based on partial specifications of a cue
- Contiguity effects: Retrieving one memory activates temporally adjacent memories

---

## Hybrid Reasoning Approaches

While our current implementation relies primarily on LLM-based reasoning, 
future work could explore hybrid approaches that combine LLMs with symbolic or rule-based reasoning systems. 
This is especially useful to our coding tasks as code follows hard logic. 
This can address the limited creativity problem observed in pure LLM reasoning, 
where agents may struggle to generate novel solution strategies beyond their training data.

Traditional cognitive architectures like Soar naturally integrate symbolic reasoning with subsymbolic mechanisms. 
Modern LLM-based agents could benefit from similar hybrid approaches combining symbolic planning and rule-based constraints with LLM creativity.

---

## Scaling and Performance Evaluation

Our choice of 100 training iterations appears somewhat arbitrary, 
and with improved memory management systems to solve the limitations we found with large memory banks, 
we could potentially scale up training iterations to achieve better performance. 
This connects to our earlier discussion on component-wise evaluation, 
as proper scaling requires reliable assessment of individual memory components.

The surprising observation that the 4o mini model performed better with larger retrieval values of k while the 4o 0806 model performed better with smaller k values on the training set (though the former is overly influenced by memories on the downside)
suggests complex interactions between model size, 
memory utilization, and task performance. 
This warrants further investigation and highlights the need for more systematic evaluation approaches.

### Benchmarking Improvements

As noted in the limitations section, the MBPP Plus benchmark is quite noisy, 
making it hard to draw definitive conclusions about different strategies. 
Future work should focus on improving benchmarking methodologies:

- Using benchmarks with less noise and ambiguity
- Multiple benchmarks / larger sample sizes to average out noise
- Newer models which might be able to handle memory noise more effectively
