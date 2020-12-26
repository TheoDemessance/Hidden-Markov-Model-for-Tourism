# Hidden Markov model 

To transform a frequency automaton into a Hidden Markov Models (HMM), one has to start to change the frequency automaton into a **stochastic automaton**. This first step consists to convert the frequencies to relative frequency. 

The process to transform a stochastic automaton into an HMM is described and proved by **[Dupont et al](https://www.researchgate.net/publication/2640446_Probabilistic_DFA_Inference_using_Kullback-Leibler_Divergence_and_Minimality)** and **[Harbrard et al](https://hal.archives-ouvertes.fr/hal-00085176v2)**. The steps of the process are not discussed in this folder. Although we provide an explanation of the structure of an HMM.

An HMM is a graph where a node has a set of couples [item, probability], refer to the *probability* to generate the *item* on this node. The item *#* refers to the end of a sequence. The root node of an HMM is characterised by an ingoing arc without a start node. Links possess a *probability* to go from a node to another node. 

#### All the different python files you can see are provided here separately to make it easier for you to understand our approach. During the realization of our work, we added the different functions in our *TrieNode* class. No need to adapt the code.

## Prediction process

In a HMM, the prediction process is done from a given sequence of items. Therefore, it is necessary to find where to start the prediction thanks to the **Viterbi algorithm**, implemented in our case as you can see in *Viterbi.py*. Given an input sequence of items, this algorithm computes the most probable sequence of observations.

In our context, we want to predict the behavior of a tourist given a chronological sequence of visited places. Following the prediction process, we can recommend visiting one or many suffixes following the decreasing value of their probabilities.

## Update process

The update process adapts the probabilities to jump and the probabilities to generate items for a sequence set. To update the HMM, we use the **Baum-Welch algorithm**. In our method, we implement this algorithm without any modification, so it isn't discussed in this paper.
