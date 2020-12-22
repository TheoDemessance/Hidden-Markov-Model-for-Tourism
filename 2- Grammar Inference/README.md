## Learning Process

The learning process is a set of algorithms to build a mathematical model from raw data in aims to induct knowledge, called <b>grammatical rules</b>.

To learn from the sequences set and to induce grammatical rules, our learning process starts by modeling the sequences set to the **frequency prefix tree** . On the basis of the tree model, **grammatical rules** are inducted. To make predictions easier, we have structured the rules in an **HMM**.

In what follows, we will represent each element of the sequence by a unique integer called item. In other words, an item refers to a place visited by a tourist.

### Frequency Prefix Tree (FPT)

Also known as Trie, it represents a directed rooted hierarchical tree where the nodes and the link are weighted.  The link between two nodes of FPT is weighted with two attributes; the first one, in parenthesis, is an item and the second one is its frequency of occurrence in the sequences set. 

The nodes have one attribute that corresponds to the number of times a sequence ends in this node. By default, it equals zero.

The construction of FPT consists of inserting each item of the sequences in the tree. At the beginning, the FPT is only composed of a root with zero as attribute. The insertion process is an iterative process on each sequence. The process of constructing FPT is described in *trie.py* file.

### Relaxed and original Alergia algorithm

**Relaxed Alergia algorithm** tries to recursively merge all the pairs of nodes, from the root to the leaves. Unlike the **Original Alergia algorithm**, it does not test the compatibility of children of these pairs of nodes.

To differentiate nodes that cannot merge from those that will be tested, we define two types of nodes, RED nodes and BLUE nodes.
In the beginning, only the root node of the FPT is RED, and BLUE contains the direct children of the root. The BLUE nodes are visited successively. Once visited, a BLUE node tries to merge with the RED node. If the visited node does not merge, it becomes a RED node and all its children become BLUE. This process is repeated until all FPT nodes are RED.
When a BLUE node is compatible with a RED node, the **merging process** is launched. the merging process is composed of two operations *Merge* and *Fold*. 

#### Merge operation
To merge a BLUE node into a RED node, all the ingoing links of BLUE node are redirected to the RED node. If the RED node already has an ingoing link with the same item attribute as a redirected link, then only the frequencies are added. Next, the BLUE node attribute is added to the RED node attribute.

#### Fold operation
When a BLUE node merges into a RED node, all children of BLUE node are recursively merged into children of the RED node with the same item attribute link. If the link with an item attribute doesn't exist in the RED node, a new child is inserted.

The output of the Relaxed Alergia algorithm is a graph with frequency and item called **frequency automaton**.
To make a prediction, in the literature, there are not existing algorithms or methods that allow us to analyze a frequency automaton. Thus, we will transform the frequency automaton into an **Hidden Markov Models**. 
