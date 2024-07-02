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

for char in thingie[:9]: # Priming the memory
    mister_scan.token_memory.append(char)


for thing in thingie[:5000]:
    mister_scan.read_token(thing)

pattern_count = mister_scan.pattern_count
for key, value in sorted(pattern_count.items()[:20], key=lambda x: x[1], reverse=True): # sort by count, greatest first
    print(f"{key}: {value}")

print(f"\nThere are {len(pattern_count.items())} recorded patterns!")
