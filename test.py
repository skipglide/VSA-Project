import numpy as np
from vsa.memory import CleanUpMemory, LookUpMemory, SymbolLibrary
import vsa.vector as v
from vsa.utils import TimeCalls
d = 1000

cleanup = CleanUpMemory(d, 0.1)
lookup = LookUpMemory(d, 0.1)
symbol_library = SymbolLibrary(d, 0.1)
sequences = CleanUpMemory(d, 0.1)

# Test adding converting array to bytes & back
a = v.generate_symbol(d)
b = v.generate_symbol(d)
c = v.generate_symbol(d)
a_bites = v.array_to_bytes(a)
a_array = v.bytes_to_array(a_bites)
print("Testing *_to_* function")
print(f"similarity of converted vector: {v.similarity(a, a_array)}") # Should equal exactly 1.0

# Add symbol to clean up memory and recover it
cleanup.add(a)
print("Generating Noise")
for i in range(1, 9): # Add some noise
    cleanup.add(v.generate_symbol(d))
unsorted_list = cleanup.return_similarities(a)
top_result = v.best_match(unsorted_list)

print("Testing cleanup")
print(a.shape, top_result.shape)
print(f"a simu. score to clean up retrieval: {v.similarity(a, top_result)}") # Should equal exactly 1.0

# Create a noisy symbol and clean it up
print("Testing noisy cleanup")
noisy_symbol = v.bundle(a, v.generate_symbol(d))
print(v.similarity(a, noisy_symbol)) # Should be less than one, but greater than 0.1
unsorted_list = cleanup.return_similarities(noisy_symbol)
top_result = v.best_match(unsorted_list)
print(f"a simu. score to noisy-clean up retrieval: {v.similarity(a, top_result)}") # Should equal exactly 1.0

# Test Bind operation
print("Testing noisy cleanup")
ac = v.bind(a, c)
bc = v.bind(b, c)
print(f"a simularity to b: {v.similarity(a, b)}")
print(f"ac simularity to bc: {v.similarity(ac, bc)}")
a_ = v.unbind(ac, c)
print(f"a_ simularity to a: {v.similarity(a, a_)}")

# Test threshold
# Add binded vectors that will score ~0.5 simularity
for i in range(1,3):
    _ = v.generate_symbol(d)
    _ = v.bundle(a, _)
    cleanup.add(_)
print(f"there are {len(v.threshold(cleanup.return_similarities(a), 0.1))} vectors above threshold {cleanup.threshold}")

s = v.sequence(lookup, a, b, c) # Create the sequence
sequences.add(s) # Add it to sequence clean up
for i in range(1, 99): # Add some noise
    lookup.add_symbol_for(v.generate_permutation(d))
# Now we're retreive the permutation vector for s in lookup
permutation_vector = lookup.return_simularities(s)
