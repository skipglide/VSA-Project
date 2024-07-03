# VSA-Project

Some random examples of VSA. Impliments linked lists and a pattern recognizer for raw text. If you are unfamiliar with Vector Symbolic Architecture or Hyper-Dimensional Computing, you can familiarize yourself with it [here](https://www.hd-computing.com/).

## Linked Lists

Implimenting link lists is simple. First some definitions:

### Definitions
Symbol: A symbol is a high dimensional vector which has certain properties which make it useful for symbolic computing.

Cleanup Memory: Used to clean up a noisy vector, very critical for sharing information across domains. This term gets used interchangably with the word "vector".

Lookup Memory: This takes a symbol and directly associates one with something else; this something can be another symbol or a matrix or an image of something.

Symbol Library: This is an implimentation of a hash table to take a key and retreive a symbol, it is like the inverse of Lookup Memory. This can be useful for language processing as we can use a string to see if there are any symbols associated with them.

Pointer: In this context, a pointer is a symbol that contains information that can be extracted and processed to find information connected to some other symbol.

A, Symbol 'A'

B, Symbol 'B'

L<sub>x</sub>, Symbol for Link 'x'

P<sub>x</sub>, Symbol for a pointer for 'x'

p<sub>x</sub>, Symbol for the Permutation Matrix 'x'

M<sub>x</sub>, the actual Permutation Matrix 'x', this matrix is represented by P<sub>x</sub>

C<sub>E</sub>, Cleanup Memory for Entities (Just symbols which could be for anything)

C<sub>L</sub>, Cleanup Memory for Links

C<sub>P</sub>, Cleanup Memory for Pointers

L<sub>P</sub>, Lookup Memory for Permutations


### Procedure
1. First you take your symbol A & B and add them to C<sub>E</sub>, this way we can perform a vector query with any symbols related to either A or B and retrieve the original symbols. We have our vector A which we want linked to B.

A, B

2. Now we generate a permutation symbol (p<sub>A</sub>) and the corresponding matrix (M<sub>A</sub>) for the symbol 'A'

p<sub>A</sub>, M<sub>A</sub>

3. We associate pA & M<sub>a</sub> in L<sub>P</sub>, if we have the the vector P<sub>A</sub>, we can easily lookup the corresponding matrix with a query to L<sub>P</sub>

LP

4. Now we generate the pointer to B (P<sub>B</sub>) with an inverse permutation operation:

P<sub>B</sub> = M<sub>A</sub>***-1***(B)

5. Now that we have A, p<sub>A</sub>, & P<sub>B</sub>, we can bundle these vectors together to create a link symbol for A (L<sub>A</sub>)

L<sub>A</sub> = A + p<sub>A</sub> + P<sub>B</sub>

6. Now add L<sub>A</sub> to C<sub>L</sub>
