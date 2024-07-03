# VSA-Project

Some random examples of VSA. Impliments linked lists and a pattern recognizer for raw text. If you are unfamiliar with Vector Symbolic Architecture or Hyper-Dimensional Computing, you can familiarize yourself with it [here](https://www.hd-computing.com/).

## Linked Lists

Implimenting link lists is simple. First some definitions:

### Definitions
Symbol: A symbol is a high dimensional vector which has certain properties which make it useful for symbolic computing.
Cleanup Memory: Used to clean up a noisy vector, very critical for sharing information across domains.
Lookup Memory: This takes a symbol and directly associates one with something else; this something can be another symbol or a matrix or an image of something
Symbol Library: This is an implimentation of a hash table to take a key and retreive a symbol, it is like the inverse of Lookup Memory. This can be useful for language processing as we can use a string to see if there are any symbols associated with them.
Pointer: In this context, a pointer is a symbol that contains information that can be extracted and processed to find information connected to some other symbol.

A, Symbol 'A'
B, Symbol 'B'
L~x~, Symbol for Link 'x'
P~x~, Symbol for the Permutation Matrix 'x'
M~x~, the actual Permutation Matrix 'x', this matrix is represented by P~x~
C~E~, Cleanup Memory for Entities (Just symbols which could be for anything)
C~L~, Cleanup Memory for Links
C~P~, Cleanup Memory for Pointers
L~P~, Lookup Memory for Permutations

