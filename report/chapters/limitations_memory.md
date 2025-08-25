# Limitations: Memory

After reviewing experimental logs, we found several ways which irrelevant memories could confound the results of our findings.

## Unrelated memories can interfere with problem solving
The analysis of experimental trajectories reveals a significant limitation in evaluating the effects of memory in agents: 
**unrelated memories can influence problem-solving performance unpredictably**, 
particularly affecting smaller models more than larger ones.

### Inconsistent Representation Patterns

One striking pattern of memory interference occurs when solving problems that require mathematical constants like pi. Across both small and large models, retrieved memories and even the problem statement subtly influence how agents represent mathematical constants in their code, creating unexpected variations in solution approaches despite all agents understanding the correct formula.

MBPP problems 233 (lateral surface area of a cylinder) and 139 (circumference of a circle) provide clear examples of this phenomenon. In both cases, all agents correctly identify the underlying mathematical formula, but their implementation varies in three significant ways:

- Short decimal approximation: Using approximate values like `pi = 3.14159` (passes public test cases but fails private test cases)
- Long decimal approximation: Using more precise values like `pi = 3.141592653589793` (passes all test cases)
- Math library usage: Using the built-in constant via `import math` and `math.pi` (passes all test cases)

#### Small Model (GPT-4o-mini) Behavior

For MBPP 233 (lateral surface area of a cylinder):

- ReAct used a short decimal approximation that passed the public test case but failed private test cases:
  ```python
  def calculate_lateral_surface_area(radius: float, height: float) -> float:
      # Define the value of pi
      pi = 3.14159
      # Calculate the lateral surface area using the formula
      lateral_surface_area = 2 * pi * radius * height
      return lateral_surface_area
  ```

- RAG, despite retrieving geometry-related documents with no mention of pi (like the one below), used a more precise decimal value:
  ```
  [Textbook Reference Material]:
      Chapter: Geometry
      Section: Polygon area
      Part: 1/1
      \section{Polygon area}
      
      A general formula for calculating the area
      of a polygon, sometimes called the \key{shoelace formula},
      is as follows: \index{shoelace formula}
      ...
  ```
  
  The resulting code showed the influence despite irrelevant content:
  ```python
  def calculate_pi():
      # This function returns the value of pi
      return 3.141592653589793
  
  def lateralsuface_cylinder(radius: float, height: float) -> float:
      # Calculate the value of pi
      pi = calculate_pi()
      # Calculate the lateral surface area using the formula 2 * pi * r * h
      area = 2 * pi * radius * height
      return area
  ```

- CoALA retrieved memories about geometric problems (triangles) that had no direct relationship to cylinders:
  ```
  [Summary]:
      In this task, the goal was to determine if a right-angled triangle could be formed 
      with a given hypotenuse \( H \) and area \( S \). The solution involved using the 
      properties of right triangles, specifically the Pythagorean theorem and the formula 
      for the area of a triangle...
  ```
  
  Yet still produced code with a precise pi constant:
  ```python
  def lateral_surface_area(radius, height):
      # Importing the value of pi
      pi = 3.141592653589793
      # Calculate the lateral surface area using the formula
      area = 2 * pi * radius * height
      return area
  ```

#### Large Model (GPT-4o) Behavior

For MBPP 233:

- ReAct used `math.pi` from the standard library:
  ```python
  import math
  
  def lateralsuface_cylinder(height: float, radius: float) -> float:
      lateral_surface_area = 2 * math.pi * radius * height
      return lateral_surface_area
  ```

- RAG retrieved an irrelevant document about polygons:
  ```
  [Textbook Reference Material]:
      Chapter: Geometry
      Section: Polygon area
      Part: 1/1
      \section{Polygon area}
      ...
      \key{Pick's theorem} provides another way to calculate
      the area of a polygon provided that all vertices 
      of the polygon have integer coordinates.
      ...
  ```
  
  But used a short decimal approximation:
  ```python
  def lateralsuface_cylinder(height: float, radius: float) -> float:
      pi = 3.1415  # Approximation of pi
      lateral_surface_area = 2 * pi * radius * height
      return lateral_surface_area
  ```

