import random
import pprint

class Graph:
    nodes = []
    edges = []
    removed_edges = []
    def remove_edge(self,x,y):
        e = (x,y)
        try:
            self.edges.remove(e)
            print("Removed edge %s" % str(e))
            self.removed_edges.append(e)
        except:
            print("Attempted to remove edge %s, but it wasn't there" % str(e))

    def Nodes(self):
        return self.nodes

    # Sample data
    def __init__(self):
        self.nodes = [1,2,3,4,5]
        self.edges = [
            (3,5),
            (4,2),
            (5,2),
            (2,1),
            (3,1),
            (4,1)
        ]

G = Graph()
N = G.Nodes()
for  x in N:
   for y in N:
      for z in N:
         #print("(%d,%d,%d)" % (x,y,z))
         if (x,y) != (y,z) and (x,y) != (x,z):
            if (x,y) in G.edges and (y,z) in G.edges:
                G.remove_edge(x,z)

print("Removed edges:")
pprint.pprint(G.removed_edges)
print("Remaining edges:")
pprint.pprint(G.edges)