# Discussion: Large Models

## Large Model Takes Advantage of Memory
Our results demonstrate a divergence in memory utilization effectiveness between model sizes. While memories appear to hinder smaller models like GPT-4o mini, larger models such as GPT-4o 0806 show the capacity to effectively leverage memory systems for improved performance (76.5% ReAct vs 77.5% RAG and 77.0% CoALA), suggesting that successful memory utilization requires sufficient model complexity and reasoning capacity.

### Dynamic Programming Optimization: A Case Study
MBPP Task 239:
> Write a function that takes in positive integers m and n and finds the number of possible sequences of length n, such that each element is a positive integer and is greater than or equal to twice the previous element but less than or equal to m.
```python
assert get_total_number_of_sequences(10, 4) == 4
```

ReAct implemented a naive recursive solution without memoization:
```python
def count_sequences(current_value, current_length, m, n):
    # Base case: if the sequence length is n, we have a valid sequence
    if current_length == n:
        return 1
    
    count = 0
    # Try all possible next values that are at least twice the current value
    for next_value in range(2 * current_value, m + 1):
        count += count_sequences(next_value, current_length + 1, m, n)
    
    return count

def get_total_number_of_sequences(m, n):
    total_count = 0
    # Start sequences with each possible starting value from 1 to m
    for start_value in range(1, m + 1):
        total_count += count_sequences(start_value, 1, m, n)
    
    return total_count
```
This caused an error when faced with a large $m=200,n=6$ for the private test case.

RAG retrieved a document about the "Inclusion-Exclusion Principle" (seemingly irrelevant), but it hints at using memoization with dynamic programming (stored in $d[i]$):

> ...
> 
> We will use dynamic programming. For convenience, push (1,1) to the beginning and (n,m) at the end of the obstacles array. Let's compute the numbers $d[i]$ — the number of ways to get from the starting point ($0-th$) to $i-th$, without stepping on any other obstacle ...
> 
> ...
>
> When considering an obstacle $t$ between $0$ and $i$ ($0 < t < i$), on which we can step, we see that the number of paths from $0$ to $i$ that pass through $t$ which have $t$ as the **first obstacle between start and $i$**. We can compute that as: $d[t]$ multiplied by the number of arbitrary paths from $t$ to $i$. We can count the number of "bad" ways summing this for all $t$ between $0$ and $i$.
> 
> We can compute $d[i]$ in $O(k)$ for $O(k)$ obstacles, so this solution has complexity $O(k^2)$.
> 
> ...

RAG then recognized the need for optimization and implemented memoization:
```python
def count_sequences(current, length, m, n, memo):
    # ...
    # Check if the result is already computed and stored in memo
    if (current, length) in memo:
        return memo[(current, length)]
    # ...

def get_total_number_of_sequences(m: int, n: int) -> int:
    total_sequences = 0
    memo = {}
    # Try each starting number from 1 to m
    for starting_number in range(1, m + 1):
        total_sequences += count_sequences(starting_number, 1, m, n, memo)
    
    return total_sequences
```
and passed all test cases.

CoALA retrieved an experience on an unrelated problems (integer replacement operations), leading to the same naive approach as ReAct without memoization.
> In this problem, the goal was to transform a positive integer `n` into `1` using the minimum number of operations.
>
> ...
>
> Here is the final solution for reference:
> ```python
> class Solution:
> 	def integerReplacement(self, n: int) -> int:
> 		steps = 0
> 		while n != 1:
> 			if n % 2 == 0:
> 				n //= 2
> 			else:
> 				if n == 3 or (n - 1) % 4 == 0:
> 					n -= 1
> 				else:
> 					n += 1
> 			steps += 1
> 		return steps
> ```

This example illustrates two critical insights:
- Large models can identify optimization patterns even from tangentially related memories, and
- Memory retrieval quality significantly impacts outcomes -- relevant but indirect memories (RAG) outperformed irrelevant memories (CoALA).

### Tuple Intersection and Memory-Guided Algorithm Selection: A Case Study

MBPP Task 473 demonstrates how retrieved memories can guide large models toward more appropriate algorithmic approaches through subtle algorithmic insights.

> Write a function to find the tuple intersection of elements in the given tuple list irrespective of their order.
```python
assert tuple_intersection([(3, 4), (5, 6), (9, 10), (4, 5)] , [(5, 4), (3, 4), (6, 5), (9, 11)]) == {(4, 5), (3, 4), (5, 6)}
```

