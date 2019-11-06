import networkx as nx
import numpy as np
import librootboard

class Board(object):
    """docstring for Board."""

    def __init__(self):
        try:
            A = np.loadtxt("boards/autumn.brd")
        except OSError:
            A = np.array([[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]])
        self.graph = nx.from_numpy_matrix(A)

    def generate(self, v=12, e=17, max_neighbours=6, min_neighbours=2, planar=False, nsuits=3):
        


    def plot(self):
        nx.draw_spring(self.graph)