- CoALA retrieved a memory about triangles that included math library imports:
  ```
  [Summary]:
      In tackling the problem of finding a right-angled triangle with a given hypotenuse \( H \) 
      and area \( S \), the core concepts involved understanding the Pythagorean theorem and 
      the formula for the area of a triangle...
      
      ### Code Snippet:
      ```python
      import sys
      import math
      
      def find_triangle_sides():
          ...
      ```
  ```
  
  And was influenced to use `math.pi`:
  ```python
  import math
  
  def lateralsuface_cylinder(radius: float, height: float) -> float:
      lateral_surface_area = 2 * math.pi * radius * height
      return lateral_surface_area
  ```
but in fact this influence wasn't needed as seen in ReAct!

#### The Pattern Reverses Across Problems

What makes this phenomenon particularly interesting is that the same agent shows inconsistent behavior across similar problems:

For Problem 139 (circumference of circle), with the exact same base formulas:

- ReAct (4o mini): Used a long decimal in Problem 139 but a short decimal in Problem 233
- ReAct (4o 0806): Used `math.pi` in Problem 233 but short decimal in Problem 139, failing private test cases
- RAG (4o 0806): Used short decimal in Problem 233 but `math.pi` in Problem 139, when in both cases the retrieved document was irrelevant
- CoALA (4o 0806): Retrieved a memory on pi and handling of precision with decimal places but did not mention math library, used `math.pi` (one would expect it to use a long decimal due to memory influence)

This complete reversal of approach within the same models suggests the unpredictable influence of memory and context on implementation choices.

| Model | Problem | Agent | Memory Relevance | Pi Implementation | Result |
|-------|---------|-------|-----------------|-----------------|--------|
| **GPT-4o mini** | 233: Lateral surface area of cylinder | ReAct | N/A (no memory) | Short decimal (3.14159) | **Fail** |
| | | RAG | Irrelevant (about circles, no pi mention) | Long decimal (3.141592653589793) | **Pass** |
| | | CoALA | Irrelevant | Long decimal (3.141592653589793) | **Pass** |
| | 139: Circle circumference | ReAct | N/A (no memory) | Long decimal (3.141592653589793) | **Pass** |
| | | RAG | Irrelevant (about circles, no pi mention) | Long decimal (3.141592653589793) | **Pass** |
| | | CoALA | Irrelevant (about circles, no pi mention) | Long decimal (3.141592653589793) | **Pass** |
| **GPT-4o 0806** | 233: Lateral surface area of cylinder | ReAct | N/A (no memory) | math.pi | **Pass** |
| | | RAG | Irrelevant (about polygons) | Short decimal (3.14159) | **Fail** |
| | | CoALA | Partially relevant (used math library) | math.pi | **Pass** |
| | 139: Circle circumference | ReAct | N/A (no memory) | Short decimal (3.14159) | **Fail** |
| | | RAG | Irrelevant (about circles, no pi mention) | math.pi | **Pass** |
| | | CoALA | Partially relevant (mentioned pi and decimal precision) | math.pi | **Pass** |

### Inconsistent Error Recovery Behaviors

Memory interference can lead to surprising differences in how agents interpret errors and handle recovery, with some agents persisting in incorrect interpretations despite clear evidence to the contrary.

MBPP 610:
> Write a python function which takes a list and returns a list with the same elements, but the k'th element removed.
```python
assert remove_kth_element([1,1,2,3,4,4,5,1],3)==[1, 1, 3, 4, 4, 5, 1]
```

This problem has an implicit constraint: indexing starts at 1 (not 0), as shown in the public test case.

**Agent Response Differences** (GPT-4o 0806):

