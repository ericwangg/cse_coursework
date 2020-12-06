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

class Queue:
    def __init__(self, L):
        self._L = L

    def enqueue(self, item):
        self._L.append(item)

    def dequeue(self):
        return self._L.pop(0)

    def __len__(self):
        return len(self._L)

    def isempty(self):
        return len(self) == 0


class SimpleUGraph():
    def __init__(self, V, E):
        self._V = set()
        for v in V:
            self.addVertex(v)

        self._E = set()
        for u, v in E:
            self.addEdges( (u,v) )

        # self._M = dict()     #mapping of edges to labels
        # for i in self.edges():
        #     self._M[i] = None

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

    def addEdge(self, u, v):
        self._E.add((u, v))
        self._E.add((v, u))
        # if label == None:
        #     self._M[(u, v)] = label     # can't assign to function call wtf
        #     self._M[(v, u)] = label

    def removeEdge(self, u ,v):
        self._E.remove((u, v))
        self._E.remove((v, u))
        # if label != None:
        #     self._M[(u, v)] = None
        #     self._M[(v, u)] = None

    def neighbors(self, v):
        return (w for u, w in self._E if u == v)       # what this for loop actually do?!?

# bfs & findPath
    def bfs(self, v):       #breadth-first search, using queue
        tree = {}
        tree[v] = None
        queue = [v]
        while queue != []:
            cur = queue.pop(0)
            for i in self.neighbors(cur):
                if i not in tree:
                    tree[i] = cur
                    queue.append(i)
        return tree

    def getPath(self, d ,v):
        keyset = list(d.keys())[0]
        listV = [v]
        i = v
        while i != keyset:
            try:
                i = d[i]
            except KeyError:
                return None
            listV = [i] + listV
        return listV

    def findPath(self, u ,v):
        if u == v:
            return None
        d = self.bfs(u)
        return self.getPath(d, v)

    # def getLabel(self, u, v):
    #     if (u,v) in self._M:
    #         return self._M.get((u,v))

def createActorGraph(mapAtoM):
    m = mapAtoM
    G = SimpleUGraph(set(), set())
    for actor in m.keys():
        G.addVertex(actor)
    for actor1 in m.keys():
        for actor2 in m.keys():
            if actor1 == actor2:
                pass
            for movie in m[actor1]:
                if movie in m[actor2]:
                    G.addEdge(actor1, actor2)
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
