import math

class PQ:
    def __init__(self):
        self._L = []

    def insert(self, item, priority):
        self._L.append((item, priority))

    def findmin(self):
        return min(self._L, key = lambda x : x[1])[0]

    def removemin(self):
        item, priority = min(self._L, key = lambda x : x[1])
        self._L.remove((item, priority))
        return item

    def reducepriority(self, n, m):
        for k in range(len(self._L)):
            if self._L[k][0] == n:
                self._L[k] = (n, m)

    def __len__(self):
        return len(self._L)

def getMapAtoM():
  fp = open("lg_actor_data.txt", "r")
  mapAtoM = {}
  for s in fp:
    if not s.strip():
      continue

    #print(s)
    l1 = s.split("\t")
    if s[0].isalpha():
      actor = l1[0].split("(")[0].strip()
    movie = l1[-1].split(")")[0].strip() + ')'
    #print ("ACTOR:",actor)
    #print("MOVIE:", movie)

    if actor not in mapAtoM:
      mapAtoM[actor] = set([movie])
    elif movie not in mapAtoM[actor]:
      mapAtoM[actor].add(movie)

  fp.close()
  return mapAtoM

## Use the SimpleUGraph from the previous lab
class SimpleUGraph():
    def __init__(self, V=[], E=[], w = None):
        self._V = set()
        self._E = set()
        self._M = dict()  #mapping of edges to labels
        for v in V: self.addVertex(v)
        for u, v, w in E: self.addEdge(u,v, w)
        # for u, v, w in self._M:
        #     self.

# Vertex
    def vertices(self):
        return iter(self._V)

    def addVertex(self, v):
        self._V.add(v)

    def removeVertex(self, v):
        for neighbor in list(self.neighbors(v)):
            self.removeEdge(v, neighbor)
        self._V.remove(v)

# Edges
    def edges(self):
        return iter(self._E)

    def addEdge(self, u, v, wt):
        self._E.add((u, v))
        self._E.add((v, u))
        if wt != None:
            self._M[(u, v)] = wt     # can't assign to function call wtf
            self._M[(v, u)] = wt
        #     pass

    def removeEdge(self, u , v, wt):
        self._E.remove((u, v))
        self._E.remove((v, u))
        if wt != None:
            self._M[(u, v)] = None     # can't assign to function call wtf
            self._M[(v, u)] = None
        #     pass

    def neighbors(self, n):
        return (v for u, v in self._E if u == n)       # what this for loop actually do?!?

    # def dfs(self, v):                      #working dfs for SimpleGraph, from lecture
    #     tree = {}
    #     tovisit = [(None, v)]
    #     while tovisit:
    #         a, b = tovisit.pop()
    #         if b not in tree:
    #             tree[b] = a
    #             for n in self.neighbors(b):
    #                 tovisit.append((b,n))
    #     return tree

    def bfs(self, V):       #breadth-first search, using queue
        tree = {}
        tovisit = Queue([(None, v)])
        while tovisit:
            a, b = tovisit.dequeue()
            if b not in tree:
                tree[b] = a
                for n in self.neighbors(b):
                    tovisit.enqueue((b,n))
        return tree

    def findPath(self, u, v):
        paths = self.bfs(u)
        mypath = []
        if u == v:
            return None
        elif v in paths:
            mypath.append(v)
            cur = v
            while paths[cur] != None:
                mypath.append(paths[cur])
                cur = paths[cur]
            mypath.reverse()
            return mypath
        else:
            return None

    def getLabel(self, u, v):
        if (u,v) in self._M:
            return self._M.get((u,v))

    def getLabel(self, u, v):
        if (u,v) in self._M:
            return self._M.get((u,v))

    def weight(self, x, y):
        for u, vin self._E:
            if x == u and v == y:
                return weight


def createActorGraph(mapAtoM):
    m = mapAtoM
    G = SimpleUGraph(set(), set(), None)
    for actor in m.keys():
        G.addVertex(actor)
    for actor1 in m.keys():
        for actor2 in m.keys():
            if actor1 == actor2:
                pass
            for movie in m[actor1]:
                if movie in m[actor2]:
                    G.addEdge(actor1, actor2, None)
    return G

def KBNcompute(G, A):
    KBN = G.findPath(A, 'Bacon, Kevin')
    if A == 'Bacon, Kevin':
        return 0
    else:
        if KBN is None:
            return float('inf')
        else:
            return len(KBN) - 1




def Dijkstra(G, v):
    tree = {v, None}
    D = {u: float('inf') for u in G.vertices()}
    D[v] = 0
    tovisit = PQ()
    for u in G.vertices():
        tovisit.insert(u, D[u])
    while len(tovisit) != 0:
        u = tovisit.removemin()
        for n in G.neighbors(u):
            if D[u] + G.weight(u,n) < D[n]:
                D[n] + G.weight(u, n)
                tree[n] = u
                tovisit.reducepriority(n, D[n])
    return tree, D

## Use getPath() function fro previous lab


mapAtoM = getMapAtoM()
G = createActorGraph(mapAtoM)

paths = Dijkstra(G, 'Bacon, Kevin')

path1 = getPath(G, paths, 'Weaver, Jason')
for x in path1[::-1]:
    print(x)

path2 = getPath(G, paths, 'Costner, Kevin')
for x in path2[::-1]:
    print(x)

path3 = getPath(G, paths, 'Pesci, Joe')
for x in path3[::-1]:
    print(x)
