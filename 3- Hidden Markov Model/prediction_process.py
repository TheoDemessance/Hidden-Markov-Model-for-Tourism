def prediction(self, seq, L):
    S = dict()
    path = self.viterbi_path(seq)
    current = self.find_node(text = self.matrice_transition.index[path[-1] - 1])
    return self.suffixes(current, 1, S, '', L)
    
def suffixes(self, current, probability, S, suffix, L):
    if L == 0:
        return S
    
    else:
        for child in current.children[1:]:
            suffix += child[0]
            probability = probability * child[1] * child[3]
            S[suffix] = probability
            found = self.suffixes(child[2], probability, S, suffix, L-1)
            if found:
                return found