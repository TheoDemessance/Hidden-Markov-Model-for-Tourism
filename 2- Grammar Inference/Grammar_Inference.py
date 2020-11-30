#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class TrieNode:
    '''
    We initialize the class TrieNode, which represents a Node in the PrefixTree.
    We have the following attributes:
        - text: it represents the label of the node. 
        - is_word : it's a boolean True or False, according if the given node is a leaf or not. By default, it is False.
        - children : it's a list of all the nodes where the given node is going to transit, with a certain frequency/probability. 
                     By default, we give a ['#', '0', 'itself'] which represents the number of times a word ends in this node.
        - state: it's a unique id representing each node
        - frequency: a integer representing how many times a transition has been taken during the construction of a tree
        - alphabet : a list representing the unique 
        - previous: it's a list with all the predecessors of a node
    '''
    _COUNTER_NODE = 1
    def __init__(self, text = "λ"):
        self.text = text
        self.is_word = False
        self.children = list()
        self.children.append(['#', 0, self]) #1st element:SYMB 2nd element:FREQUENCY 3rd element:CHILDREN
        self.state = TrieNode._COUNTER_NODE
        self.frequency = 0
        self.alphabet = []
        TrieNode._COUNTER_NODE += 1
        self.previous = []

    def get_frequency(self):
        freq = 0
        for child in self.children[1:]:
            freq += child[1]
        return freq
    
    def get_frequency2(self):
        freq = 0
        for child in self.children:
            freq += child[1]
        return freq

    def __str__(self):
        return 'symb:{} state:{} -> children:{}'.format(self.text, self.state, self.children)

