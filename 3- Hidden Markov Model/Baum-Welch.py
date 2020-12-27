def forward(self, V, a, b, initial_distribution):
    alpha = np.zeros((V.shape[0], a.shape[0]))
    alpha[0, :] = initial_distribution * b[:, V[0] + 1]
    #print(alpha)
    for t in range(1, V.shape[0]):
        for j in range(a.shape[0]):
            # Matrix Computation Steps
            #                  ((1x2) . (1x2))      *     (1)
            #                        (1)            *     (1)
            alpha[t, j] = alpha[t - 1].dot(a[:, j]) * b[j, V[t] + 1]
        
    return alpha
 
def backward(self, V, a, b):
    beta = np.zeros((V.shape[0], a.shape[0]))

    # setting beta(T) = 1
    beta[V.shape[0] - 1] = np.ones((a.shape[0]))

    # Loop in backward way from T-1 to
    # Due to python indexing the actual loop will be T-2 to 0
    for t in range(V.shape[0] - 2, -1, -1):
        for j in range(a.shape[0]):
            beta[t, j] = (beta[t + 1] * b[:, V[t + 1] + 1]).dot(a[j, :])
    
    return beta
 
def baum_welch(self, obs, initial_distribution = None, n_iter = 100):
        
    a = self.matrice_transition.to_numpy()
    b = self.matrice_emission.to_numpy()
    
    
    if not initial_distribution:
        initial_distribution = np.full(self.matrice_transition.to_numpy().shape[0], 1/self.matrice_transition.to_numpy().shape[0])
        #initial_distribution[0] = 1
    
    M = a.shape[0]
    T = len(obs)

    for n in range(n_iter):
        alpha = self.forward(obs, a, b, initial_distribution)
        beta = self.backward(obs, a, b)

        xi = np.zeros((M, M, T - 1))
        for t in range(T - 1):
            denominator = np.dot(np.dot(alpha[t, :].T, a) * b[:, obs[t + 1] + 1].T, beta[t + 1, :])
            for i in range(M):
                numerator = alpha[t, i] * a[i, :] * b[:, obs[t + 1] + 1].T * beta[t + 1, :].T
                xi[i, :, t] = numerator / denominator

        gamma = np.sum(xi, axis=1) 
        a = np.sum(xi, 2) / np.sum(gamma, axis=1).reshape((-1, 1))

        # Add additional T'th element in gamma
        gamma = np.hstack((gamma, np.sum(xi[:, :, T - 2], axis=0).reshape((-1, 1))))

        K = b.shape[1]
        denominator = np.sum(gamma, axis=1)
        for l in range(K):
            b[:, l] = np.sum(gamma[:, obs == l], axis=1)

        b = np.divide(b, denominator.reshape((-1, 1)))
    
    tmp1 = self.matrice_transition
    tmp2 = self.matrice_emission
    
    self.matrice_transition = pd.DataFrame(a, index = tmp1.index, columns = tmp1.columns)
    self.matrice_emission = pd.DataFrame(b, index = tmp2.index, columns = tmp2.columns)