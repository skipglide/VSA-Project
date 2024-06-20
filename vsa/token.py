from numpy import ones
from vector import bind

def get_unicode_number(char):
  """
  Returns the unicode number from a single character.
  """
  unicode_number = ord(char)
  return unicode_number

class Scanner:
  def __init__(self, symbol_library):
    self.symbol_library = symbol_library

    self.token_window = 2
    self.symbolic_memory_length = 10
    
    self.token_memory = [ones(symbol_library.dimensionality, dtype=float16) for _ in range(self.token_window)]
    self.symbolic_memory = [ones(symbol_library.dimensionality, dtype=float16) for _ in range(self.symbolic_memory_length)]
  
  def update_token_memory(self, t):
    symbol = self.symbol_library.retrieve_value(t)
    self.token_memory[1] = self.token_memory[0]
    self.token_memory[0] = symbol

  def read_token(self, char):
    # FIX THAT LOGIC
    t = get_unicode_number(char)
    if self.symbol_library.already_there(t):
      self.update_token_memory(t)
    else:
      self.symbol_library.add_key(t)
      self.update_token_memory(t)

  def update_memory(self):
    for i in range(self.symbolic_memory_length):
      new_symbol = bind(self.token_memory[0], )
