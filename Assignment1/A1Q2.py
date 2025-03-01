import sys
import math

'''
You may do "import math", and use function math.comb().
But you need to investigate the complexity of math.comb()
in order to justify the complexity of your own algorithm.
'''


def combination_index_calculation(total_elements, combination, current_position=0, previous_element=-1):
    '''
    combination_index_calculation method recursively calculates the lexicographical index of a given combination
    
    Param:
        total_elements (int) = Total number of elements in the input sets
        combination (list) = combination for which the index is calculated and sorted lexicographically
        current_position (int) = stores the current index in the combination being processed
        previous_element (int) = element in the previous step 
        
    Return:
        total_idx (int) = The number of combinations that comes before given one in lexicographical order 
    '''
    # Base Condtion: After processing all the combination elements
    if current_position == len(combination):
        return 0
    
    total_idx = 0
    current_num = combination[current_position] 
    
    # Iterate over possible elements before the current element in the combination
    for i in range(previous_element + 1, current_num):
        # stores the remaining element after choosing current_position 
        remain = len(combination) - (current_position + 1) 
        
        # add combinations starting with i followed by remaining elements to total_idx
        total_idx += math.comb(total_elements - i - 1, remain)
    
    # recursively process the next_position with the current element as previous_element for next call
    total_idx += combination_index_calculation(total_elements, combination, current_position + 1, current_num)
    
    return total_idx
    
    
def find_combination_index(total_elements, combination): 
    '''
    find_combination_index method computes the lexicographical idx of a combination of elements
    
    Param:
        total_elements (int) = Total number of elements in the input sets
        combination (list) = the combination to find the idx
        
    Returns: 
        combination_index_calculation result (int) = the lexicographical index of the combination
    '''
    if not combination:
        return 0
    
    # ensure the combination is sorted to determine the correct lexicographical idx
    sorted_combination = sorted(combination)
    return combination_index_calculation(total_elements, sorted_combination) 

def main():
    num_query = int(sys.stdin.readline())
    for _ in range(num_query):
        a = [int(s) for s in sys.stdin.readline().split()]
        n, q = a[0], a[1:] 
        print(find_combination_index(n, q))

if __name__ == "__main__":
    main()
    
    
'''
Justification of the Time Complexity of algorithm:

    1. Sorting - line 60
    According to python document, https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts
    The document says that python sort() uses the Timsort algorithm which has a time complexity of O(n log n)
    Hence:
        * It requires O(k log k)
    
    2. math.comb - line 37
    According to python document, https://github.com/python/cpython/blob/main/Modules/mathmodule.c
    The document includes math_comb_impl function    
    
    2-1. perm_comb_small in math_comb_impl method results in O(k)
        # Code snippet from math_comb_impl
            ki = Py_MIN(ki, ni - ki);
        if (ki > 1) {
            result = perm_comb_small((unsigned long long)ni,
                                     (unsigned long long)ki, 1);
            goto done;
        }
        
        # Code snippet from perm_comb_small
            unsigned long long result = n;
        for (unsigned long long i = 1; i < k;) {
                result *= --n;
                ++i;
        }
        
        => Time complexity of O(k)
        
    2-2. perm_comb in math_comb_impl method also results in O(k)
        # Code snippet from perm_comb
            unsigned long long j = k / 2;
            a = perm_comb(n, j, iscomb);
            b = perm_comb(n, k - j, iscomb);
        
        This snippet shows Divde & Conquer method
            Divide:
                C(n, k) = C(n, j) * C(n - j, k - j) / C(k, j)
                
            Recursion step:
                C(8, 4) -> C(8, 2) * C(6, 2) / C(4, 2)
                C(8, 2) -> C(8, 1) * C(7, 1) / C(2, 1)
            ...
            hence, k = 4 which means that
            
        => Time complexity of O(k)
        
    In conclusion, when recursion called by k times AND across all recursive calls, the total number of iterations for loop is at most O(n - k) in total => O(k * n)
    Sorting requires O(k log k)
    Hence, Total time complexity of this algorithm is O(k * n) + O(k log k)
'''
