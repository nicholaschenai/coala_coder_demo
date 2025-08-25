# Discussion: Small Models

## Why do memories appear to hinder small models?
We saw from the results that for 4o mini, RAG (72.8%) and CoALA (73.8%) fare worse than ReAct (74.9%). 
This section compares trajectories of 4o mini across these 3 strategies to understand why this is the case.
In short, while memories can help or hinder 4o mini depending on the scenario, the net effect is negative. 

### Small models are over-sensitive to subtle cues in memory
Since RAG and CoALA share the same problem-solving framework as ReAct, 
(empty memories for RAG and CoALA result in the same behavior as ReAct),
if RAG and CoALA retrieved irrelevant memories, 
a model capable of reasoning should be able to ignore them and perform as well as ReAct.
This is not the case and implies that small models might be **over-sensitive** to subtle cues in memory, 
for worse on average.

The first example is on MBPP 274:
> Write a python function that takes in a positive integer $n$ and finds the sum of even index binomial coefficients.
```python
assert even_binomial_Coeff_Sum(4) == 8
```

ReAct naively looped over the series and calculated the binomial coefficients via factorials.
```python
def factorial(num):
    # Helper function to calculate factorial of a number
    if num == 0 or num == 1:
        return 1
    result = 1
    for i in range(2, num + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    # Helper function to calculate binomial coefficient C(n, k)
    return factorial(n) // (factorial(k) * factorial(n - k))
```
While not optimal (the ground truth solution uses a closed form expression), it passed both public and private test cases.

RAG retrieved relevant documents on calculating binomial coefficients and saw the recurrence formula
>    ...
>    Binomial coefficients can be
>    recursively calculated as follows:
>    $$
>    {n \choose k}  =  {n-1 \choose k-1} + {n-1 \choose k}
>    $$
>    ...

causing it to calculate the binomial coefficients using the recurrence relation.

```python
def binomial_coefficient(n, k):
    if k == 0 or k == n:
        return 1
    return binomial_coefficient(n - 1, k - 1) + binomial_coefficient(n - 1, k)
```
While this solution passed the public test case, it failed the private test case where $n=100$ 
as the recursion depth exceeded the limit.

Surprisingly, in a retrieved document further down, 
there was actually a guide to calculate the binomial coefficients more effectively by storing the values rather than use recursion.
```cpp
const int maxn = ...;
int C[maxn + 1][maxn + 1];
C[0][0] = 1;
for (int n = 1; n <= maxn; ++n) {
	C[n][0] = C[n][n] = 1;
	for (int k = 1; k < n; ++k)
		C[n][k] = C[n - 1][k - 1] + C[n - 1][k];
}
```
This suggests that small models **might not effectively use memories**, even if it is in the context. 

Another example is on MBPP Plus task 293:

> Write a function to find the third side of a right angled triangle.
```python
assert otherside_rightangle(7,8)==10.63014581273465
```
This is just Pythagoras' theorem.
We can see from the test case that the hypotenuse is the output as it is the longest side.

The model's first thought (used by all 3 strategies since this happens before retrieval) 
is to assume that one of the inputs is the hypotenuse, and it needs to guess which is it:

> ...
> 3. **Write a pseudocode solution**:
>    ```
>    Function otherside_rightangle(side1, side2):
>        If side1 is greater than side2:
>            hypotenuse = side1
>            other_side = sqrt(hypotenuse^2 - side2^2)
>        Else:
>            hypotenuse = side2
>            other_side = sqrt(hypotenuse^2 - side1^2)
>        Return other_side
>    ```
> ...

ReAct implemented this, failed the test case, but self-corrected on the second attempt:
> 2. **Identifying the Error**: In the previous solution, I incorrectly assumed that one of the provided sides could be the hypotenuse. 
> However, the problem statement implies that we are always given the two shorter sides of the triangle, 
> and we need to calculate the hypotenuse using the Pythagorean theorem.

On the other hand, RAG retrieved a document that directly states the Pythagorean theorem:

> A \key{distance function} defines the distance between
> two points.
> The usual distance function is the
> \key{Euclidean distance} where the distance between
> points $(x_1,y_1)$ and $(x_2,y_2)$ is
> $\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}.$

and answered the question correctly on the first attempt.

CoALA on the other hand, retrieved a memory that considered various cases of the triangle sides:

> ...
>     This function reads multiple test cases from standard input, where each test case consists of two integers representing the height and area of a triangle. It processes each test case to calculate the possible side lengths of a triangle that can be formed with the given height and area. 
> ...
```python
def find_triangle(H, S):
	# Calculate the value of 2 * S
	area_double = 2 * S

	# Calculate the discriminant for the quadratic equation
	discriminant = H**4 - 4 * (area_double**2)

	if discriminant < 0:
		return -1  # No valid triangle exists

	# Calculate the two possible values for a
	a1 = ((H**2 + discriminant**0.5) / 2)**0.5
	a2 = ((H**2 - discriminant**0.5) / 2)**0.5

	# Calculate corresponding b values
	b1 = (H**2 - a1**2)**0.5
	b2 = (H**2 - a2**2)**0.5

	# Prepare the results
	sides1 = sorted([a1, b1, H])
	sides2 = sorted([a2, b2, H])

	# Check if the sides are valid
	if sides1[0] > 0 and sides1[1] > 0:
		return sides1
	if sides2[0] > 0 and sides2[1] > 0:
		return sides2

	return -1  # No valid triangle exists
```
> ...

