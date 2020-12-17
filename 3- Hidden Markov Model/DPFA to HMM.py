# -*- coding: utf-8 -*-

'''
These are the two functions we added to our PrefixTree class.
They allow us to transform a DPFA into a HMMT by following our data structure. 
'''
def transform_to_HMMT(self, current = None, visited = None):
    '''

    Parameters
    ----------
    current : TrieNode, optional
        it corresponds to the node we are currently in. The default is None.
    visited : List, optional
        it corresponds to all the node we've already modified. With it, we won't iterate ad infinitum. The default is None.

    Returns
    -------
    A HMMT
    
    Recursively, it will transform the nodes by grouping the same transition (using sub function group_transition)
    and then, separate the emission functions and the transition functions.
    '''
    if not current:
        current = self.root
    
    if not visited:
        visited = []
        visited.append(current)
            
    for child in current.children[1:]:
        if(len(child) <= 3):
            trans = self.group_transition(current)

            for sub in trans:
                sum_ = 0
                for node in sub:
                    sum_ += node[1]
                for node in sub:
                    node[1] /= sum_
                    node.append(sum_) #we iterate through the different transitions, and we calculate the transition and emission probabilities 

    for child in current.children[1:]:
        if child[2] not in visited:  
            visited.append(current) 
            self.transform_to_HMMT(child[2], visited)      
            

def group_transition(self, node):
    '''
    

    Parameters
    ----------
    node : TrieNode
        The node we want to group the transitions.

    Returns
    -------
    result : List
        a List of Lists, which contains the different transitions splited.

    '''
    result = []
    for child in node.children[1:]:
        list_child = [x for x in node.children[1:] if x[2].state == child[2].state] #we compare all the nodes between each others
        if list_child not in result:
            result.append(list_child) #each time a node has the same destination, we group them together
            
    return result
