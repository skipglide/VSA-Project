from vector import generate_symbol,\
    similarity, array_to_bytes, \
        bytes_to_array

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
  def __init__(self, d):
    self.symbol = generate_symbol()