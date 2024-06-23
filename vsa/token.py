from numpy import ones
from vector import generate_symbol, bind, array_to_tuple,\
   tuple_to_array, permute_forward, generate_permutation

def get_unicode_number(char):
  """
  Returns the unicode number from a single character.
  """
  unicode_number = ord(char)
  return unicode_number

class Scanner:
  def __init__(self, symbol_library, cleanup_memory, lookup_memory, perm_cleanup):
    self.symbol_library = symbol_library
    self.pattern_cleanup = cleanup_memory
    self.permutation_lookup = lookup_memory
    self.permutation_cleanup = perm_cleanup
    self.dimensionality = symbol_library.dimensionality
    # TODO: add check that all these memories are the same dimensionality

    self.token_window = 10
    self.token_memory = []
    self.symbol_memory = [ones(symbol_library.dimensionality, dtype=float16) for _ in range(self.token_window)]

    self.pattern_count = dict()

  def store_permutation(self, perm):
    p = generate_symbol(self.dimensionality)
    self.permutation_lookup.add_association(p, perm)
    return p

  def array_to_sequence(arr):
    perm = generate_permutation(self.dimensionality)
    s = arr[0] # The begining of the sequence
    for symbol in arr[1:-1]: # Leave out the first element
      s = bundle(permute_forward(s, perm), symbol)
    p = store_permutation
    self.perm_cleanup.add(p)
    s += p
    return s

  def update_pattern_count(self, symbol):
    key = array_to_tuple(symbol)
    self.pattern_count[key] = pattern_counts.get(key, 0) + 1

  def update_token_memory(self, symbol):
    self.token_memory.insert(symbol)
    self.token_memory.pop(-1)

  def read_token(self, char):
    t = get_unicode_number(char)
    if self.symbol_library.already_there(t): # If it's already known, just update the memory and move.
      self.update_token_memory
    else: # If it's new, add it to the symbol library and the cleanup memory too.
      self.symbol_library.add_key(t)
      symbol = self.symbol_library.retrieve_symbol(t)
      self.pattern_cleanup.add(symbol)
      self.update_token_memory(t)
    # Tokens are patterns too
    symbol = self.symbol_library.retrieve_symbol(t)
    self.update_pattern_count(symbol)

  def update_memory(self):
    for i in range(self.token_window - 1):
      strings = self.token_memory[0:i]
      # Okay, now it needs to take that list of char and encode them into symbols
      # Okay, now that you have those symbols, now you need to turn them into a permutation sequence 
      # Cool, with that permutation sequence, we can now record its occurance in the update_pattern_count
      # Uhhh, okay I think that's it?
# Opps
# We forgot to incorporate a way to effiently pair symbols with the original pattern
# Gonna have to rewrite