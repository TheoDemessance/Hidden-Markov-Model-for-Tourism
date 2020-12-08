#!/usr/bin/env python
# coding: utf-8

import Original_Alergia 
import Relaxed_Alergia

if __name__ == '__main__':
    
    with open("../1- Data Analysis/sequences.txt") as file:
        sequences = [line.strip() for line in file]
    
    print('\n ------------------ \n')
    print('Sequences : ', sequences)
    print('\n ------------------ \n')
    
    dfa_ori = Original_Alergia.Original_Alergia(sequences, 1/1000)
    
    print('\n ------------------ \n')
    
    dfa_relax = Relaxed_Alergia.Relaxed_Alergia(sequences, 1/1000)
    
    print('\n ------------------ \n')
    print('Original : ', dfa_ori.size())
    print('Relaxed : ', dfa_relax.size())
    print('\n ------------------ \n')

