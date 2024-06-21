import numpy as np

def link(a, b):
  pass

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

def sequence(a, b):
  

def permute_forward(x, p):
  return np.dot(p, x)

def permute_inverse(x, p):
  return np.dot(p.T, x)

def generate_permutation(n):
    # Create an identity matrix
    identity = np.eye(n)
    
    # Generate random permutation indices
    perm = np.random.permutation(generate_key(), n)
    
    # Use the permutation to shuffle the rows of the identity matrix
    return identity[perm]

def generate_symbol(dimensionality: int):
  return np.random.uniform(minval=-1.0, maxval=1.0, shape=(1, dimensionality))

def array_to_tuple(arr):
    return tuple(arr)

def tuple_to_array(tup):
    return np.array(tup, dtype=np.float32)

def similarity(a,b):
    assert a.shape[-1] == b.shape[-1], "VSA Dimension must match: " + str(a.shape) + " " + str(b.shape)
    #multiply values by pi to move from (-1, 1) to (-π, π)
    pi = np.pi
    a = jnp.multiply(a, pi)
    b = jnp.multiply(b, pi)
    #calculate the mean cosine similarity between the vectors
    similarity = np.mean(np.cos(a - b), axis=1)
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
    x = generate_symbol(self.dimensionality)
    self.memory[array_to_tuple(x)] = a
    return x

  def add_association(self, x, a):
    self.memory[x] = a
  
  def return_simularity(self, x):
    # This is a naive implimentation until I incorporate annoy
    result = []
    for association in self.memory:
      a = tuple_to_array(association[0])
      result.append((simularity(x, a), a))
    return result
  
  def retrieve_value(self, x):
      try:
          return self.memory[x]
      except KeyError:
          print("No value")
          return None

class CleanUpMemory:
  def __init__(self, d):
    self.memory = set()
    self.dimensionality = d
  
  def add(self, *args):
    for x in args:
      self.memory.add(array_to_tuple(x))
  
  def check_memory(self, x):
    """
    Check if x is already in clean up memory.
    """
    if array_to_tuple(x) in self.memory:
      return True
    else:
      return False
  
  def clean_up(self, x):
    list = self.return_simularity(x)
    sorted_list = sorted(list, key=lambda x: x[0])
    return sorted_list[0][-1]

  def return_simularity(self, x):
    # This is a naive implimentation until I incorporate annoy
    result = []
    for symbol in self.memory:
      a = tuple_to_jax_array(symbol)
      result.append((simularity(x, a), a))
    return result

class FHRR:
  """
  Fourier Holographic Reduced Representation
  """
  def __init__(self):
    self.symbol = generate_symbol()