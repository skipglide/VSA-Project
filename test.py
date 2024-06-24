import numpy as np
from vsa import CleanUpMemory, LookUpMemory, SymbolLibrary
import vsa as v

d = 1000

cleanup = CleanUpMemory(dimensionality)
lookup = LookUpMemory(dimensionality)
symbol_library = SymbolLibrary(dimensionality)

# Test adding converting array to bytes & back
a = v.generate_symbol(d)
b = v.generate_symbol(d)
c = v.generate_symbol(d)
a_bites = v.array_to_bytes(a)
a_array = v.bytes_to_array(a_bites)
print(v.similarity(a, a_array)) # Should equal exactly 1.0

# Add symbol to clean up memory and recover it
cleanup.add(a)
for i in range(1, 99): # Add some noise
    cleanup.add(v.generate_symbol(d))
unsorted_list = cleanup.return_similarity(a)
top_result = v.sort(unsorted_list)
print(v.similarity(a, top_result)) # Should equal exactly 1.0

# Create a noisy symbol and clean it up
noisy_symbol = v.bundle(a, v.generate_symbol(d))
print(v.similarity(a, noisy_symbol)) # Should be less than one, but greater than 0.1
unsorted_list = cleanup.return_similarity(noisy_symbol)
top_result = v.sort(unsorted_list)
print(v.similarity(a, top_result)) # Should equal exactly 1.0

# Create a permutation matrix to store a sequence
permutation_matrix = v.generate_permutation(d)
s = v.sequence(lookup, a, b, c) # Create the sequence
for i in range(1, 99): # Add some noise
    lookup.add(v.generate_permutation(d))
permutation_vector = v.sort(lookup.retrieve_value(s)) # Try to retrieve the permutation vector out of the sequence
# Now use th