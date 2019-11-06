import numpy as np


def binary_rperm(m, x):
    # Returns an m long vector containing x ones
    E = np.hstack((np.ones(x,dtype=np.int8),
        np.zeros(m - x,dtype=np.int8)))
    np.random.shuffle(E)
    return E

def random_given_sum(N, sum):
    # generates N random integers that sum to sum
    A = np.hstack((np.random.randint(0,sum,(N-1,),dtype=np.int8),[0,sum]))
    A.sort()
    return A[1:]-A[:-1]

def node_connections(self, N, u, c):
    # Distributes c connections between N uxu matrices
    # adhering to the bounds in max_neighbours and min_neighbours
    E = np.zeros((u,u,N), dtype=np.int8)

    # This array decides how many ones to populate the g, ith col with
    num_ones = random_given_sum(N*u, c)

    print(num_ones, sum(num_ones), c)

    for g in range(N):
        for i in range(u):
            E[:,i,g] = binary_rperm(u, num_ones[g])

    return E

def form_block_list(E, N):
    # Takes a 3-array E and whacks it into a Nu*Nu matrix's upper diagonal
    if E.shape[2] < N*(N-1)//2:
        raise IndexError('E array is not tall enough -\
         z axis is %d long, requires %d' % (E.shape[2],N*(N-1)//2))

    block_list = []
    b = 0
    Z = np.zeros_like(E[:,:,0])

    for i in range(N):
        block_list.append([])
        for j in range(N):
            if j <= i:
                block_list[i].append(Z)
            else:
                block_list[i].append(E[:,:,b])
                b += 1

    return block_list
