from numpy.random import randint

import jax.numpy as jnp
from jax import device_put, random, jit

def generate_symbol(number: int, dimensionality: int):
  return random.uniform(generate_key(), minval=-1.0, maxval=1.0, shape=(number, dimensionality))

def generate_key():
  seed = randint(0, 2**32)
  return random.PRNGKey(seed)

def jax_array_to_tuple(arr):
    return tuple(arr)

def tuple_to_jax_array(tup):
    return jnp.array(tup, dtype=jnp.float32)

@jit
def similarity(a,b):
    assert a.shape[-1] == b.shape[-1], "VSA Dimension must match: " + str(a.shape) + " " + str(b.shape)
    #multiply values by pi to move from (-1, 1) to (-π, π)
    pi = jnp.pi
    a = jnp.multiply(a, pi)
    b = jnp.multiply(b, pi)
    #calculate the mean cosine similarity between the vectors
    similarity = jnp.mean(jnp.cos(a - b), axis=1)
    return similarity

class LookUpMemory:
  def __init__(self):
    self.memory = dict()
    self.dimensionality = d

  def add_association(self, x, a):
    # device_put turns a JAX array into a hashable type so the dictionary can use it as a key value
    self.memory[x] = a
  
  def return_simularity(self, x):
    # This is a naive implimentation until I incorporate annoy
    result = []
    for association in self.memory:
      a = tuple_to_jax_array(association[0])
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
  
  def add(self, x):
    # device_put turns a JAX array into a hashable type so the dictionary can use it as a key value
    self.memory.add(x)
  
  def check_memory(self, x):
    """
    Check if x is already in clean up memory.
    """
    if jax_array_to_tuple(x) in self.memory:
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