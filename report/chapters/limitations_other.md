# Limitations: Other

Here are some potential factors beyond memory which could confound the results of our findings. 

## MBPP Plus Benchmark Limitations

The MBPP Plus benchmark, while widely used for evaluating code generation capabilities, contains several categories of issues that can confound experimental results and lead to misleading performance comparisons between agent strategies. Here are some of them:

### Ambiguous Mathematical Problem Specifications

**Linear Diophantine Equation Problem (MBPP 160)**:
> Write a function that returns integers x and y that satisfy ax + by = n as a tuple, or return None if no solution exists.
```python
assert find_solution(2, 3, 7) == (2, 1)
```

This specification is mathematically ambiguous as multiple valid solutions exist for most inputs, but only one specific solution is accepted. 
On 4o mini:

ReAct uses a simple loop assuming non-negative constraints:
```python
def find_solution(a: int, b: int, n: int) -> tuple[int, int] | None:
    # Iterate through possible values of x
    for x in range(n // a + 1):
        # Calculate the corresponding value of y
        if (n - a * x) % b == 0:  # Check if (n - ax) is divisible by b
            y = (n - a * x) // b
            if y >= 0:  # Ensure y is non-negative
                return (x, y)  # Return the solution as a tuple
    return None  # Return None if no solution is found
```
which is similar to the ground truth. This passes all test cases, one of which is
```python
assert find_solution(1,13,17) == (4, 1)
```

RAG and CoALA managed to retrieve a document that directly matches the problem:

> `[Textbook Reference Material]:`
> 
>    Title: Linear Diophantine Equation
>    ...
>
>    A Linear Diophantine Equation (in two variables) is an equation of the general form:
> 
>    $$ax + by = c$$
> 
>    where $a$, $b$, $c$ are given integers, and $x$, $y$ are unknown integers.
> 	  ...
> 	
>    To find one solution of the Diophantine equation with 2 unknowns, you can use the `[Extended Euclidean algorithm](extended-euclid-algorithm.md)`. First, assume that $a$ and $b$ are non-negative. When we apply Extended Euclidean algorithm for $a$ and $b$, we can find their greatest common divisor $g$ and 2 numbers $x_g$ and $y_g$ such that:
> 
>    $$a x_g + b y_g = g$$
>    ...
>
> `[/Textbook Reference Material]`


it then implements the solution
```python
def find_solution(a: int, b: int, n: int) -> tuple[int, int] | None:
    g = gcd(a, b)
    if n % g != 0:
        return None  # No solution exists
        
	# Find one solution using Extended Euclidean Algorithm
    x0, y0 = extended_euclidean(a, b)
    x0 *= n // g
    y0 *= n // g
    # Complex adjustment logic to find more solutions...
```
However, this returns `(17, 0)` for `find_solution(1,13,17)` which is valid from the problem description, but it fails the assertion.


### Edge Case Specification Gaps
**Matrix Column Access (MBPP 611)**: 
> Write a function which given a matrix represented as a list of lists returns the max of the n'th column.
```python
assert max_of_nth([[5, 6, 7], [1, 3, 5], [8, 9, 19]], 2) == 19
```
The problem expects negative indices to be treated as valid column references, but this behavior isn't documented in the problem description, causing agents **with** input validation to fail.

On 4o 0806,

ReAct passed the column number directly as an index
```python
def max_of_nth(matrix, n):
    # Initialize an empty list to store the values of the n-th column
    column_values = []
    
    # Iterate over each row in the matrix
    for row in matrix:
        # Append the n-th element of the current row to column_values
        column_values.append(row[n])
    
    # Return the maximum value from the collected n-th column values
    return max(column_values)
```
and passed all test cases.

RAG practiced input validation:
```python
def max_of_nth(matrix, n):
    # Check if the matrix is empty or if n is not a valid column index
    if not matrix or n < 0 or n >= len(matrix[0]):
        return None
    ...
```
and subsequently failed a private test case where $n=-1$

**String Integer Validation (MBPP 113)**:
>Write a function to check if a string represents an integer or not.
```python
assert check_integer("python")==False
```

The specification lacks crucial details:
- How to handle empty strings
- Expected return type for invalid inputs (`None` vs `False`)

On 4o mini, CoALA returned `False` for empty strings (which makes sense since the assertion uses `False`)
```python
def check_integer(s: str) -> bool:
    # Check if the string is empty
    if not s:
        return False
	...
```
but failed the private test case of an empty string, and the ground truth expects a `None` return.

