The generated FPT cannot be used directly due to its large number of nodes. The number of nodes is at most the number of unique items power the length of the largest sequence in the sequences set. To overcome this problem, one must reduce its size using grammatical inference (GI).

The grammatical inference is a method of machine learning which consists of reducing a FPT into a stochastic automaton by merging nodes. Two nodes can be merged if they have the same grammatical rules, i.e. they valid the compatibility test. Two nodes validating the compatibility test are said compatible.

Alergia is a GI method, which takes as a parameter the FPT and iteratively attempts to merge all node pairs. Two nodes are merged if they are compatible. With Alergia algorithm, the compatibility between two nodes depends on the compatibility between all their children until the leaves. 

To check if two nodes are compatible, the number of tests to compute with a given FPT having n different items and a height of h is at most n^h. Performing the compatibility test between each pair of nodes in the FPT generates an explosion of combinations.

To counter this problem, we purpose a Relaxed Alergia algorithm. In this folder, both of the method are implemented, and tests are conducted and shown below.
