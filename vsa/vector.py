import numpy as np

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


def array_to_bytes(arr):
  """
  Converts an array to a byte object.

  Args:
        arr (ndarray): 1D-Array for VSA operations.

    Returns:
        bites: Byte representaion of array.
  """
  return arr.tobytes()


def bytes_to_array(bites):
    array = np.frombuffer(bites, dtype=np.float64)
    return array


def threshold(unsorted_list: list, threshold: float):
  filtered_list = [_[0] for _ in unsorted_list if _[0] >= threshold]

def sort(unsorted_list):
  sorted_list = sorted(unsorted_list, key=lambda x: x[0])
  return sorted_list[0][-1]

# Basic Operations
#

def generate_symbol(dimensionality: int):
  symbol = np.random.uniform(low=-1.0, high=1.0, size=(1, dimensionality))
  return symbol.reshape(dimensionality)

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


def sequence(lookup, *symbols):
  s = symbols[0]
  P = generate_permutation(lookup.dimensionality)
  for symbol in symbols[1:]:
    s = permute_forward(s, P) + symbol
  symbol = lookup.add_symbol(P)
  s += symbol
  return s


def desequence(s, cleanup, lookup):
  # TODO: finish this function
  symbols = list()
  similarity = lookup.return_similarity(s)
  while similarity > 0.1:
    recovery = cleanup.cleanup(s)
    symbols.append(recovery)

# Linked Lists
#

def link(a: ndarray, b: ndarray, entries: CleanUpMemory, permutations: LookUpMemory, pointers: CleanUpMemory):
  # Add a & b to entries if not already present
  entries.add(a, b)
  # Create a permutation matrix with a symbol to represent it
  P = generate_permutation
  p = permutations.add_symbol(P)
  # Generate the pointer using the permutation matrix & a symbol
  pointer = permute_inverse(b, P)
  pointers.add(pointer)
  # Create the link vector that contains a symbol, a permutation matric symbol, and the pointer.
  l = bundle(a, p, pointer)
  return l


def find_link(a: ndarray, links: CleanUpMemory, entries: CleanUpMemory, permutations: LookUpMemory, pointers: CleanUpMemory):
  link = links.clean_up(a)


# Memory Classes
#

class SymbolLibrary:
  def __init__(self, d):
    self.library = dict()
    self.dimensionality = d
  
  def already_there(self, x):
    if x in self.memory.keys():
      return True
    else:
      return False
  
  def add_key(self, key):
    self.memory[key] = generate_symbol(self.dimensionality)
  
  def retrieve_symbol(self, key):
    return self.memory[key]

class LookUpMemory:
  def __init__(self, d):
    self.memory = dict()
    self.dimensionality = d

  def add_symbol(self, a):
    '''
    Takes thing 'a' and generates a symbol to return
    '''
    x = generate_symbol(self.dimensionality)
    self.memory[array_to_bytes(x)] = a
    return x

  def add_association(self, x, a):
    """
    Takes a symbol 'x' and uses it as key for retreiving 'a'
    """

    self.memory[array_to_bytes(x)] = a
  
  def return_similarity(self, x):
    """
    Takes the symbol 'x' and returns a list of
    """
    # This is a naive implimentation until I incorporate annoy
    result = []
    for association in self.memory:
      a = bytes_to_array(association)
      result.append((similarity(x, a), a))
    return result
  
  def retrieve_value(self, x):
      try:
          return self.memory[array_to_bytes(x)]
      except KeyError:
          print("No value")
          return None

class CleanUpMemory:
  def __init__(self, d):
    self.memory = set()
    self.dimensionality = d
  
  def add(self, *args):
    for x in args:
      self.memory.add(array_to_bytes(x))
  
  def check_memory(self, x):
    """
    Check if x is already in clean up memory.
    """
    if array_to_bytes(x) in self.memory:
      return True
    else:
      return False
  
  def clean_up(self, x):
    unsorted_list = self.return_similarity(x)
    sorted_list = sorted(unsorted_list, key=lambda x: x[0])
    return sorted_list[0][-1]

  def return_threshold(self, x: ndarray, threshold: float):
    """
    Returns a list of symbols who's simularities exceed a certain threshold.
    Args:
        x (ndarray): A symbol.
        t (float): A simularity threshold, should be between 0 and 1.

    Returns:
        list: A list of the results in no particular order
    """
    simularities = return_simularities(x)
    thresholds = threshold(x, threshold)
    # TODO: Finish this


  def return_simularities(self, x):
    # This is a naive implimentation until I incorporate annoy
    result = []
    for symbol in self.memory:
      a = bytes_to_array(symbol)
      result.append((similarity(x, a), a))
    return result

# Custom Data Types
#

class FHRR:
  """
  Fourier Holographic Reduced Representation
  """
  def __init__(self):
    self.symbol = generate_symbol()