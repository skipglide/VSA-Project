from numpy import ones
from vector import generate_symbol, bind, array_to_tuple, tuple_to_array

def get_unicode_number(char):
  """
  Returns the unicode number from a single character.
  """
  unicode_number = ord(char)
  return unicode_number

class Scanner:
  def __init__(self, symbol_library, cleanup_memory):
    self.symbol_library = symbol_library
    self.pattern_cleanup = cleanup_memory

    self.token_window = 2
    self.symbolic_memory_length = 10
    
    self.token_memory = [ones(symbol_library.dimensionality, dtype=float16) for _ in range(self.token_window)]
    self.symbolic_memory = [ones(symbol_library.dimensionality, dtype=float16) for _ in range(self.symbolic_memory_length)]

    self.pattern_count = dict()

  def update_pattern_count(self, symbol):
    key = array_to_tuple(symbol)
    self.pattern_count[key] = pattern_counts.get(key, 0) + 1

  def update_token_memory(self, t):
    symbol = self.symbol_library.retrieve_value(t)
    self.token_memory[1] = self.token_memory[0]
    self.token_memory[0] = symbol

  def read_token(self, char):
    # FIX THAT LOGIC
    t = get_unicode_number(char)
    if self.symbol_library.already_there(t): # If it's already known, just update the memory and move.
      self.update_token_memory(t)
    else: # If it's new, add it to the symbol library and the cleanup memory too.
      self.symbol_library.add_key(t)
      symbol = self.symbol_library.retrieve_symbol(t)
      self.pattern_cleanup.add(symbol)
      self.update_token_memory(t)
    # Tokens are patterns too
    symbol = self.symbol_library.retrieve_symbol(t)
    self.update_pattern_count(symbol)

  def update_memory(self):
    for i in range(self.symbolic_memory_length):
      new_symbol # TODO: oops we need to use permutations
      self.pattern_cleanup.memory.add(new_symbol)
      self.symbolic_memory[i] = new_symbol
      self.update_pattern_count(new_symbol)
# Opps
# We forgot to incorporate a way to effiently pair symbols with the original pattern
# Gonna have to rewrite