import numpy as np

def link(a, b):
  pass

def sort(unsorted_list):
  sorted_list = sorted(unsorted_list, key=lambda x: x[0])
  return sorted_list[0][-1]

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

def sequence(lookup, *symbols):
  s = symbols[0]
  P = generate_permutation(lookup.dimensionality)
  for symbol in symbols[1:]:
    s = permute_forward(s, P) + symbol
  symbol = lookup.add_symbol(P)
  s += symbol
  return s

def desequence(s, cleanup, lookup):
  symbols = list()
  similarity = lookup.return_similarity()
  while similarity > 0.1:
    recovery = cleanup.cleanup(s)
    symbols.append(recovery)

def permute_forward(x, P):
  return np.dot(x, P)

def permute_inverse(x, P):
  return np.dot(x, P.T)

def generate_permutation(n):
    # Create an identity matrix
    identity = np.eye(n)
    
    # Generate random permutation indices
    perm = np.random.permutation(n)
    
    # Use the permutation to shuffle the rows of the identity matrix
    return identity[perm]

def generate_symbol(dimensionality: int):
  symbol = np.random.uniform(low=-1.0, high=1.0, size=(1, dimensionality))
  return symbol

def array_to_bytes(arr):
    return arr.tobytes()

def bytes_to_array(bites):
    array = np.frombuffer(bites, dtype=np.float64)
    return array

def similarity(a,b):
    assert a.shape[-1] == b.shape[-1], "VSA Dimension must match: " + str(a.shape) + " " + str(b.shape)
    #multiply values by pi to move from (-1, 1) to (-π, π)
    pi = np.pi
    a = np.multiply(a, pi)
    b = np.multiply(b, pi)
    #calculate the mean cosine similarity between the vectors
    similarity = np.mean(np.cos(a - b), axis=1) # Get rid of axis?
    return similarity

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

  def return_similarity(self, x):
    # This is a naive implimentation until I incorporate annoy
    result = []
    for symbol in self.memory:
      a = bytes_to_array(symbol)
      result.append((similarity(x, a), a))
    return result

class FHRR:
  """
  Fourier Holographic Reduced Representation
  """
  def __init__(self):
    self.symbol = generate_symbol()