ReAct initially used zero-indexing (standard in Python), failed the test case, then quickly recognized the issue:
> ... 
> 2. **Understanding the Error:**
>    - The function is removing the element at index `3`, which is `3` in the list `[1,1,2,3,4,4,5,1]`.
>    - The expected output suggests that the element at index `2` (which is `2`) should be removed instead.
> 
> 3. **Re-evaluate the Problem Statement:**
>    - The problem statement is ambiguous about whether the index is 0-based or 1-based.
>   - The test case suggests that the index is 1-based, meaning the 3rd element in the list (1-based) is `2`, which should be removed.
> ...

and fixed its solution assuming 1-index:
```python
def remove_kth_element(lst, k):
    # Adjust for 1-based index by subtracting 1 from k
    # Return a new list that is the concatenation of:
    # - the sublist from the start to just before index k-1
    # - the sublist from index k to the end
    return lst[:k-1] + lst[k:]
```

RAG initially made the same mistake, but when presented with a test failure, 
RAG insisted its approach was correct and the test case was wrong:
> ...
> 
> 3. **Identifying the Mistake:**
>    - The expected output in the test case seems incorrect. The expected output `[1, 1, 3, 4, 4, 5, 1]` suggests that the element `2` was removed, which is at index 2, not index 3.
>    - The function `remove_kth_element` is correctly removing the element at index 3, which is `3`, resulting in `[1, 1, 2, 4, 4, 5, 1]`.
> 
> 4. **Conclusion:**
>    - The function implementation is correct based on the problem statement, which specifies removing the `k`-th element.
>    - The test case expectation seems to be incorrect. The function is correctly removing the element at the specified index.
> 
> Given this analysis, the function is correctly implemented. The discrepancy lies in the expected output of the test case, not in the function logic.

However, after a second error message, RAG reconsidered and fixed its approach.
> ...
>
> 3. **Identifying the Mistake:**
>    - The misunderstanding here is in the interpretation of the `k`-th element. The test case seems to expect the removal of the element at the `k`-th position in a one-based index system, not zero-based.
>    - In a one-based index system, the `k`-th element is at index `k-1` in zero-based indexing.
> 
> 4. **Correcting the Solution:**
>    - Adjust the function to remove the element at index `k-1` to align with the test case expectations.
> ...

```python
def remove_kth_element(lst, k):
    # Adjust for one-based index by subtracting 1 from k
    index_to_remove = k - 1
    # Check if the adjusted index is valid
    if 0 <= index_to_remove < len(lst):
        # Remove the element at the adjusted index
        lst.pop(index_to_remove)
    # Return the modified list
    return lst
```
In all 3 iterations, it retrieved the same irrelevant document on the Josephus problem
> 	# Josephus Problem
> 
>    ## Statement
> 
>    We are given the natural numbers $n$ and $k$.
>    All natural numbers from $1$ to $n$ are written in a circle. 
>    First, count the $k$-th number starting from the first one and delete it.
>    Then $k$ numbers are counted starting from the next one and the $k$-th one is removed again, and so on.
> ...

CoALA also insisted the test case was wrong upon reflecting on the failed test case
> ...
> 
> 3. **Identifying the Mistake:**
>    - The mistake is not in the logic of the function itself, but rather in the understanding of the test case.
>    - The test case `remove_kth_element([1,1,2,3,4,4,5,1],3)` expects the element at index 3 (which is `3`) to be removed. The expected result `[1, 1, 3, 4, 4, 5, 1]` is incorrect because it still contains the element `3` at index 2. The correct expected result should be `[1, 1, 2, 4, 4, 5, 1]`.
> 
> 4. **Conclusion:**
>    - The function implementation is correct. The issue lies in the expected output of the test case, which is incorrect. The function correctly removes the element at the specified index.
> 
> Given this analysis, the function does not need any changes. The test case expectation should be corrected.

