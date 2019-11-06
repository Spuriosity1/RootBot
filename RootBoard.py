import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from librootboard import *


class Graph(object):
    """Represents an undirected, weightless graph"""

    def __init__(self, v=0, e=0):
        # Constructor given v nodes
        self.A = np.zeros((v,v),dtype=np.int8)
        self.e = e
        self.v = v
        self.V = [i for i in range(v)]

    def __len__(self):
        return self.A.shape[0]

    def __getitem__(self, i):
        if type(i) is not int:
            raise TypeError("Nodes can only be accessed by integers")
        return (self.V[i], list(self.argwhere(A[:,i] != 0)))

    def __setitem__(self, i, value):
        if type(i) is not int:
            raise TypeError("Nodes can only be accessed by integers")
        self.V[i] = value


    def neigbours(self, i=None):
        if i is not None:
            return np.sum(self.A[i,:])
        elif type(i) is int:
            return np.sum(self.A, axis=0)
        else:
            raise TypeError("Nodes can only be accessed by integers")


class ClearingGraph(Graph):
    """Represents an undirected graph of Root clearings"""

    def __init__(self, v, e, nsuits=3, min_neighbours=2, max_neighbours=4):
        super(ClearingGraph, self).__init__(v,e)
        self.nsuits=nsuits
        self.min_neighbours = min_neighbours
        self.max_neighbours = max_neighbours

        if v%nsuits != 0:
            print("WARN: nodes will not be evenly shared between suits")
            v = v-v%nsuits
            print("Readjusting to v=%d" % v)
        if e > (v**2)*(nsuits-1)//(2*nsuits):
            print("ERROR: It is not possible to distribute %s edges and preserve n-particity" % e)
        if 2+e-v < 0 or e > 3*v-6:
            print("ERROR: There is no planar graph with these parameters.")



    def form_graph(self):
        # Randomly distributes e edges between the 3u^2 possible interconnections
        u = self.v//self.nsuits

        num_blocks = self.nsuits*(self.nsuits-1)//2
        # Number of upper-diagonal interconnections to fill
        E = binary_rperm(num_blocks*u**2, self.e)
        E = E.reshape((u,u, num_blocks)) # make into a long 3-matrix
        A = np.block(form_block_list(E, self.nsuits))
        A += A.T
        print(A)
        self.A = A

    def generate(self):
        self.form_graph()

        self.draw()


    def draw(self):
        plt.clf()
        # nx.draw_kamada_kawai(self.graph)
        g = nx.from_numpy_matrix(self.A)    
        nx.draw_spring(g)




rb = ClearingGraph(15,27)
rb.generate()
rb.draw()
