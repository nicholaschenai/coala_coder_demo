# Methodology

As the CoALA paper only describes the coding agent at a high level, 
we still need to figure out specific implementation details.

## Pseudocode
### Inference
```
Rollout: For each attempt (up to max_attempts):
    a. If first attempt:
        - Generate initial solution context
    else:
        - Generate critique based on previous attempts
    b. Retrieve k relevant memories using current context from:
        - Episodic memory (past transitions)
        - Semantic memory (textbooks, reflections, summaries)
        - Procedural memory (code library)
    c. Generate code using retrieved context
    d. Execute code and get environment feedback
    e. Store transition in episodic memory:
        (Task, Critique, Generated Code, Env Feedback, Success/Fail)
    f. If execution successful, break loop
```
In our experiments, we use `max_attempts=4`

### Training
```
For each training task:
    Perform rollout (Inference loop above)
    Generate and store semantic memories:
        - Create episode summary
        - Reflection by comparing to official solution
    If successful:
        - Generate skill description for code written during rollout
        - Reason out scenarios in which this skill will be useful, append to description.
        - Add code + descriptions to procedural memory
```

## CoALA implementation details

### Prompts and retrieval methodology
Prompts and retrieval methodology adapted from USACO Bench `[3]` and Reflexion `[11]`

As in USACO Bench, we get the LLM to write a rough solution first and use that rough solution for retrieval. 
This is because the problem description might contain stories rather than algorithmic keywords, 
and thus less suitable for retrieval. 

### Memories
Currently all memories are retrieved via vector similarity with existing cue

#### Episodic
(Task, Previous Critique, Thought Process and Code, Environment Feedback, Result) tuple for each transition.

We store all transitions in the episodic memory in a lossless fashion due to this principle from cognitive science:

Automatic creation `[13]`: Agents shouldn't need to decide which experiences to remember, as this can interfere with task-based reasoning and agents are unlikely to effectively determine which experiences will be relevant to future decisions.

This is in contrast to the current trend of summarizing memories and discarding potentially useful information.

#### Semantic:
- Vector DB of competitive programming textbooks curated in USACO Bench `[3]`
- Summaries at the end of each training episode
- Reflections at the end of each training episode by comparing to the correct solution

#### Procedural:
- Learning of procedural skills is inspired by Voyager `[4]`
    - When a code is successful, it is added to the procedural memory for future reference, with a skill description written
    - After this, direct prompting to reason about when this skill will be useful, append as metadata to aid retrieval (as mentioned in the CoALA paper)
- Voyager style code library for callable functions
    - Allows agent to reuse previously written functions by calling it
    - If not callable (eg class), stored as retrievable text

Full examples in [appendix_memory_examples.md](appendix_memory_examples.md)
