import numpy as np
from vsa.vector import CleanUpMemory, LookUpMemory, SymbolLibrary
import vsa.vector as v
from vsa.utils import mr_timer
d = 1000

cleanup = CleanUpMemory(d)
lookup = LookUpMemory(d)
symbol_library = SymbolLibrary(d)

# Test adding converting array to bytes & back
a = v.generate_symbol(d)
b = v.generate_symbol(d)
c = v.generate_symbol(d)
a_bites = v.array_to_bytes(a)
a_array = v.bytes_to_array(a_bites)
print("Testing *_to_* function")
print(mr_timer(v.similarity(a, a_array)).output) # Should equal exactly 1.0

# Add symbol to clean up memory and recover it
cleanup.add(a)
print("Generating Noise")
for i in range(1, 9): # Add some noise
    cleanup.add(v.generate_symbol(d))
unsorted_list = cleanup.return_similarity(a)
print("Printing similarities")
for element in unsorted_list:
    print(element[0])

top_result = v.sort(unsorted_list)
print("printing top result")
print(top_result[0])

print("Testing cleanup")
print(a.shape, top_result.shape)
print(v.similarity(a, top_result[-1])) # Should equal exactly 1.0

# Create a noisy symbol and clean it up
print("Testing noisy cleanup")
noisy_symbol = v.bundle(a, v.generate_symbol(d))
print(v.similarity(a, noisy_symbol)) # Should be less than one, but greater than 0.1
unsorted_list = cleanup.return_similarity(noisy_symbol)
top_result = v.sort(unsorted_list)
print(v.similarity(a, top_result)) # Should equal exactly 1.0

# Create a permutation matrix to store a sequence
permutation_matrix = v.generate_permutation(d)
s = v.sequence(lookup, a, b, c) # Create the sequence
for i in range(1, 99): # Add some noise
    lookup.add_symbol(v.generate_permutation(d))
permutation_vector = v.sort(lookup.retrieve_value(s)) # Try to retrieve the permutation vector out of the sequence
# Now use th