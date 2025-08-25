# Appendix: Subtle influence
This shows the effect of subtle influence of irrelevant memories impacting a model's outputs which then lead it to get the right answer.

This is on MBPP 237 for 4o mini.
Their first thought process is as follows, and note how similar they are.
Note that subsequently, ReAct could not self-correct to get the question right, 
while RAG and CoALA could.

ReAct:
>  1. **Restate the problem in plain English:**
>    We need to create a function that takes a list of tuples as input and returns a dictionary. This dictionary should map each unique tuple to the number of times it appears in the input list.
> 
> 2. **Conceptualize a solution first in plain English:**
>    To solve this problem, we can iterate through the list of tuples and keep track of how many times each tuple appears. We can use a dictionary to store the tuples as keys and their counts as values. For each tuple in the list, we will check if it is already in the dictionary. If it is, we will increment its count; if it is not, we will add it to the dictionary with a count of 1. Finally, we will return the dictionary.
> 
> 3. **Write a pseudocode solution:**
>    ```
>    function check_occurences(tuples_list):
>        create an empty dictionary called occurrences
>        for each tuple in tuples_list:
>            if tuple is in occurrences:
>                increment occurrences[tuple] by 1
>            else:
>                set occurrences[tuple] to 1
>        return occurrences
>    ```
> 
> 4. **Output the final Python 3 solution with your solution steps in comments:**
> ```python
> def check_occurences(tuples_list):
>     # Create an empty dictionary to store occurrences
>     occurrences = {}
>     
>     # Iterate through each tuple in the input list
>     for tup in tuples_list:
>         # Check if the tuple is already in the dictionary
>         if tup in occurrences:
>             # Increment the count for this tuple
>             occurrences[tup] += 1
>         else:
>             # Add the tuple to the dictionary with a count of 1
>             occurrences[tup] = 1
>             
>     # Return the dictionary containing the counts of each tuple
>     return occurrences
> ```

RAG:
> 1. **Restatement of the Problem**: 
>    We need to create a function that takes a list of tuples and counts how many times each unique tuple appears in that list. The output should be a dictionary where the keys are the unique tuples and the values are their respective counts.
> 
> 2. **Conceptualization of the Solution**: 
>    To solve this problem, we can use a dictionary to keep track of the counts of each tuple. We will iterate through the list of tuples, and for each tuple, we will check if it is already in the dictionary. If it is, we will increment its count; if it is not, we will add it to the dictionary with a count of 1. Finally, we will return the dictionary containing the counts of each unique tuple.
> 
> 3. **Pseudocode Solution**:
>    ```
>    function check_occurences(tuples_list):
>        create an empty dictionary called counts
>        for each tuple in tuples_list:
>            if tuple is in counts:
>                increment counts[tuple] by 1
>            else:
>                set counts[tuple] to 1
>        return counts
>    ```
> 
> 4. **Final Python 3 Solution**:
> ```python
> def check_occurences(tuples_list):
>     # Create an empty dictionary to store counts
>     counts = {}
>     
>     # Iterate through each tuple in the input list
>     for tup in tuples_list:
>         # If the tuple is already in the dictionary, increment its count
>         if tup in counts:
>             counts[tup] += 1
>         # If the tuple is not in the dictionary, add it with a count of 1
>         else:
>             counts[tup] = 1
>             
>     # Return the dictionary containing counts of each unique tuple
>     return counts
> ```

CoALA:
> 1. **Restate the problem in plain English**: 
>    The task is to create a function that takes a list of tuples and counts how many times each unique tuple appears in that list. The result should be a dictionary where the keys are the unique tuples and the values are their respective counts.
> 
> 2. **Conceptualize a solution first in plain English**: 
>    To solve this problem, we can iterate through the list of tuples and maintain a count of each tuple in a dictionary. For each tuple we encounter, we will check if it is already in the dictionary. If it is, we will increment its count; if it is not, we will add it to the dictionary with a count of 1. Finally, we will return the dictionary containing the counts of all unique tuples.
> 
> 3. **Write a pseudocode solution**:
>    ```
>    function check_occurences(tuples_list):
>        create an empty dictionary called counts
>        for each tuple in tuples_list:
>            if tuple is in counts:
>                increment counts[tuple] by 1
>            else:
>                set counts[tuple] to 1
>        return counts
>    ```
> 
> 4. **Output the final Python 3 solution with your solution steps in comments**:
> ```python
> def check_occurences(tuples_list):
>     # Create an empty dictionary to store counts of each tuple
>     counts = {}
>     
>     # Iterate through each tuple in the provided list
>     for tup in tuples_list:
>         # If the tuple is already in the dictionary, increment its count
>         if tup in counts:
>             counts[tup] += 1
>         # If the tuple is not in the dictionary, add it with a count of 1
>         else:
>             counts[tup] = 1
>             
>     # Return the dictionary containing the counts of each unique tuple
>     return counts
> ```