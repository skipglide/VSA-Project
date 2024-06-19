from vsa.vector import LookUpMemory, CleanUpMemory, permute_forward, permute_inverse, generate_permutation, generate_symbol, generate_key, similarity

d = 100

entries = CleanUpMemory(d)
permutations = LookUpMemory(d)
pointers = CleanUpMemory(d)
links = CleanUpMemory(d)

# Create two symbols we want to associate
a = generate_symbol(d)
b = generate_symbol(d)
entries.add(a, b)

# Create a permutation matrix with a symbol to represent it
P_a = generate_permutation(d)
p_a = permutations.add(p)

# Generate the pointer using the permutation matrix & a symbol
pointer_ab = permute_inverse(b, P_a)
pointers.add(pointer_ab)

# Create the link vector that contains a symbol, a permutation matric symbol, and the pointer.
l_a = bundle(a, p_a, pointer_ab)
links.add(l_a)

# Adding Random Noise
for i in range(1, 99):
  entries.add(generate_symbol(d))
  permutations.add_association(generate_symbol(d), generate_permutation(d))
  pointers.add(generate_symbol(d))
  links.add(generate_symbol(d))

# Recover B
# With a, obtain link vector that contains information to point to other symbol
link = links.clean(a)[0]
# Get the permutation matrix
permutation_matrix = retrieve_value(link)
# Apply a permutation operation to retrieve the linked value B
noisy_vector = permute_forward(link, permutation_matrix)
# Clean up the noise from our permute operation
resultant_vector = entries.clean(noisy_vector)[0]
# Check the simularity of this resultant vector with our original symbol 'b'.
print(simularity(b, resultant_vector))