class PrefixTree:
    '''
    We initialize the class PrefixTree, starting with the root, an empty node.
    To this root, we use different functions
    '''
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, current = None):
        '''
        Adds a given word in the trie. 
        When inserting a sequence, a tree traverse is performed, starting at the root. 
        The traversal compares the first item of the sequence to the links attribute item in the root.
        
        - If no link exists or no link has the same item attribute, a new link to a new node is created. 
          The attribute item of the new link will be the item of the sequence and a frequency equals to one.

        - If a link with the same attribute item is found, its frequency is incremented by one. 
          Then, the traversal searches the next item of the sequence in the corresponding sub-tree. 

        - When an item is the last of a sequence, then the attribute in the end node of the traversal is incremented by one.
        
        
        Arguments:
        word -- a sequence of characters representing the word/sequence ('abc' -> add 'a' then 'b' then 'c') 
        
        Return:
        The updated version of the trie, with the added word inside
        '''
        if not current: 
            current = self.root
            pre = self.root
        for i, char in enumerate(word):
            current.frequency += 1
            if char not in [x[0] for x in current.children]:
                prefix = word[0:i+1]
                current.children.append([char, 1, TrieNode(prefix)])
                if(pre not in current.previous):
                    current.previous.append(pre)
                pre = current
                current = current.children[-1][2]

            else:
                for child in current.children:
                    if child[0] == char:
                        child[1] += 1
                        if(pre not in current.previous):
                            current.previous.append(pre)
                        pre = current
                        current = child[2]

        current.is_word = True   
        current.children[0][1] += 1
        current.frequency += 1
        
    def starts_with(self, prefix, current = None):
        '''
        It is the same process as the insertion part, except that we only read the caracters,
        and we do not increment the frequency.
        
        Arguments:
        prefix -- the beginning of a word
        
        Return:
        a list of all words beginning with the given prefix, or
        an empty list if no words begin with that prefix.
        '''
        words = list()
        if not current:
            current = self.root
        for char in prefix:
            if char not in [x[0] for x in current.children]:
                return list()
            for child in current.children:
                  if child[0] == char:
                    current = child[2]
        self.__child_words_for(current, words)
        return words
    
    def __child_words_for(self, node, words):
        '''
        Private helper function. Cycles through all children
        of node recursively, adding them to words if they
        constitute whole words (as opposed to merely prefixes).
        
        Arguments:
        node -- a given node in which we check the children
        words -- list of words which constitute whole words
        '''
        if node.is_word:
            words.append(node.text)
        for child in node.children[1:]:
            self.__child_words_for(child[2], words)
    
    def size(self, current = None, visited = None):
        '''
        Function to get the size of the trie. We iterate through all the children of each node
        and increment the count by one each time we encounter a new node.
        
        Arguments:
        current -- the current node we are in
        visited -- a list of nodes representing the nodes we have already visited (in case we have loops in the trie)
        
        Return:
        The size of this prefix tree, defined
        as the total number of nodes in the tree.
        '''
        if not current:
            current = self.root
        
        if not visited:
            visited = []
            visited.append(current)
            
        count = 1
        
        for child in current.children[1:]:
            if(child[2] not in visited):
                visited.append(child[2])
                count += self.size(child[2], visited)
                
        return count

    def leaf(self, current = None, visited = None):
        '''
        Function to get the number of leaves of the trie. We iterate through all the children of each node
        and increment the count by one each time we encounter a new node.
        
        Arguments:
        Same as size function
        
        Return:
        Number of leaves in a trie
        '''
        if not current: 
            current = self.root     
        if not visited:
            visited = []
        count = 0
        tmp = 0
        self.__leaves_for(current, count, visited)         
        return count
    
    def __leaves_for(self, current, count, visited):
        '''
        Private helper function. Cycles through all children
        of node recursively, adding them to words if they
        constitute whole words (as opposed to merely prefixes).
        '''
        if current.is_word == True:
            count += 1
        for child in current.children[1:]:
            if(child[2] not in visited):
                visited.append(child[2])
                self.__leaves_for(child[2], count, visited)
    
    def transform2proba(self, current = None):
        '''
        Recursive function to transform the FFA (Frequency Finite Automaton) into a PFA (Probabilistic Finite Automaton)
        by dividing the frequency of each branch by the sum of all frequencies : 
        
        Arguments: 
        current -- node in which we are currently in
        
        Return: 
        The updated trie transformed into a probabilistic automaton
        '''
        if not current:
            current = self.root
            
        freq = current.get_frequency2()
        for child in current.children:
            if(isinstance(child[1], int) == False):
                return 0
            else: 
                child[1] = child[1]/freq
                if child[2].state != current.state:
                    current = child[2]    
                    self.transform2proba(current)
    
    def predict(self, sequence, method = '', current = None):
        '''
        Function to predict with a given sequence, the next item according to 
        different probabilities.
        
        Arguments:
        sequence -- a given sequence to which we want to predict the next item
        method -- 2 choices : 
                        - fuzzy : return all the items in order to have a sum of their probabilities > 0.5
                        - deterministic : return the item with the highest proba
        current -- we give the choice to the user to start their traversal at a given node
        
        Return:
        According to the method used, either it returns a list of items (fuzzy method), or a unique item (deterministic method)
        '''
        if not current:
            current = self.root
         
        for char in sequence:
            for child in current.children:
                if child[0] == char:
                    current = child[2]
        
        probas = [[x[0], x[1]] for x in current.children]
        probas = sorted(probas, key = lambda x: x[1], reverse = True)
        
        sum_ = 0
        items = []
        for subproba in probas:
            sum_ += subproba[1]
            items.append((subproba[0], subproba[1]))
            if(sum_ > 0.5):
                break   
        if method == 'fuzzy':
            return items
        elif method == 'deterministic':
            return probas[0][0]

    def display(self):
        '''
        Prints the contents of this prefix tree.
        '''
        print('====================================================================================')
        self.__displayHelper(self.root)
        print('====================================================================================\n')
    
    def __displayHelper(self, current, visited = None):
        '''
        Private helper for printing the contents of this prefix tree.
        '''
        if not visited: 
            visited = []
        
        print(current)
        
        for child in current.children[1:]:
            if child[2] not in visited:
                visited.append(current)
                self.__displayHelper(child[2], visited)


# In[ ]:


def Alergia(sequences, alpha):
    '''
    Our version of the Alergia algorithm. It tries to recursively merge all the pairs of nodes, from the root to the leaves.
    Unlike the original version, the difference is that it does not test the compatibility of children of these pairs of nodes.
    
    Arguments: 
    sequences -- the sequences to build the Trie and then convert it in a PFA
    alpha -- an int between 0 and 1. It represents a parameter of the Hoeffding bounds. 
    
    Return:
    A DPA according to the sequences we have
    '''
    print('Starting building corresponding Trie \n')
    trie = PrefixTree()
    trie.alphabet = list({l for word in sequences for l in word})
    for subseq in sequences:
        trie.insert(subseq)
    print(trie.size())
    print(trie.leaf())
    #initial = trie.size()
    red = []
    red.append(trie.root)
    blue = []
    for x in trie.root.children[1:]:
        if(x[2] not in blue):
            blue.append(x[2])
    t0 = 0.5
    
    print('Running Alergia on trie \n')
    while(len(blue) > 0):
        qb = blue[0]
        blue.remove(qb)
        promote = True
        if(qb.get_frequency() >= t0):
            for qr in red:
                if(AlergiaCompatible(trie, qr, qb, alpha)):
                    #print('Merge accepted...')
                    #print(qr)
                    #print(qb)
                    trie = MergeFold(trie, qr, qb)
                    promote = False
                    for child in qr.children[1:]:    
                        if(child[2] not in blue and child[2].state != qr.state and child[2] not in red):
                            blue.append(child[2])
                    break
        
            if(promote == True):
                #print('No merge possible...')
                red.append(qb)
                for child in qb.children[1:]:
                    if(child[2] not in blue and child[2] not in red):
                        blue.append(child[2])
        else:
            continue
    
    trie.transform2proba()
    print('Algo done')
    return trie

def AlergiaCompatible(trie, qr, qb, alpha):
    '''
    Sub-method of the Alergia main one. It tells us if 2 nodes (a red and a blue) are compatible
    
    Arguments:
    trie -- the current trie we are working on
    qr -- a red node 
    qb -- a blue node
    alpha -- parameter alpha mentionned above
    
    Return:
    a boolean saying whether or not the 2 nodes in arguments are compatible
    '''
    correct = True
    if(AlergiaTest(qr.children[0][1], qr.get_frequency(), qb.children[0][1], qb.get_frequency(), alpha) == False):
        correct = False
    
    return correct
  
def AlergiaTest(f1, n1, f2, n2, alpha):
    '''
    Sub-method of the Alergia compatible method. It computes the hoeffding bounds and compare it to the gamma threshold
    
    Arguments:
    f1 -- incoming frequency of the node 1
    n1 -- number of times a word ends in node 1
    f2 -- incoming frequency of the node 2
    n2 -- number of times a word ends in node 2
    1 & 2 refers to the nodes we want to compare (i.e a node Red and a node Blue)
    alpha -- same parameter alpha as mentionned
    
    Return:
    True if gamma < hoeffding (then, the nodes are compatible)
    False if not
    '''
    gamma = math.fabs(f1/n1 - f2/n2)
    root = math.sqrt(1/(2*math.log(2/alpha)))
    summ = (1/math.sqrt(n1)) + (1/math.sqrt(n2))
    hoeffding = root * summ
    return gamma < hoeffding

def MergeFold(trie, qr, qb): 
    '''
    MERGE OPERATION: 
    To merge a BLUE node into a RED node, all the ingoing links of BLUE node are redirected to the RED node. 
    If the RED node already has an ingoing link with the same item attribute as a redirected link, then only the frequencies are added. 
    Next, the BLUE node attribute is added to the RED node attribute.
    
    FOLD OPERATION:
    When a BLUE node merges into a RED node, all children of BLUE node are recursively merged into children of the RED node with the same item attribute link.
    If the link with an item attribute doesn't exist in the RED node, a new child is inserted.
    
    Arguments:
    trie -- the current Trie we are working on
    qr -- the red node 
    qb -- the blue node to merge
    '''
    q = qb.previous[0]
    if qb.text[-1] not in qr.text:
        qr.text = qr.text+ ', ' + qb.text[-1]
    for child in q.children:
        if(child[2].state == qb.state):
            child[2] = qr 
    qr.children[0][1] += qb.children[0][1]
    words = trie.starts_with('', current = qb)
    for word in words:
        trie.insert(word)
    return trie


# In[ ]:


def Alergia(sequences, alpha):
    '''
    Original version of the Alergia Algorithm
    
    Arguments: 
    sequences -- the sequences to build the Trie and then convert it in a PFA
    alpha -- an int between 0 and 1. It represents a parameter of the Hoeffding bounds. 
    
    Return:
    A DPA according to the sequences we have
    '''
    print('Starting building corresponding Trie \n')
    trie = PrefixTree()
    trie.alphabet = list({l for word in sequences for l in word})
    for subseq in sequences:
        trie.insert(subseq)
    print(trie.size())
    print(trie.leaf())
    #initial = trie.size()
    red = []
    red.append(trie.root)
    blue = []
    for x in trie.root.children[1:]:
        if(x[2] not in blue):
            blue.append(x[2])
    t0 = 0.5
    
    print('Running Alergia on trie \n')
    while(len(blue) > 0):
        qb = blue[0]
        blue.remove(qb)
        promote = True
        if(qb.get_frequency() >= t0):
            for qr in red:
                if(AlergiaCompatible(trie, qr, qb, alpha)):
                    #print('Merge accepted...')
                    #print(qr)
                    #print(qb)
                    trie = MergeFold(trie, qr, qb)
                    promote = False
                    for child in qr.children[1:]:    
                        if(child[2] not in blue and child[2].state != qr.state and child[2] not in red):
                            blue.append(child[2])
                    break
        
            if(promote == True):
                #print('No merge possible...')
                red.append(qb)
                for child in qb.children[1:]:
                    if(child[2] not in blue and child[2] not in red):
                        blue.append(child[2])
        else:
            continue
    
    trie.transform2proba()
    print('Algo done')
    return trie

def AlergiaCompatible(trie, qr, qb, alpha):
    '''
    Sub-method of the Alergia main one. It tells us if 2 nodes (a red and a blue) are compatible
    
    Arguments:
    trie -- the current trie we are working on
    qr -- a red node 
    qb -- a blue node
    alpha -- parameter alpha mentionned above
    
    Return:
    a boolean saying whether or not the 2 nodes in arguments are compatible
    '''
    correct = True
    alphabet = list({l for word in ll for l in word})
    if(AlergiaTest(qr.children[0][1], qr.get_frequency(), qb.children[0][1], qb.get_frequency(), alpha) == False):
        correct = False
    
    for a un trie.alphabet:
        for children_r in qr.children:
            for children_b in qb.children:
                if(a == children_r[1] and a == children_b[1]):
                    if(AlergiaTest(children_r[2], children_r.frequency, children_b[2], children_b.frequency, alpha) == False):
                        correct = False
    return correct
  
def AlergiaTest(f1, n1, f2, n2, alpha):
    '''
    Sub-method of the Alergia compatible method. It computes the hoeffding bounds and compare it to the gamma threshold
    
    Arguments:
    f1 -- incoming frequency of the node 1
    n1 -- number of times a word ends in node 1
    f2 -- incoming frequency of the node 2
    n2 -- number of times a word ends in node 2
    1 & 2 refers to the nodes we want to compare (i.e a node Red and a node Blue)
    alpha -- same parameter alpha as mentionned
    
    Return:
    True if gamma < hoeffding (then, the nodes are compatible)
    False if not
    '''
    gamma = math.fabs(f1/n1 - f2/n2)
    root = math.sqrt(1/(2*math.log(2/alpha)))
    summ = (1/math.sqrt(n1)) + (1/math.sqrt(n2))
    hoeffding = root * summ
    return gamma < hoeffding

def MergeFold(trie, qr, qb): 
    '''
    MERGE OPERATION: 
    To merge a BLUE node into a RED node, all the ingoing links of BLUE node are redirected to the RED node. 
    If the RED node already has an ingoing link with the same item attribute as a redirected link, then only the frequencies are added. 
    Next, the BLUE node attribute is added to the RED node attribute.
    
    FOLD OPERATION:
    When a BLUE node merges into a RED node, all children of BLUE node are recursively merged into children of the RED node with the same item attribute link.
    If the link with an item attribute doesn't exist in the RED node, a new child is inserted.
    
    Arguments:
    trie -- the current Trie we are working on
    qr -- the red node 
    qb -- the blue node to merge
    '''
    q = qb.previous[0]
    if qb.text[-1] not in qr.text:
        qr.text = qr.text+ ', ' + qb.text[-1]
    for child in q.children:
        if(child[2].state == qb.state):
            child[2] = qr 
    qr.children[0][1] += qb.children[0][1]
    words = trie.starts_with('', current = qb)
    for word in words:
        trie.insert(word)
    return trie


# In[3]:


get_ipython().system('jupyter nbconvert --to script Grammar_Inference.ipynb')


# In[ ]:




