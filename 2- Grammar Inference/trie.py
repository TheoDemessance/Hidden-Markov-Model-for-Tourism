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