and persisted on this for all 4 iterations, resulting in a wrong answer! 
In the first iteration, it retrieved an irrelevant episodic memory

> `[Past Memory]`:
> 
>   `[Task]`:
> 
>       Given a string s, a k duplicate removal consists of choosing k adjacent and equal letters from s and removing them causing the left and the right side of the deleted substring to concatenate together.
>       We repeatedly make k duplicate removals on s until we no longer can.
>       Return the final string after all such duplicate removals have been made.
> ...

on the 2nd-4th iteration, it retrieved the same irrelevant summary of its past experience:

> In this problem, the core concept was to efficiently remove sequences of `k` adjacent and identical characters from a string until no more such sequences exist. The solution leveraged a stack to keep track of characters and their counts, which is a common pattern for problems involving removal of adjacent duplicates.
>     
> ...

### Irrelevant memories subtly steer models to reason out patterns
Sometimes, irrelevant memories can cause a model to write a slightly different output, 
which then lead it to get the right answer!

MBPP 237:
> Write a function that takes in a list of tuples and returns a dictionary mapping each unique tuple to the number of times it occurs in the list.
```python
assert check_occurences([(3, 1), (1, 3), (2, 5), (5, 2), (6, 3)] ) == {(1, 3): 2, (2, 5): 2, (3, 6): 1}
```
This required understanding an implicit constraint: tuples should be treated as unordered pairs when counting occurrences, as seen from the public test case. On 4o mini,

ReAct failed to recognize this pattern and implemented increasingly complex heuristics trying to reconcile the test case with its literal interpretation of the problem statement. 
In the end, it couldn't get the public test case right.

RAG initially retrieved unrelated documents and could not spot the implicit constraint, 
so it also made the same mistake as ReAct. 
Surprisingly, during the critic step, it realized the constraint:
> 1. **Understanding the Expected Output**: 
>    The assertion states that the function should return a dictionary mapping each unique tuple to the number of times it occurs in the list. The expected output for the input `[(3, 1), (1, 3), (2, 5), (5, 2), (6, 3)]` is `{(1, 3): 2, (2, 5): 2, (3, 6): 1}`. This indicates that the tuples `(1, 3)` and `(2, 5)` should be counted twice, while `(3, 6)` should be counted once.
> 
> 2. **Identifying the Mistake**: 
>    The mistake in the previous solution is that it does not account for the fact that tuples `(3, 1)` and `(1, 3)` are considered the same for counting purposes. The function should treat tuples as unordered pairs, meaning `(a, b)` is equivalent to `(b, a)`. Therefore, when counting occurrences, we need to ensure that we are counting both `(3, 1)` and `(1, 3)` as the same tuple.
> 
> 3. **Correcting the Approach**: 
>    To fix this, we can sort the elements of each tuple before counting them. By sorting, we can ensure that `(3, 1)` and `(1, 3)` are both represented as `(1, 3)`. This way, we can accurately count the occurrences of each unique unordered pair.

The same thing happened to CoALA. 
A comparison of their thought process can be found in the [appendix](./appendix_subtle_influence.md). 
Despite their similarities, ReAct was not able to self-correct its approach, 
while RAG and CoALA could.

For many additional examples of memory interference across different model sizes and agent strategies, see [Appendix: Memory Interference Examples](./appendix_memory_interference.md).

---

## Irrelevant context can facilitate recall of internal knowledge
Sometimes, an LLM knows a fact but cannot recall unless prompted, despite the prompt having no relevance!
This phenomenon, while interesting, is a confounding variable in our experiments. 
The premise of CoALA is that with a well-crafted memory, learning and retrieval system, 
a large language model can tap onto these memories during reasoning to achieve better results. 
Irrelevant context enabling LLMs to score better on certain tasks can hide the true effectiveness of the memory system.

This is different from the previous section, which discusses the impact of irrelevant memories on model **reasoning** -- We are discussing the impact of irrelevant memories on model **retrieval from internal knowledge**.

