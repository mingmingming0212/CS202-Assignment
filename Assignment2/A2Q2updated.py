import sys

def LCVS(A, B):
    '''
    This algorithm finds the length of the longest common V shaped subsequence between two integer sequences A and B

    For this assignment, V-shaped subsequence consists of two parts:
        - A strictly decreasing subsequence from the left to a pivot
        - A strictly increasing subsequence from the pivot to the right
      The pivot element is common to both parts and should be included in both

    Parameters:
        A (list of str): Input for A and it will be converted into a list of integers
        B (list of str): Input for B and it will be converted into a list of integers

    Returns:
        int: Return the length of the longest common V-shaped subsequence that appears in both A and B

    Notes:
        - The function uses DP table to calculate:
            1. lds (Longest Decreasing Subsequence) ending at each index of A using elements from B.
            2. lis (Longest Increasing Subsequence) starting at each index of A using elements from B.
        - The final result is the maximum value of (LDS[i] + LIS[i] - 1) across all i,
          For return value I ensure that at least 3 elements are present in the V as it is necessary to form V shaped subsequence.
        - The final time complexity of this algorithm is O(n * m), where n = len(B), m = len(A).
    '''
    
    A = list(map(int, A))
    B = list(map(int, B))
    
    # Map each element in A to all its occurrence indices
    a_positions = {}
    for i, val in enumerate(A):  # i is index and val is element 
        if val not in a_positions:
            a_positions[val] = []
        a_positions[val].append(i)
    
    # Initialize arrays for decreasing and increasing subsequence lengths
    lds = [0] * len(A)  # Longest Decreasing Subsequence ending at position i
    lis = [0] * len(A)  # Longest Increasing Subsequence starting at position i

    # Calculate LDS using elements in B
    for element in B:
        if element in a_positions:
            for i in a_positions[element]:
                lds[i] = 1 
                for j in range(i):
                    if A[j] > element:
                        lds[i] = max(lds[i], lds[j] + 1)
    
    # Calculate LIS using elements in reversed B
    for element in reversed(B):
        if element in a_positions:
            for i in a_positions[element]:
                lis[i] = 1  
                for j in range(i + 1, len(A)):
                    if A[j] > element:
                        lis[i] = max(lis[i], lis[j] + 1)
    
    # Combine LDS and LIS to find the longest V-shaped subsequence
    max_length = 0
    for i in range(len(A)):
        if lds[i] >= 1 and lis[i] >= 1:
            current_length = lds[i] + lis[i] - 1  # Subtract 1 to avoid double-counting the middle element
            if current_length >= 3:  # Valid V-shape must have at least 3 elements
                max_length = max(max_length, current_length)
    
    return max_length

# Entry point
num_pairs = int(sys.stdin.readline())
for _ in range(num_pairs):
    A = sys.stdin.readline().split()
    B = sys.stdin.readline().split()
    print(LCVS(A, B))


'''
Justification of the Time Complexity of the LCVS Algorithm:
    - m = len(A)  (length of sequence A)
    - n = len(B)  (length of sequence B)

1. Building a_positions map:
    - Iterates through all elements in A once.
    - Time complexity: O(m)

2. First Loop (for LDS calculation):
    - Outer loop runs for each element in B -> O(n)
    - For each B element found in A, we iterate through indices of A -> worst case O(m)
    - Inner loop over j from 0 to i (on average O(m))
    - Total worst-case complexity for LDS part: O(n * m)

3. Second Loop (for LIS calculation):
    - Symmetric to LDS loop, just reversed -> also O(n * m)

4. Final loop to combine LDS and LIS:
    - Iterates over A once -> O(m)

Total Time Complexity:
    = 1 + 2 + 3 + 4
    = O(m) + O(2nm) + O(m)
    = O(2nm + 2m)
    = O(n * m)

Therefore, the overall worst-case time complexity is:
    = O(n * m)
'''