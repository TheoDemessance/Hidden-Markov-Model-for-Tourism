 # Our Grammar Inference approach and results: 
 
 Our learning process consists to induct grammatical rules from the sequences set. The process is composed of four steps, described in the following process:
 
## Creation of the FPTA 

In order to be able to make our predictions, we first need to create our prefix tree, representing all the possible sequences read by the tree. 

We start by creating the *TrieNode* class. It represents a node of our tree. It takes as attribute:
- a string of characters 'text', which represents the label of each node.
- an 'is_word' boolean initialized to False. It becomes True if it has no children (i.e. if the word is finished).
- a list of children, to which we initialise for all nodes the first element representing the number of words ending at that node (completes the boolean presented above)
- an integer 'state', which represents the id of the node. It is unique for each node of the tree.
- an 'is_displayed' boolean initialized to False. It is used when displaying the tree, when there are loops so that it is only displayed once.
- a list of precedents, which grows as you go along. All the precedents of each node are added to it. For the root node, we consider that its predecessor is itself.

For the *PrefixTree* class, which represents the tree as such, we have:
- a *TrieNode* which represents the root node
- the class functions that we will detail below

### Class functions of *PrefixTree*.

#### Insert function:
It allows us to insert a word (taken as a parameter), starting from a certain node (current parameter). To do so, we enumerate the word (each character is taken one by one with its corresponding index), then, if the character is not present in the children list, we will create a node and then increment the indices. If there is already a child node with the same character, we increment its frequency by 1. When the word is finished, we pass the boolean to True, and we increment the word counter by 1. 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Trie_example.svg/1200px-Trie_example.svg.png" alt="Drawing" style="width: 50px;"/>
