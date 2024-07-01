from numpy import ndarray

from .vector import generate_symbol,\
  similarity, array_to_bytes, \
  bytes_to_array, sort, threshold, \
  best_match

# Memory Classes
#

class Memory:
  def __init__(self, d: int, t: float):
    """
    A class for performing recall operations.

    Args:
      d (int): The dimensionality of the symbols.
      t (float): The threshold for performing cleanup operations.
    """
    self.dimensionality = d
    self.threshold = t
  

class CleanUpMemory(Memory):
  def __init__(self, d: int, t: int):
    super().__init__(d, t)
    self.memory = set()

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
    """
    Returns the symbol with the highest similarity score to the symbol 'x'.

    Args:
      x (ndarray): A symbol.

    Returns:
      symbol: A symbol with the highest similarity score.    
    """
    unsorted_list = self.return_similarities(x)
    return best_match(unsorted_list)

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

  def return_similarities(self, x):
    """
    Generates an unsorted list of pairs of simularity-scores/symbols
    """
    result = []
    for symbol in self.memory:
      a = bytes_to_array(symbol)
      result.append((similarity(x, a), a))
    return result


class SymbolLibrary(Memory):
  """
  A library that takes a valid key and returns a symbol
  """
  def __init__(self, d: int, t: int):
    super().__init__(d, t)
    self.library = dict()

  def already_there(self, x):
    if x in self.library.keys():
      return True
    else:
      return False

  def add_key(self, key):
    self.library[key] = generate_symbol(self.dimensionality)

  def retrieve_symbol(self, key):
    return self.library[key]


class LookUpMemory(Memory):
  def __init__(self, d: int, t: int):
    super().__init__(d, t)
    self.memory = dict()

  def add_symbol_for(self, a):
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

  def return_similarities(self, x):
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