
Search CLI for Zendesk 

# Requirements
1. python3 or above

# Installation
1. Clone this repo
2. `cd` into the directory
3. `pip install -r requirements.txt`

# Usage
Running search:
`python3 zensearch/search.py`

Running tests:
`python3 tests/run_tests.py`

---

# Search Tree Implementation
This search solution utilises a dictionary based Trie data structure.
A Trie data structure is a search tree which is built by inserting words of the search text character by character. As more words are added, the prefixes begin to overlap, for example adding BAN and BANANA. We denoting the end of each word with a terminal character such as `$: B-A-N-$`. We can then traverse the tree from `B -> A -> N`, and at `N` we check if it has child node `$`, if it does then we know BAN is in the search text. 

Each level of the trie has a dictionary which stores its child nodes keyed by the character.
Below is a representation of the levels of a Trie containing `BAN$` and `BANANA$`:
```
ROOT : {B: NODE1}  
NODE1: {A: NODE2}  
NODE2: {N: NODE3}  
NODE3: {$: TERMINALNODE} {A: NODE5}  
NODE4: {N: NODE6}  
NODE6: {A: NODE7}  
NODE7: {$: TERMINALNODE}  
```

A Trie implementation ensures that each query is linear to the length of the query string. This is because we are traversing the Trie using each character of the query string and checking if there is a terminal character when we reach the last letter.

Constructing a Trie can also be done in time linear to the length of the search text as we are just inserting each character into the Trie.

# Search Types
Freeform search: searches across groups (Users, Orgs, Tickets)
Field and Group search: filters a freeform search by group and field

# Note
1. The Trie is exportable. This means that it can be built, saved to disk and loaded as necessary.
2. Any objects can be stored in the TerminalNodes of the Trie, thus allowing flexible decisions as to what and how
   the results of queries are stored.
3. Optimal for exact and prefix matching.
4. Can be space inefficient as the nodes grow quadratic to the length of the search text.
   1. A suffix trie could be useful in this situation
   




