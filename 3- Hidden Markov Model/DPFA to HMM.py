def group_transition(self, node):
    result = []
    for child in node.children:
        list_child = [x for x in node.children if x[2].state == child[2].state]
        if list_child not in result:
            result.append(list_child)
            
    return result

def transform_to_HMMT(self, current = None, visited = None):
    if not current:
        current = self.root
    
    if not visited:
        visited = []
        visited.append(current)
        
    freq = current.get_frequency2()
    
    for child in current.children:
        if(len(child) <= 3):
            trans = self.group_transition(current)

            for sub in trans:
                sum_ = 0
                for node in sub:
                    sum_ += node[1]
                for node in sub:
                    node[1] /= sum_
                    node.append(sum_)              

    for child in current.children[1:]:
        if child[2] not in visited:  
            visited.append(current) 
            self.transform_to_HMMT(child[2], visited)   