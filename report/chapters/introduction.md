# Introduction

## Cognitive architectures
### What is cognitive architecture?
- Models of human cognition
- Explicit instantiation of processes like
    - Perception
    - Memory
    - Planning
- Cannonical example: Soar `[1]`

### Why cognitive architectures?
1. Bio-inspired components -- could give us a clue to intelligence:
    - Distinct long-term memories (procedural, semantic, episodic) with different properties
2. Complementary strengths with LLMs:
    - LLMs provide broad task knowledge from pretraining
    - Cognitive architectures add:
        - Explicit grounding in environment
        - Structured verification and multistep reasoning
        - Coordinated use of multiple knowledge sources
3. System-level benefits:
    - Explainable: Memory formation and associations can be traced
    - Editable: Explicit memories and processes can be modified
    - Deliberate: Cognitive processes can be explicitly implemented rather than emerging unpredictably

## CoALA
In "Cognitive Architectures for Language Agents" (CoALA) `[2]`, the authors propose a framework for integrating cognitive architectures with large language models (LLMs). 
A summary of the paper can be found [here](https://github.com/nicholaschenai/agi-potential-notes/blob/main/papers/coala.md).

The key ideas presented are:
1. Systematizes diverse methods for LLM-based agents:
    - Organizes existing architectures under a unified framework
    - Highlights gaps and proposes actionable directions
    - Standardizes terminology and components across different works
2. Enhances LLM capabilities through structured components:
    - Complements LLM's broad knowledge with explicit memory systems
    - Supports deliberate decision-making through propose-evaluate-select procedures
3. Bridges traditional cognitive architectures and modern LLMs:
    - Replaces handcrafted rules with flexible LLM reasoning
    - Makes text the standard internal representation

To make this idea more concrete, the authors outline a coding agent based on CoALA principles:

> For example, a future coding agent could maintain human-provided programming knowledge (semantic) such
> as manuals, textbooks, problems, and examples, as well as its problem solutions and test records (episodic),
> reflections, and summaries on top of these experiences (semantic), and a gradually expanding code library
> that stores useful methods, e.g., QuickSort, GCD, LCA (procedural). 

The authors also suggests this way of making use of experience:
> ... allow agents to reason about when certain knowledge would be useful, and store this as metadata to facilitate later recall

## Related Work: AI for code
For an overview of AI for code, see this [literature review](https://github.com/nicholaschenai/ai-for-code)

## Contributions
Our primary contributions include:

- We present an implementation of the coding agent described in the CoALA paper, 
and evaluate its performance on coding tasks.

- We demonstrate how memory systems from cognitive architectures can enhance code generation and understanding.

- Our experiments revealed distinct behavioral patterns between small and large language models when augmented with CoALA's memory systems, providing insights into how model capacity interacts with external cognitive mechanisms.

- We identified and characterized specific types of memory interference, 
contributing to the understanding of memory-augmented systems' failure modes.

- We propose enhancements to the implementation based on the findings above.
