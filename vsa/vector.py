import jax.numpy as jnp
from jax import jit
from jax import random

def generate_symbol(key, number: int, dimensionality: int):
  return random.uniform(key, minval=-1.0, maxval=1.0, shape=(number, dimensionality))

def generate_key(seed):
    return random.PRNGKey(seed)

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