### Examples
MBPP Plus task 20:
> Write a function to check if the given number is woodball or not.
```python
assert is_woodall(383) == True
```
This is a definition question, where a Woodall number is defined as a natural number of the form $n \cdot 2^n - 1$. The below 3 examples are from 4o mini:

ReAct guessed a formula that passes the public test case but failed the private test case as it got the definition wrong:

> To check if a number is a woodball number, 
> we can find the sum of consecutive integers starting from 1 and see if we can reach the given number. 
> The sum of the first `n` integers is given by the formula `n * (n + 1) / 2` ...

For RAG, the retrieved documents didn't say anything about Woodall numbers:
```
[Textbook Reference Material]:
    Title: The Inclusion-Exclusion Principle
    Part: 2/5
    ...
[/Textbook Reference Material]

[Textbook Reference Material]:
    Title: Primality tests
    Part: 2/2
    ...
[/Textbook Reference Material]

[Textbook Reference Material]:
    Title: Primality tests
    Part: 1/2
    ...
[/Textbook Reference Material]
```
but upon seeing these documents, it then realized the definition:

> 1. **Restatement of the Problem**: The task is to create a function that determines whether a given number is a Woodall number. 
> A Woodall number is defined as a number of the form $ n \cdot 2^n - 1 $ for some non-negative integer $ n $.

The same thing happened for CoALA: It retrieved summaries of its problem-solving experience, all of which are irrelevant:
```
[Summary]:
    In solving the problem of determining whether a set of matchsticks can form a square, 
    ...
[/Summary]

[Summary]:
    In this problem, the goal was to find the N'th number in a specific series: 0, 1, 5, 14, 30, 55, ... The series was actually generated by summing the squares of the first (N-1) natural numbers.
    ...
[/Summary]

[Summary]:
    In this problem, the goal was to determine if a sequence of integers could be modified to have a sum of zero
    ...
[/Summary]
```

but immediately after, it realized

> The task is to create a function that checks if a given number is a Woodall number. 
> A Woodall number is defined as a number that can be expressed in the form $ n \cdot 2^n - 1 $ for some non-negative integer $ n $.

Another instance of this is in MBPP Plus task 268
> Write a function to find the n'th star number.
```python
assert find_star_num(3) == 37
```
which is another task that requires knowing a definition. 

On 4o mini, ReAct and RAG did not know the definition, 
kept trying and eventually failed for the maximum of 4 attempts.
CoALA on the other hand realized the definition after failing once and then reflecting on its failure. 
Note that during this step, the first round's retrieved memories were not present in the message thread. 
(Retrieved memories only appear during the coding step and are removed immediately after) 
The memories retrieved by RAG and CoALA were all irrelevant.
This shows 2 things:
- Hidden internal knowledge requires specific types of prompts to be activated, even if irrelevant (RAG couldn't recall the definition despite given 4 attempts with document retrieval)
- Sometimes these prompts can be very subtle -- the influence of memories on the model's code writing process and comments within, rather than the memories themselves in the case of MBPP task 20, triggered CoALA's internal knowledge this time.

### Explaining the phenomenon
This effect observed in our experiments aligns with research on LLMs' factual recall mechanisms. 
Studies analyzing internal knowledge representation through knowledge neurons `[9]` and mechanistic interpretability `[10]` reveal that LLMs do not always retrieve relevant facts when faced with direct questions. 

`[9]` demonstrates that alternative reasoning pathways, 
triggered by external context -- even when irrelevant or misleading -- 
can enhance factual recall performance. 

`[10]` observed that inserting unrelated context shifted model outputs in 38.3% of cases for Llama-3 and almost 48.0% for Mistral.
They showed that LLMs rely on abstract class structures built during training, 
with output determined by competitive interaction between direct questioning and context-sensitive circuits. 
This could also explain why reasoning is affected by unrelated context in the previous section.
