# Pattern Recognizer
# Don't read this.
# Original OC do not steal!

from nltk.corpus import reuters

import vsa as v
from vsa.memory import CleanUpMemory, LookUpMemory, SymbolLibrary
from vsa.token import Scanner

d = 1000
t = 0.1

symbol_library = SymbolLibrary(d, t)
pattern_cleanup = CleanUpMemory(d, t)
permutation_lookup = LookUpMemory(d, t)
permutation_cleanup = CleanUpMemory(d, t)

mister_scan = Scanner(symbol_library, pattern_cleanup, permutation_lookup, permutation_cleanup)

thingie = reuters.raw()

from time import sleep

for thing in thingie:
    sleep(0.1)
    print(thing)