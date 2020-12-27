def create_matrix_transition(self, current = None, visited = None):
        if not current:
            current = self.root
        
        if not visited:
            visited = []   
            
        for i in range(len(current.children)):
            #We group the transitions having the same "destination" node, to fill the matrix with the transition probability
            listt = self.group_transition(current)
            for c in listt:
                self.matrice_transition.loc[current.text, c[0][2].text] = round(c[0][3], 2)
            visited.append(current)
                
        for i in range(len(current.children)):
            #we iterate in all the children to fill all the matrix
            if(current.children[i][2] not in visited):
                self.create_matrix_transition(current.children[i][2], visited) 
                
        self.matrice_transition = self.matrice_transition.fillna(0).astype('float')
        
    def create_matrix_emission(self, current = None, visited = None):
        if not current:
            current = self.root
        
        if not visited:
            visited = []
            
        for i in range(len(current.children)):
            self.matrice_emission.loc[current.text, current.children[i][0]] = round(current.children[i][1], 2)
            visited.append(current)
        
        for i in range(len(current.children)):
            if(current.children[i][2] not in visited):
                self.create_matrix_emission(current.children[i][2], visited) 
        
                
        self.matrice_emission = self.matrice_emission.fillna(0).astype('float')
        self.matrice_emission = self.matrice_emission.reindex(sorted(self.matrice_emission.columns), axis=1)
