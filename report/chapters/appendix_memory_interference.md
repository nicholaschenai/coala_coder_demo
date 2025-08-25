# Appendix: Memory Interference Examples

This appendix contains additional examples of memory interference across different model sizes and agent strategies, complementing the discussion in the main limitations section on "Unrelated memories can interfere with problem solving."

In the examples below, 
we verified that all retrieved memories by RAG and CoALA were irrelevant to the problem, 
and the discrepancies in behavior remains an open question worth investigating.

## Small Model (GPT-4o-mini) Examples

### MBPP 232: Return N Largest Items from List

This problem requires returning the N largest items from a list, 
with a public test case that uses the set operator, 
which might influence the model.

- ReAct got misled by the test case and incorrectly used a set operation before sorting, causing it to miss duplicates.
- RAG implemented the correct solution directly.
- CoALA surprisingly got misled similar to ReAct.

### MBPP 120: Maximum Absolute Product Between Numbers in Pairs of Tuples Within a Given List
- ReAct implemented it correctly.
- CoALA, despite understanding that it should use absolute values, incorrectly assumed that all numbers would be positive and therefore omitted the absolute function in its implementation and got the private test case wrong.

### MBPP 125: Maximum Difference Between Number of 0s and 1s in Binary String

**Problem Description:** Find the maximum difference between the number of 0s and number of 1s in any sub-string of the given binary string.

- ReAct got it right.
- CoALA erroneously used the absolute function when calculating the difference, when the problem specifically asked for the raw difference (number of 0s - number of 1s).

## Large Model (GPT-4o 0806) Examples

### MBPP 103: Eulerian Number Calculation

**Problem Description:** Calculate the Eulerian number A(n, m).

- ReAct got it right.
- RAG reversed the order of base case checks and failed.
- CoALA had the same issue as RAG

### MBPP 11: Remove First and Last Occurrence of Character

**Problem Description:** Remove the first and last occurrence of a specified character in a string.

**Key Challenge:** Handling the case where there is only one occurrence of the character.

- ReAct got it right.
- CoALA properly handled the edge case in its pre-retrieval thought process, but after receiving memories, it no longer considered this scenario.

### MBPP 16: Validate Strings with Underscore-Joined Lowercase Letters

**Problem Description:** Write a function that returns true if the input string contains sequences of lowercase letters joined with an underscore and false otherwise.

- ReAct used logical statements for validation instead of regular expressions (which the ground truth solution uses) and still got it right.
- CoALA misunderstood the problem, only checking if underscores are flanked by lowercase letters rather than validating all characters between underscores, got it wrong
  - Its pre-memory reasoning had the correct approach.
- RAG performed similarly to ReAct and got it right

### MBPP 792: Count Number of Lists in a List

**Problem Description:** Count the number of lists contained within a given list.

**Public Test Case Limitation:** Only contains simple lists-within-lists, not complex nested structures.

- ReAct naively used `len()` because the public test case only had a simple list within a list, failed for private test case
- RAG properly checked each element to verify if it's a list

### MBPP 752: Find the nth Jacobsthal Number

**Problem Description:** Write a function to find the nth Jacobsthal number.

- ReAct understood the definition but calculated it recursively, leading to recursion depth issues for large values in private test cases.
- CoALA calculated it iteratively from base cases and got it right

## Common Patterns of Memory Interference

Across these examples, several patterns emerge:

- In several cases (MBPP 11, 16), the agent's pre-memory reasoning was correct, but exposure to memories (even irrelevant ones) shifted its approach.

- Memories can influence the choice between different valid implementation strategies (recursive vs. iterative, regex vs. logical checks), sometimes pushing toward better or worse approaches without clear reason.

- Memories can introduce implicit assumptions (e.g., all numbers being positive in MBPP 120) that weren't present in either the problem statement or the retrieved memory itself.

- Memory retrieval sometimes causes agents to overlook edge cases they had initially considered (MBPP 11), suggesting interference with the agent's original problem-solving process.
