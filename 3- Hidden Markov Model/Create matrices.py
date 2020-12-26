def create_matrix_transition(self, current = None, visited = None):
    if not current:
        current = self.root
    
    if not visited:
        visited = []
        
    for i in range(len(current.children)):
        if(current.children[i][2] not in visited):
            self.matrice_transition.loc[current.text, current.children[i][2].text] = round(current.children[i][3], 2)
            visited.append(current)
            self.create_matrix_transition(current.children[i][2], visited) 
            
    self.matrice_transition = self.matrice_transition.fillna(0).astype('float')
    #self.matrice_transition = self.matrice_transition.to_numpy(dtype = 'float')
        

def create_matrix_emission(self, current = None, visited = None):
    if not current:
        current = self.root
    
    if not visited:
        visited = []
        
    for i in range(len(current.children)):
        if(current.children[i][2] not in visited):
            self.matrice_emission.loc[current.text, current.children[i][0]] = round(current.children[i][1], 2)
            visited.append(current)
            self.create_matrix_emission(current.children[i][2], visited) 
            
    self.matrice_emission = self.matrice_emission.fillna(0).astype('float')
    self.matrice_emission = self.matrice_emission.reindex(sorted(self.matrice_emission.columns), axis=1)
    #self.matrice_emission = self.matrice_emission.to_numpy(dtype = 'float')