As such, its solution also considered various cases:
```python
def calculate_hypotenuse(a, b):
    # Calculate the hypotenuse using the Pythagorean theorem
    return (a**2 + b**2)**0.5

def calculate_other_side(hypotenuse, side):
    # Calculate the other side using the Pythagorean theorem
    return (hypotenuse**2 - side**2)**0.5

def otherside_rightangle(side1, side2):
    # Check if either side is the hypotenuse
    if side1 > side2:  # side1 is the hypotenuse
        return calculate_other_side(side1, side2)
    else:  # side2 is the hypotenuse or both are legs
        return calculate_hypotenuse(side1, side2)
```
While it passed the public test case as it fits the correct branch of the if statement, 
it failed a private test case when the other branch is followed.

In older experiments (not yet released), 
we found that 4o mini was so strongly influenced that the APPS formatting during training is practised in MBPP Plus during testing. 
Usually the model can recover after seeing the error message from the execution, 
but occasionally it gets stuck in a loop, unable to recover to submit an answer. 
Formatting examples include:
- Wrong indentation
- Calling the function (especially naming it as `main`) to read and write from IO despite instructions in MBPP Plus to write a function of a specific name which does not deal with the IO 

### Small models handle long contexts poorly
Our experiments accumulate past attempts in a message thread, just like in USACO-Bench `[3]` and Reflexion `[11]`.

In a [previous experiment](https://github.com/nicholaschenai/voyager_coder_experiments/tree/main/report), 
we evaluated a variant of ReAct where we do not accumulate the past messages, 
and instead insert previous round results (if it exists) into the context. 
On GPT 4o-mini, this scored 76.2% which is an improvement over the current 74.9%.
This suggests that long context degrades small models' performance.
For a full discussion of why this is so, we refer the reader to the previous experiment's report.

It follows that since memories increase the length of the context, 
strategies with memories can fare worse than ReAct, especially when the memories are not relevant.

## Small models can still benefit from good memories

Despite the net negative impact of memories on small models, 
there are specific instances where well-targeted memories enable small models to achieve better solutions than the memory-free ReAct baseline. 
These cases demonstrate that mitigating the downside from irrelevant or low-quality memories can unlock the potential of cognitive architectures and lead to improved performance.

**Algorithm Optimization Through Memory Guidance**

MBPP 126:
> Write a python function to find the sum of common divisors of two given numbers.
```python
assert sum(10,15) == 6
```

ReAct used a straightforward brute force approach that iterates through all numbers up to the minimum of the two inputs (O(min(a,b))), causing it to fail the private test case of inputs (987654321, 123456789) due to time limit exceeded (TLE).

RAG retrieved a document about the Euclidean algorithm for computing the greatest common divisor (GCD), which led it to recognize that
> we can find the greatest common divisor (GCD) of the two numbers, as all common divisors will be divisors of the GCD

This insight resulted in a more efficient algorithm that computes the GCD first, then finds its divisors.
```python
def gcd(a, b):
    while b != 0:
        a, b = b, a % b  # Update a and b using the Euclidean algorithm
    return a  # Return the GCD

def sum(a: int, b: int) -> int:
    gcd_value = gcd(a, b)  # Find the GCD of a and b
    sum_of_divisors = 0
    for i in range(1, gcd_value + 1):  # Iterate from 1 to gcd_value
        if gcd_value % i == 0:  # Check if i is a divisor of gcd_value
            sum_of_divisors += i  # Add i to the sum
    return sum_of_divisors  # Return the total sum of common divisors
```
However, that too also caused it to TLE on a larger test case (987654321, 987654321)

> [!Aside]
> The model seems to be slightly confused from its thought:
> "For example, for the numbers 10 and 15, the common divisors are 1, 5, and 10, and their sum is 6."
> since 10 is not a divisor of 15.

CoALA went even further by retrieving both GCD knowledge shown above, and previous experience with divisor counting optimizations on a different problem:
> `[Summary]:`
>
> 	... 
> 
> 	...the task reduces to counting the divisors of the absolute difference.
> 
>    The solution involved creating a function to count the divisors of a number, which iterates up to the square root of the number to efficiently find all divisors
> 
> 	...
> 
>    ```python
>     def count_divisors(n):
>         count = 0
>         for i in range(1, int(n**0.5) + 1):
>             if n % i == 0:
>                 count += 1
>                 if i != n // i:
>                     count += 1
>         return count
>    ``` 
> 	...
> 
> `[/Summary]`

This combination of memories enabled CoALA to implement the most optimized solution
```python
def gcd(a, b):
    # Calculate the greatest common divisor using the Euclidean algorithm
    while b != 0:
        a, b = b, a % b
    return a

def sum_of_divisors(n):
    # Calculate the sum of all divisors of n
    total = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            total += i  # i is a divisor
            if i != n // i:
                total += n // i  # n // i is also a divisor
    return total

def sum(a: int, b: int) -> int:
    # Find the GCD of a and b
    g = gcd(a, b)
    # Return the sum of the divisors of the GCD
    return sum_of_divisors(g)
```
which passes all test cases, demonstrating how multiple relevant memory sources can compound to produce superior algorithmic choices.
