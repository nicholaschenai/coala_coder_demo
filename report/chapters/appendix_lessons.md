# Further lessons from experimenting with Cognitive Architectures

## Mitigate LLM Reasoning Errors
- Erroneous outputs might be stored and retrieved later, causing errors in future reasoning steps
- Examples of failure modes seen experimentally
    - LM to give ratings
    - LM for extraction
        - Can be too literal 
    - LM summarization
        - Throws away some info (that's why need explicit LT mem structures)
    - Generalization of LM learnt knowledge
        - Prompting for general template seems to be hard
        - Can learn from Soar's chunking to replace variables
- Symbolic verifiers / other fallbacks as much as possible!
