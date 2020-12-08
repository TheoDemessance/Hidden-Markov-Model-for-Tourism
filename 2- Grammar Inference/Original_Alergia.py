#!/usr/bin/env python
# coding: utf-8
import math
import trie 

def Original_Alergia(sequences, alpha):
    '''
    Original version of the Alergia Algorithm
    
    Arguments: 
    sequences -- the sequences to build the Trie and then convert it in a PFA
    alpha -- an int between 0 and 1. It represents a parameter of the Hoeffding bounds. 
    
    Return:
    A DPA according to the sequences we have
    '''
    print('Starting building corresponding Trie \n')
    pfa = trie.PrefixTree()
    pfa.alphabet = list({l for word in sequences for l in word})
    for subseq in sequences:
        pfa.insert(subseq)
    
    print('Initial size of the PFA', pfa.size(), '\n')
    
    red = []
    red.append(pfa.root)
    blue = []
    for x in pfa.root.children[1:]:
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
                if(Original_AlergiaCompatible(pfa, qr, qb, alpha)):
                    #print('Merge accepted...')
                    #print(qr)
                    #print(qb)
                    pfa = Original_MergeFold(pfa, qr, qb)
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
    
    pfa.transform2proba()
    print('Algo done')
    return pfa

def Original_AlergiaCompatible(pfa, qr, qb, alpha):
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
    if(Original_AlergiaTest(qr.children[0][1], qr.get_frequency(), qb.children[0][1], qb.get_frequency(), alpha) == False):
        correct = False
    
    for a in pfa.alphabet:
        for children_r in qr.children:
            for children_b in qb.children:
                if(a == children_r[1] and a == children_b[1]):
                    if(Original_AlergiaTest(children_r[2], children_r.frequency, children_b[2], children_b.frequency, alpha) == False):
                        correct = False
    return correct
  
def Original_AlergiaTest(f1, n1, f2, n2, alpha):
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

def Original_MergeFold(pfa, qr, qb): 
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
    words = pfa.starts_with('', current = qb)
    for word in words:
        pfa.insert(word)
    return pfa