ReAct implemented a solution using `frozenset` to handle order-insensitive comparison:
```python
def tuple_intersection(list1, list2):
    # Convert each tuple in list1 to a set and store in set1
    set1 = {frozenset(t) for t in list1}
    
    # Convert each tuple in list2 to a set and store in set2
    set2 = {frozenset(t) for t in list2}
    
    # Find the intersection of set1 and set2
    intersection = set1.intersection(set2)
    
    # Convert each frozenset in the intersection back to a sorted tuple
    result = {tuple(sorted(s)) for s in intersection}
    
    return result
```
The use of `frozenset` would discard duplicate elements within tuples, causing ReAct to fail a test case where tuples contain repeated elements.

RAG retrieved a textbook document about "Comparison to sorting" which discussed different algorithmic approaches for finding intersections:

> It is often possible to solve a problem using either data structures or sorting. Sometimes there are remarkable differences in the actual efficiency of these approaches...
>
> Instead of data structures, we can use sorting. First, we sort both lists A and B. After this, we iterate through both the lists at the same time and find the common elements...

Influenced by this memory about sorting being an effective approach for comparison problems, RAG implemented a more robust solution using tuple sorting which passed all test cases:
```python
def tuple_intersection(list1, list2):
    # Convert each tuple in list1 to a sorted tuple and store in set1
    set1 = {tuple(sorted(t)) for t in list1}
    
    # Convert each tuple in list2 to a sorted tuple and store in set2
    set2 = {tuple(sorted(t)) for t in list2}
    
    # Find the intersection of set1 and set2
    intersection = set1.intersection(set2)
    
    # Return the intersection
    return intersection
```

CoALA retrieved a reflection on its prior problem solving experience:
> ...
> 
> 2. **Sorting and Counting**: Both solutions involve sorting the scores and counting the number of decreases in the number of contestants. The official solution uses a simple loop with `zip` to compare consecutive elements, which is a clean and efficient way to count decreases.
>
> ...
>
> 4. **Output**: The official solution constructs a final list of problem indices by iterating over sorted difficulty scores and their associated problem indices. This approach is clear and ensures the correct order of output.
> 
> ...

which encouraged it to consider iterating over and sorting as well. 
It then implemented a similar solution to RAG and passed all test cases.

This example illustrates how **algorithmically-relevant memories can guide large models toward more principled solutions**. 
The retrieved memories about sorting provided both RAG and CoALA with the insight that sorting is often preferable to complex data structures for comparison problems, 
leading them to choose `tuple(sorted(t))` over `frozenset(t)`. 
This demonstrates that large models can extract and apply meta-algorithmic insights from retrieved memories, 
even when the specific problem domains differ from the memory content.

### Subtle Memory Influences: Weak Positive Effects

Beyond the clear-cut examples of memory advantage, there exist subtler cases where retrieved memories appear to provide weak but beneficial signals to large models. While these influences are more difficult to definitively attribute to memory content, they suggest that large models can extract value even from tangentially related or partially relevant memories.

These cases demonstrate the nuanced nature of memory utilization in large models, where even indirect cues can contribute to improved problem-solving approaches. For detailed examples and analysis of these subtle influences, see [Appendix: Weak Positive Examples](appendix_weak_positive.md).

---

## Large Model Might Not Always Utilize Memories Effectively

MBPP Task 781 presents a particularly intriguing example of how memory-augmented models can retrieve similar relevant information yet apply it differently, demonstrating that memory access alone does not guarantee successful utilization.

> Write a python function to check whether the count of divisors is even.
```python
assert count_divisors(10)
```

