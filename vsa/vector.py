import numpy as np

from utils import TimeCalls
# Utilities
#

def arr2tup(arr):
  """
  Converts a numpy array to a tuple.

  Args:
        arr (ndarray): 1D-Array for VSA operations.

    Returns:
        tup: Array as Tuple, is hashable.
  """
  return tuple(arr)


def tup2arr(tup):
  """
  Converts a tuple to a numpy array.

  Args:
        tup (tuple): Tuple representation of VSA symbol.

    Returns:
        arr: 1D-Array for VSA operations.
  """
  return np.array(tup).reshape(len(tup))

@TimeCalls
def array_to_bytes(arr):
  """
  Converts an array to a byte object.

  Args:
        arr (ndarray): 1D-Array for VSA operations.

    Returns:
        bites: Byte representaion of array.
  """
  return arr.tobytes()

@TimeCalls
def bytes_to_array(bites):
  """
  Converts a byte object to a 1D ndarray.

  Args:
    bites: Byte representaion of array.

  Returns:
    arr (ndarray): 1D-Array for VSA operations.
  """
  array = np.frombuffer(bites, dtype=np.float64)
  return array

@TimeCalls
def threshold(unsorted_list: list, threshold: float):
  """
  Filters a list based off of a threshold value.

  Args:
    unsorted_list: a list of paired values, it filters based off a threshold value for the first of the pair

  Returns:
    filtered_list (list): a list of paired values, all of them exceed the threshold criteria
  """
  filtered_list = [_ for _ in unsorted_list if _[0] >= threshold]
  return filtered_list

def best_match(unsorted_list: list):
  """
  Returns the best match from an unsorted list of similarity/symbol pairs.

  Args:
    unsorted_list: a list of paired values, it filters based off a threshold value for the first entry of the pair.

  Returns:
    symbol (ndarray): The symbol with the highest simularity score.
  """
  sorted = sort(unsorted_list)
  symbol = sorted[0][-1]
  return symbol

@TimeCalls
def sort(unsorted_list: list):
  """
  Sorts a list of pairs of values based off of a simularity score in the first entry of each pair.

  Args:
    unsorted_list: a list of paired values, it filters based off a threshold value for the first entry of the pair.

  Returns:
    sorted_list (list): a list of paired values, all of them exceed the threshold criteria
  """
  sorted_list = sorted(unsorted_list, key=lambda x: x[0])
  return sorted_list

# Basic Operations
#
@TimeCalls
def generate_symbol(dimensionality: int):
  symbol = np.random.uniform(low=-1.0, high=1.0, size=(1, dimensionality))
  return symbol.reshape(dimensionality)

@TimeCalls
def similarity(a,b):
    assert a.shape[-1] == b.shape[-1], "VSA Dimension must match: " + str(a.shape) + " " + str(b.shape)
    #multiply values by pi to move from (-1, 1) to (-π, π)
    pi = np.pi
    a = np.multiply(a, pi)
    b = np.multiply(b, pi)
    #calculate the mean cosine similarity between the vectors
    similarity = np.mean(np.cos(a - b), axis=0) # Get rid of axis?
    return similarity

# Bundling Operation
#

def bundle(*symbols):
    symbols = np.stack(symbols, axis=0)
    #convert each angle to a complex number
    pi = np.pi
    j = np.array([0+1j])

    #sum the complex numbers to find the bundled vector
    cmpx = np.exp(pi * j * symbols)
    bundle = np.sum(cmpx, axis=0)
    #convert the complex sum back to an angle
    bundle = np.angle(bundle) / pi
    bundle = np.reshape(bundle, (1, -1))

    return bundle

# Binding Operations
#

def remap_phase(x):
    x = np.mod(x, 2.0)
    x = -2.0 * np.greater(x, 1.0) + x

    return x

def bind(*symbols):
    #stack the vararg inputs into an array
    symbols = np.stack(symbols)
    #sum the angles
    symbol = np.sum(symbols, axis=0)
    #remap the angles to (-1, 1)
    symbol = remap_phase(symbol)
    #reshape the output to maintain 2D array
    symbol = np.reshape(symbol, (1, -1))

    return symbol

def unbind(x, *symbols):
    #stack and sum the symbols to be unbound
    symbols = np.stack(symbols, axis=0)
    symbols = np.sum(symbols, axis=0)

    #remove them from the input & remap phase
    symbol = np.subtract(x, symbols)
    symbol = remap_phase(symbol)

    return symbol


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