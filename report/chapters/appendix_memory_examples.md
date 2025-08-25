# CoALA memory examples

Below are examples of different memory types found in our implementation of CoALA.

### 1. **Semantic Memory (Summary)**
Found in multiple test problems, these are episode-level summaries capturing key concepts:

**Example:**
> In this problem, the goal was to transform a positive integer `n` into `1` using the minimum number of operations. The operations allowed were dividing by 2 if `n` is even, or incrementing/decrementing by 1 if `n` is odd. The core concept here is to efficiently reduce `n` by leveraging the properties of even and odd numbers.
> 
> The key strategy was to always divide by 2 when `n` is even, as this is the most efficient way to reduce the number. For odd numbers, the decision to increment or decrement was based on the resulting number's divisibility by 4...

### 2. **Semantic Memory (Textbook Reference Material)**
Competitive programming knowledge from USACO Bench:

**Example:**
> Title: Catalan Numbers
> Part: 1/1
> # Catalan Numbers
> Catalan numbers is a number sequence, which is found useful in a number of combinatorial problems, often involving recursively-defined objects.
> 
> This sequence was named after the Belgian mathematician Catalan...
> 
> The first few Catalan numbers $C_n$ (starting from zero):
> $1, 1, 2, 5, 14, 42, 132, 429, 1430, \ldots$
> 
> ### Application in some combinatorial problems
> The Catalan number $C_n$ is the solution for
> - Number of correct bracket sequence consisting of $n$ opening and $n$ closing brackets...

### 3. **Semantic Memory (Reflection)**
Comparative analysis between agent's approach and official solutions:

**Example:**
> Reflecting on the problem-solving process for this pattern generation task, I encountered a few key insights:
> 
> 1. **Pattern Understanding**: The main challenge was correctly understanding the pattern generation logic. The pattern required alternating sequences of numbers, which was not immediately obvious. The official solution effectively captures this by using a list to manage the sequence and adjusting it iteratively.
> 
> 2. **Iterative Adjustment**: The official solution uses a list to build the sequence and then iteratively adjusts it by popping the last element and prepending a new number...

### 4. **Episodic Memory** 
Complete transition tuples with task, critique, code, feedback, and result:

**Example:**
```
[Past Memory]:
    [Task]:
        Given an encoded string, return it's decoded string.
        The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is ...

    [Previous Critique]:
        None

    [Thought Process and Code]:
        1. **Restate the problem in plain English:**
           We are given a string that is encoded using a specific pattern...
        [Full solution with code]

    [Environment Feedback]:
        Tests passed: Input: ['\"3[a]2[bc]\"'] Output: "aaabcbc"

    [Result]:
        Success
```

### 5. **Procedural Memory (Reference Code - Not callable)**
Non-standalone code patterns with descriptions and usage scenarios:

**Example:**
```
[Reference Code (Not callable)]:
    [description for function: generate_pattern]
    The function takes an integer T and a list of test cases, where each test case is an integer K...

    [end of description]
    This knowledge will be useful in scenarios where one needs to generate specific patterns based on numerical input...

    def generate_pattern(T, test_cases):
        for K in test_cases:
            for i in range(1, K + 1):
                line = ""
                for j in range(i):
                    if j % 2 == 0:  # Even index
                        line += "1"
                    else:           # Odd index
                        line += "0"
                print(line)
```

### 6. **Procedural Memory (Callable Code)**
> `[description for function: count_col_triang]`
> This function calculates the number of non-collinear triangles that can be formed from a set of points, categorized by their colors. It first organizes the points by color and then counts the triangles for each color by checking combinations of three points for collinearity. The function keeps track of the total number of triangles and identifies the color(s) with the maximum triangle count. Finally, it returns a summary that includes the total number of points, the number of unique colors, the total number of triangles, and a list of the color(s) with the maximum triangle count along with their respective counts. If no triangles can be formed, it returns a specific output indicating this. The function effectively combines geometric calculations with data organization to provide insights into the distribution of colored points.
> 
> `[end of description]`
> 
> This knowledge is useful in scenarios where one needs to analyze geometric properties of points in a plane, particularly in computational geometry, game development, or graphics programming. It can help in determining the relationships between points based on their colors, which can be applied in clustering algorithms, visual data representation, or even in solving problems related to triangulation in various fields such as computer graphics, robotics, and geographic information systems (GIS). Understanding how to count and categorize triangles formed by points can also be beneficial in mathematical modeling and simulations.
```python
def count_col_triang(points):
    from collections import defaultdict
    from itertools import combinations

    # Step 1: Organize points by color
    color_points = defaultdict(list)
    for point in points:
        color_points[point[1]].append(point[0])

    # Step 2: Initialize variables for results
    total_points = len(points)
    unique_colors = len(color_points)
    total_triangles = 0
    triangle_counts = {}

    # Step 3: Calculate triangles for each color
    for color, pts in color_points.items():
        num_points = len(pts)
        if num_points >= 3:
            # Calculate the number of combinations of 3 points
            triangles = 0
            for comb in combinations(pts, 3):
                # Check for collinearity using the determinant method
                x1, y1 = comb[0]
                x2, y2 = comb[1]
                x3, y3 = comb[2]
                if (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) != 0:
                    triangles += 1
            triangle_counts[color] = triangles
            total_triangles += triangles

    # Step 4: Determine the maximum triangle count and colors
    max_triangles = 0
    max_colors = []
    for color, count in triangle_counts.items():
        if count > max_triangles:
            max_triangles = count
            max_colors = [color]
        elif count == max_triangles:
            max_colors.append(color)

    # Step 5: Prepare the final output
    if total_triangles == 0:
        return [total_points, unique_colors, total_triangles, []]
    
    max_color_count = triangle_counts[max_colors[0]] if max_colors else 0
    return [total_points, unique_colors, total_triangles, [*sorted(max_colors), max_color_count]]
```