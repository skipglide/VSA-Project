import numpy as np
from numpy import ndarray

from .memory import CleanUpMemory, LookUpMemory, SymbolLibrary
from .utils import TimeCalls


# Sequence Operations
# 

def generate_permutation(n):
    # Create an identity matrix
    identity = np.eye(n)
    
    # Generate random permutation indices
    perm = np.random.permutation(n)
    
    # Use the permutation to shuffle the rows of the identity matrix
    return identity[perm]


def permute_forward(x, P):
  return np.dot(x, P)


def permute_inverse(x, P):
  return np.dot(x, P.T)

@TimeCalls
def sequence(lookup, *symbols):
  s = symbols[0]
  P = generate_permutation(lookup.dimensionality)
  for symbol in symbols[1:]:
    s = permute_forward(s, P) + symbol
  symbol = lookup.add_symbol_for(P)
  s += symbol
  return s

@TimeCalls
def desequence(s, cleanup, lookup):
  # TODO: finish this function
  symbols = list()
  similarity = lookup.return_similarity(s)
  while similarity > 0.1:
    recovery = cleanup.cleanup(s)
    symbols.append(recovery)

# Linked Lists
#
@TimeCalls
def link(a: ndarray, b: ndarray, entries: CleanUpMemory, permutations: LookUpMemory, pointers: CleanUpMemory):
  # Add a & b to entries if not already present
  entries.add(a, b)
  # Create a permutation matrix with a symbol to represent it
  P = generate_permutation
  p = permutations.add_symbol_for(P)
  # Generate the pointer using the permutation matrix & a symbol
  pointer = permute_inverse(b, P)
  pointers.add(pointer)
  # Create the link vector that contains a symbol, a permutation matric symbol, and the pointer.
  l = bundle(a, p, pointer)
  return l


def find_link(a: ndarray, links: CleanUpMemory, entries: CleanUpMemory, permutations: LookUpMemory, pointers: CleanUpMemory):
  link = links.clean_up(a)