### Implicit Type Constraints

**Maximum Value in Heterogeneous Lists (MBPP 294)**:
> Write a function to find the maximum value in a given heterogeneous list.
```python
assert max_val(['Python', 3, 2, 4, 5, 'version'])==5
```
The specification doesn't explicitly state that the result must be an integer (not float) which the ground truth implies.

On 4o 0806,

ReAct checked for ints and floats
```python
def max_val(lst):
    # Initialize a list to store numeric values
    numeric_values = []
    
    # Iterate over each item in the input list
    for item in lst:
        # Check if the item is an integer or a float
        if isinstance(item, (int, float)):
            # Add the numeric item to the numeric_values list
            numeric_values.append(item)
    
    # Return the maximum value from the numeric_values list
    return max(numeric_values)
```
and failed private test cases.

RAG somehow checked for ints only
```python
def max_val(lst):
    # Initialize max_value to a very small number
    max_value = float('-inf')
    
    # Iterate over each element in the list
    for element in lst:
        # Check if the element is an integer
        if isinstance(element, int):
            # If the element is greater than the current max_value, update max_value
            if element > max_value:
                max_value = element
    
    # Return the maximum integer found
    return max_value
```
probably influenced by the retrieved document mentioning subarray problems that deal with integers, and passed all test cases.

A similar case can be found in MBPP 410.

### Impact on Agent Evaluation
The limitations above are just a sample; More examples can be found in previous [experiments](https://github.com/nicholaschenai/voyager_coder_experiments/blob/main/report/APPENDIX.md#invalid--ambiguous-error-analysis)

These limitations create several evaluation issues:
- False Performance Gaps: Agents appear to perform differently due to specification interpretation rather than reasoning capabilities
- Memory Interference Effects: For memory-augmented agents (RAG, CoALA), retrieved memories can accidentally bias the interpretation of ambiguous problems for better or worse, confounding performance metrics

For future experiments, we might want to focus on cleaner benchmarks or use multiple benchmarks to average out such effects.

---

## High Problem-Level Variability with Minimal Net Performance Difference

A critical observation from our error analysis is the disparity between the total number of problems changing state 
(Pass↔Fail) across different strategies and the minimal net difference in overall accuracy. 
This raises questions about the reliability and interpretability of our experimental results.

### Quantifying State Changes vs. Net Performance

For GPT-4o mini, we observed 28-30 problems changing state between strategies (Pass→Fail or Fail→Pass), while the net accuracy difference was only equivalent to 4-8 problems. 
Similarly, for GPT-4o 0806, 16-18 problems changed state, 
with accuracy differences equivalent to 2-4 problems.

This substantial ratio of state changes to net difference strongly suggests that what appears as performance variation may primarily reflect noise rather than meaningful differences in capabilities. 

As detailed in our memory limitations analysis, much of this variability stems from how irrelevant or tangentially relevant memories unpredictably influence model behavior.

### Filtered Analysis Results

To identify genuine performance differences, 
we conducted a detailed analysis of all state changes for GPT-4o 0806, 
removing problems with ambiguous specifications, edge cases, 
or clear memory interference effects. The filtered results revealed:

#### RAG-CoALA Comparison
- Pass→Fail: 2 problems (239, 299)
- Fail→Pass: 1 problem (781)
- Verdict: RAG performs better than CoALA by 0.26%

#### ReAct-CoALA Comparison
- Pass→Fail: 1 problem (93)
- Fail→Pass: 3 problems (473, 792, 781)
- Verdict: CoALA performs better than ReAct by 0.53%

#### ReAct-RAG Comparison
- Pass→Fail: 1 problem (93)
- Fail→Pass: 3 problems (473, 752, 239)
- Verdict: RAG performs better than ReAct by 0.53%

### Implications for Evaluation
These razor-thin margins (0.26-0.53%) after filtering out noise-induced variations lead us to three conclusions:

- The performance differences between strategies are too small to draw definitive conclusions about the effectiveness of different memory-augmented approaches. (Inconclusive)

- The vast majority of performance variations appear to be artifacts of memory interference and benchmark limitations rather than differences in reasoning capabilities.

- Further experimentation with more rigorous benchmarks, more advanced models and larger sample sizes is required to elucidate the genuine benefits of cognitive architecture approaches. 
