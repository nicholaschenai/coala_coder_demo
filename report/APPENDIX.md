## Custom architecture
- Custom architecture with GPT 4-1106 scores 79.9%, beats o1-mini's 78.8% and one question away from o1's 80.2%. (4-1106 zero shot is 73.3%)

## Lessons from experimenting with Cognitive Architectures
### Manage Memory Bloat
- Easy to produce reasoning -> Easy to flood working / LT mem
    - Low value chunks
    - Experiments: Thousands of memory chunks after training
    - Voyager: Accept all correct skills. Soar: Only if it got stuck then unstuck (impasse, chunking)
- Episodic is tricky – Lowest info / token
    - Mostly **decreased** accuracies due to displacement

### Mitigate LLM Reasoning Errors
- Erroneous outputs might be stored and retrieved later, causing errors in future reasoning steps
- Examples of failure modes seen experimentally
    - LM to give ratings
    - LM for extraction
        - Can be too literal 
    - LM summarization
        - Throws away some info (that’s why need explicit LT mem structures)
    - Generalization of LM learnt knowledge
        - Prompting for general template seems to be hard
        - Can learn from Soar’s chunking to replace variables
- Symbolic verifiers / other fallbacks as much as possible!

### Iterative Improvement Over “Everything” CA
- Many new angles of attack – temptation to implement many things at once
- Ablations, debugging more difficult
- Test on the least complex domain that can discern improvement