This problem is similar to MBPP task 126 discussed in the positive case of the 
[small models section](discussion_small_models.md#small-models-can-still-benefit-from-good-memories), 
where the trick is to realize that efficient divisor counting can be achieved by iterating only up to the square root of n.

ReAct implemented a straightforward but inefficient approach, iterating through all numbers from 1 to n:
```python
def count_divisors(n: int) -> bool:
    # Initialize the count of divisors to 0
    count = 0
    
    # Iterate over all numbers from 1 to n
    for i in range(1, n + 1):
        # Check if i is a divisor of n
        if n % i == 0:
            # Increment the count of divisors
            count += 1
    
    # Check if the count of divisors is even
    return count % 2 == 0
```
This O(n) solution passed the public test case but failed on larger private test cases due to timeout.

CoALA retrieved a summary from its semantic memory about a previous problem involving divisor counting:

> In this problem, the core concept was to determine the number of divisors of the absolute difference between two numbers...
>
> ### Key Insights:
> ...
> - **Divisor Counting**: Efficiently counting divisors involves iterating up to the square root of the number and checking for divisibility.
>
> ...
> ### Code Snippet:
> ```python
> def countDivisors(n):
>     count = 0
>     i = 1
>     while i * i <= n:
>         if n % i == 0:
>             count += 1
>             if i != n // i:
>                 count += 1
>         i += 1
>     return count
> ```
> ...

Guided by this memory, CoALA successfully implemented the optimized O(√n) approach:
```python
def count_divisors(n: int) -> bool:
    # Initialize the count of divisors to 0
    count = 0
    
    # Iterate over each number from 1 to the square root of n
    i = 1
    while i * i <= n:
        # If i is a divisor of n
        if n % i == 0:
            # Increment the count for the divisor i
            count += 1
            # If i is not the square root of n, increment for the paired divisor
            if i != n // i:
                count += 1
        i += 1
    
    # Return True if the count of divisors is even, otherwise False
    return count % 2 == 0
```
This solution passed both public and private test cases.

RAG retrieved highly relevant textbook content that explicitly described the optimization technique:

> # Number of divisors / sum of divisors
>
> In this article we discuss how to compute the number of divisors $d(n)$ and the sum of divisors $\sigma(n)$ of a given number $n$.
>
> ...
>
> ```cpp
> long long numberOfDivisors(long long num) {
>     long long total = 1;
>     for (int i = 2; (long long)i * i <= num; i++) {
>         if (num % i == 0) {
>             int e = 0;
>             do {
>                 e++;
>                 num /= i;
>             } while (num % i == 0);
>             total *= e + 1;
>         }
>     }
>     if (num > 1) {
>         total *= 2;
>     }
>     return total;
> }
> ```
> ...

Despite having access to this textbook that clearly demonstrated iterating only up to the square root (`i * i <= num`), RAG implemented the same naive O(n) approach as ReAct and consequently failed the private test cases.

This is yet another confounding factor in evaluating agent performance: 
even if the retrieval is accurate, the agent's usage of it can be inconsistent. 
We hypothesize that since the textbook entry is long, 
"Lost in the middle" effects might have caused RAG to overlook the crucial optimization details.

---

## Memory-Induced Bias: The Double-Edged Sword
Previously, we found that memories can influence small models to a large extent, 
for the worse on average. 
Large models are also susceptible to such influence, though to a lesser degree.

**MBPP Task 93: Exponentiation Function**
> Write a function to calculate the value of 'a' to the power 'b'.
```python
assert power(3,4) == 81
```

ReAct and the ground truth implemented the straightforward solution using Python's built-in exponentiation operator `a ** b`. 
This passed all test cases, including the challenging private test case with `power(4, -2)`.

Both RAG and CoALA retrieved the same textbook memory about "Binary Exponentiation":
> # Binary Exponentiation
> 
> Binary exponentiation (also known as exponentiation by squaring) is a trick which allows to calculate $a^n$ using only $O(\log n)$ multiplications (instead of $O(n)$ multiplications required by the naive approach).
> 
> ...
> 
> Raising $a$ to the power of $n$ is expressed naively as multiplication by $a$ done $n - 1$ times: $a^{n} = a \cdot a \cdot \ldots \cdot a$. However, this approach is not practical for large $a$ or $n$.

Influenced by this memory emphasizing "repeated multiplication" and discussing positive integer exponents, both RAG and CoALA implemented iterative multiplication approaches:
```python
def power(a: int, b: int) -> int:
    # Initialize the result to 1, as any number to the power of 0 is 1
    result = 1
    # Multiply result by 'a', 'b' times
    for _ in range(b):
        result *= a
    # Return the final result which is a^b
    return result
```
This failed the private test case `power(4, -2)` as the iterative multiplication approach only works for non-negative integer exponents: 
When faced with `power(4, -2)`, the loop `for _ in range(-2)` doesn't execute.

While the retrieved textbook content was mathematically correct and sophisticated, 
it led RAG and CoALA to overthink a simple problem. 
They abandoned Python's built-in `**` operator (which correctly handles negative exponents) in favor of manual iterative multiplication, 
introducing unnecessary complexity and failing on negative exponents.

---

## Why does CoALA fare worse than RAG for large models? 
Our analysis reveals that **CoALA's expanded memory bank can paradoxically hinder performance through false positives during vector retrieval**. 
While both systems access the same competitive programming textbooks, 
CoALA's additional episodic memories, reflections, summaries, 
and procedural skills often introduce noise that displaces relevant knowledge.

This pattern appears consistently across multiple problems. 
In MBPP 239 (discussed earlier), RAG retrieved optimization hints about memoization while CoALA retrieved an irrelevant integer replacement problem. 
Similarly, in MBPP 299 below, we see how memory quality affects edge case handling:


MBPP Task 299:
> Write a function to calculate the maximum aggregate from the list of tuples.
```python
assert max_aggregate([('Juan Whelan',90),('Sabah Colley',88),('Peter Nichols',7),('Juan Whelan',122),('Sabah Colley',84)])==('Juan Whelan', 212)
```

ReAct implemented a naive solution which iterates through the list of tuples and maintains a running total for each contestant:
```python
def max_aggregate(tuples_list):
    # Initialize a dictionary to store the total scores for each name
    scores_dict = {}

    # Iterate through each tuple in the list
    for name, score in tuples_list:
        # ...
    
    # Initialize variables to track the name with the maximum score
    max_name = None
    max_score = 0

    # Iterate through the dictionary to find the name with the highest total score
    # ...
```
This approach failed a private test case when all scores are negative, 
as the initial `max_score` is set to zero.

RAG retrieved a document which appears irrelevant, 
but hinted at the need to consider negative values in the aggregation:
> ## Related tasks
>
> ### Finding the maximum/minimum subarray with constraints
>
> If the problem condition imposes additional restrictions on the required segment $[l, r]$ (for example, that the length $r-l+1$ of the segment must be within the specified limits), ...
>
> ...
>
> ### Search for a subarray with a maximum/minimum average
> ...
> 
> To solve this subproblem, subtract $x$ from each element of array $a[]$. Then our subproblem actually turns into this one: whether or not there are positive sum subarrays in this array.
> 
> ...

The textbook discussion about finding maximum elements and handling various constraints provided algorithmic guidance. 
RAG implemented a robust solution using Python's built-in maximum finding:
```python
def max_aggregate(data: list) -> tuple:
    # Initialize an empty dictionary to store the aggregate sums for each name
    aggregates = {}
    
    # Iterate over each tuple in the list
    for name, number in data:
        # If the name is not in the dictionary, add it with the current number
        if name not in aggregates:
            aggregates[name] = number
        else:
            # If the name is already in the dictionary, add the number to its current value
            aggregates[name] += number
    
    # Find the name with the maximum aggregate sum
    max_name = max(aggregates, key=aggregates.get)  # Robust approach!
    max_sum = aggregates[max_name]
    
    # Return the name and the maximum sum as a tuple
    return (max_name, max_sum)
```
which passed all test cases.

CoALA retrieved an irrelevant reflection about a previous problem involving sorting and counting:
> The problem was straightforward, and my solution was correct and efficient. However, reflecting on the official solution provides some insights:
>
> 1. **Data Structures**: The official solution uses a dictionary to map scores to the number of contestants, which is a neat way to handle the association between scores and contestants...
>
> 2. **Sorting and Counting**: Both solutions involve sorting the scores and counting the number of decreases in the number of contestants...
> 
> ...

It then went on to implement the same solution as ReAct and failed the private test case.

### Implications for Memory System Design
These examples highlight a challenge: 
**vector-based retrieval alone may not be the optimal approach for large, diverse memory banks**. 
The semantic similarity scores that guide retrieval can be misleading when memories span multiple domains and problem types. 
A document about "integer operations" might score similarly for both dynamic programming and arithmetic problems, 
despite containing knowledge relevant to only one.

Furthermore, the presence of multiple memory types (episodic, semantic, procedural) in CoALA creates additional opportunities for retrieving tangentially related but ultimately unhelpful information. 

This suggests that future work should investigate more sophisticated retrieval mechanisms beyond vector retrieval.
