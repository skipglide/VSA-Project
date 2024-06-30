from vsa.memory import LookUpMemory, CleanUpMemory
from vsa.vector import generate_symbol, similarity, bundle, sort, best_match
from vsa.connect import permute_forward, permute_inverse, generate_permutation

d = 1000
t = 0.1

entries = CleanUpMemory(d, t)
permutations = LookUpMemory(d, t)
pointers = CleanUpMemory(d, t)
links = CleanUpMemory(d, t)

# Create two symbols we want to associate
a = generate_symbol(d)
b = generate_symbol(d)
entries.add(a, b)

# Create a permutation matrix with a symbol to represent it
P_a = generate_permutation(d) # The matrix
p_a = permutations.add_symbol_for(P_a) # The matrix's symbol

# Generate the pointer using the permutation matrix & a symbol
pointer_ab = permute_inverse(b, P_a)
pointers.add(pointer_ab)

# Create the link vector that contains a symbol, a permutation matric symbol, and the pointer.
l_a = bundle(a, p_a, pointer_ab)
links.add(l_a)

# Adding Random Noise
for i in range(1, 1):
  entries.add(generate_symbol(d))
  permutations.add_association(generate_symbol(d), generate_permutation(d))
  pointers.add(generate_symbol(d))
  links.add(generate_symbol(d))

# Recover B
# With a, obtain link vector that contains information to point to other symbol
link = links.clean_up(a)
# Now get the permutation symbol
reconstructed_permutation_symbols = permutations.return_similarities(link)
reconstructed_permutation_symbol = best_match(reconstructed_permutation_symbols)
# Get the permutation matrix
permutation_matrix = permutations.retrieve_value(reconstructed_permutation_symbol)
# Apply a permutation operation to retrieve the linked value B
noisy_vector = permute_forward(link, permutation_matrix)
# Clean up the noise from our permute operation
resultant_vector = entries.clean_up(noisy_vector)
# Check the simularity of this resultant vector with our original symbol 'b'.
print(similarity(b, resultant_vector))