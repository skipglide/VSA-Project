from vsa.vector import CleanUpMemory, permute_forward, permute_inverse, generate_permutation, generate_symbol, generate_key, simularity

d = 1000

entries = CleanUpMemory(d)
permutations = CleanUpMemory(d)
links = CleanUpMemory(d)

a = generate_symbol(1, d)
b = generate_symbol(1, d)
p = generate_permutation(d)