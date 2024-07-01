from numpy import ones, float16
from .vector import generate_symbol
from .connect import generate_permutation, \
  permute_forward, permute_inverse
def get_unicode_number(char):
  """
  Returns the unicode number from a single character.
  """
  unicode_number = ord(char)
  return unicode_number

class Scanner:
  # First you instanciate Scanner
  # Then you feed it individual characters with read_token
  def __init__(self, symbol_library, cleanup_memory, lookup_memory, perm_cleanup):
    self.symbol_library = symbol_library
    self.pattern_cleanup = cleanup_memory
    self.permutation_lookup = lookup_memory
    self.permutation_cleanup = perm_cleanup
    self.dimensionality = symbol_library.dimensionality
    # TODO: add check that all these memories are the same dimensionality

    self.token_window = 10 # length of token list
    self.token_memory = [] # contains 
    self.symbol_memory = [ones(symbol_library.dimensionality, dtype=float16) for _ in range(self.token_window)]

    self.pattern_count = dict()

  def store_permutation(self, perm):
    p = generate_symbol(self.dimensionality)
    self.permutation_lookup.add_association(p, perm)
    return p

  def array_to_sequence(self, arr):
    perm = generate_permutation(self.dimensionality)
    s = arr[0] # The begining of the sequence
    for symbol in arr[1:-1]: # Leave out the first element
      s = bundle(permute_forward(s, perm), symbol)
    p = store_permutation
    self.perm_cleanup.add(p)
    s += p
    return s

  def update_pattern_count(self, string):
    self.pattern_count[string] = self.pattern_count.get(string, 0) + 1

  def update_token_memory(self, symbol):
    self.token_memory.insert(0, symbol) # First in line
    self.token_memory.pop(-1) # Get rid of last entry

  def read_token(self, char):
    t = get_unicode_number(char)
    if self.symbol_library.already_there(t): # If it's already known, just update the memory and move.
      self.update_token_memory
    else: # If it's new, add it to the symbol library and the cleanup memory too.
      self.symbol_library.add_key(t)
      symbol = self.symbol_library.retrieve_symbol(t)
      self.pattern_cleanup.add(symbol)
      self.update_token_memory(t)
    # I guess we just update the memory?
    self.update_memory()
    pass

  def get_symbol_with_char(self, char):
    return self.symbol_library.retrieve_symbol(get_unicode_number(char))

  def update_memory(self):
    # You can assume that any unicode number has a corresponding symbol in 
    for i in range(self.token_window - 1):
      char_list = self.token_memory[0:i]
      # Okay, now it needs to take that list of char and encode them into symbols
      symbols = [self.get_symbol_with_char(char) for char in char_list]
      # Okay, now that you have those symbols, now you need to turn them into a permutation sequence
      sequence_symbol = array_to_sequence(symbols)
      # Cool, with that permutation sequence, we can now record its occurance in the update_pattern_count
      string = ''.join(char_list)
      self.update_pattern_count(string)
      # Uhhh, okay I think that's it?

  def save_model(self):
    pass

  def load_model(self):
    pass
