from jax.numpy import ones

def get_unicode_number(char):
  """
  Returns the unicode number from a single character.
  """
  unicode_number = ord(char)
  return unicode_number

class Scanner:
  def __init__(self, symbol_library):
    self.symbolic_memory_length = 20
    self.symbol_library = symbol_library
    self.token_memory = [ones(symbol_library.dimensionality, dtype=float16) for _ in range(2)]
    self.symbolic_memory = []

  def read_token(self, char):
    t = get_unicode_number(char)
    if self.symbol_library.already_there(t):
      symbol = self.symbol_library.retrieve_value(t)
      self.token_memory.pop[0]
      self.token_memory.extend(symbol)
      return symbol
    else:
      self.symbol_library.add_key(t)

  def update_memory(self, t):
    self.token_memory[0] = (,)