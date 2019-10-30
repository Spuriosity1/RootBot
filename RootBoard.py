import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def binary_rperm(e, N):
    # Returns a random permutation of e ones and N-e zeros
    E = np.hstack((np.ones(e,dtype=np.int8),
        np.zeros(N - e,dtype=np.int8)))
    np.random.shuffle(E)
    return E

def form_block_list(E, N):
    # Takes a 3-array E and whacks it into the matrix's upper diagonal
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


class ClearingGraph(object):
    """Represents an undirected graph of Root clearings"""

    def __init__(self, v, e, nsuits=3):
        super(ClearingGraph, self).__init__()
        self.v = v
        self.e = e
        self.nsuits=nsuits
        self.conn = None
        if v%nsuits != 0:
            print("WARN: nodes will not be evenly shared between suits")
            v = v-v%nsuits
            print("Readjusting to v=%d" % v)
        if e > (v**2)*(nsuits-1)//(2*nsuits):
            print("ERROR: It is not possible to distribute %s edges and preserve n-particity" % e)
        if 2+e-v < 0:
            print("There is no planar graph with these parameters.")

    def form_graph(self):
        # Randomly distributes e edges between the 3u^2 possible interconnections
        u = self.v//self.nsuits

        num_blocks = self.nsuits*(self.nsuits-1)//2
        # Number of upper-diagonal interconnections to fill
        E = binary_rperm(self.e, num_blocks*u**2)
        E = E.reshape((u,u, num_blocks)) # make into a longish 3-matrix
        A = np.block(form_block_list(E, self.nsuits))
        A += A.T
        print(A)
        return nx.from_numpy_matrix(A)

    def generate(self):
        self.graph = self.form_graph()
        self.draw()


    def draw(self):
        plt.clf()
        # nx.draw_kamada_kawai(self.graph)
        try:
            nx.draw_planar(self.graph)
        except nx.NetworkXException:
            nx.draw_spring(self.graph)




rb = ClearingGraph(15,27)
rb.generate()
rb.draw()
