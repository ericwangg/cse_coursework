from queue import *

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

def getMapAtoM():
  fp = open("lg_actor_data.txt", "r")
  mapAtoM = {}
  for s in fp:
    if not s.strip():
      continue

    print(s)
    l1 = s.split("\t")
    if s[0].isalpha():
      actor = l1[0].split("(")[0].strip()
    movie = l1[-1].split(")")[0].strip() + ')'
    print ("ACTOR:",actor)
    print("MOVIE:", movie)

    if actor not in mapAtoM:
      mapAtoM[actor] = set([movie])
    elif movie not in mapAtoM[actor]:
      mapAtoM[actor].add(movie)
  fp.close()
  return mapAtoM
## Use the SimpleUGraph from the previous lab
class SimpleUGraph():
    # ####### for taking in 1 dictionary 'mapAtoM'
    # def __init__(self, D):
    #     self._V = set()
    #     for v in D.keys():
    #         self.addVertex(v)
    #
    #     self._E = set()
    #     for actor1 in D.keys():
    #         for actor2 in D.keys():
    #             if actor1 == actor2:
    #                 pass
    #             else:
    #                 if d[actor1].intersection(d[actor2]):
    #                     self.addEdge( (actor1, actor2) )
    #
    #     self._M = dict()     #mapping of edges to labels
    #     for i in self.edges():
    #         self._M[i] = None

    ######## for taking in 2 empty set()
    def __init__(self, V, E):
        self._V = set()
        for v in V:
            self.addVertex(v)

        self._E = set()
        for u, v in E:
            self.addEdges( (u,v))

        self._M = dict()     #mapping of edges to labels
        for i in self.edges():
            self._M[i] = None

        # for u in D.values():
        #     for w in list(d[i]):
        #         self.addEdge( w[0], w[1], None )      #modded movies init

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

    def addEdge(self, u, v, label):
        self._E.add((u, v))
        self._E.add((v, u))
        if label == None:
            self._M[(u, v)] = label     # can't assign to function call wtf
            self._M[(v, u)] = label

    def removeEdge(self, u ,v):
        self._E.remove((u, v))
        self._E.remove((v, u))
        if label != None:
            self._M[(u, v)] = None
            self._M[(v, u)] = None

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
        keys = list(d.key())[0]
        listV = [v]
        i = v
        while i != keys:
            try:
                i = keys[i]
            except KeyError:
                return None
            listV = [i] + listV
        return listV

    def findPath(self, u ,v):
        if u == v:
            return None
        d = self.bfs(u)
        return self.getPath(d, v)

    def getLabel(self, u, v):
        if (u,v) in self._M:
            return self._M.get((u,v))

def createActorGraph(mapAtoM):
    ########### HELP from Matt IMPLEMENTATION ##############
    # MtoA = {}                                   #to have Movie to Actors
    # for actor, movies in mapAtoM.items():
    #     for movie in movies:
    #         MtoA[movie] = MtoA.get(movie, list())
    #         MtoA[movie].append(actor)
    #
    # G = SimpleUGraph()
    # for actor in mapAtoM.keys():
    #     G.addVertex(actor)
    # for movie, actor in mapAtoM.items():
    #     for a in range(len(actor)):
    #         for b in range(a+1, len(actor)):
    #             G.addEdge( (actor.get(a), actor.get(b)) )
    # return G


    ############# A_imp
    m = mapAtoM
    G = SimpleUGraph(set(), set())
    for actor1 in m.keys():
        G.addVertex(actor1)
    for actor1 in m.keys():
        for actor2 in m.keys():
            if actor1 == actor2:
                pass
            for movie in m[actor1]:
                for movie in m[actor2]:
                    G.addEdge(actor1, actor2)
    return G

    ############ RY IMP, USING MOD SIMPLE U ##########
    ## Should work with modded SimpleUGraph to takin in mapAtoM

        ########### JR
        # m = mapAtoM
        # G = SimpleUGraph(set(), set())
        # for actor1 in m.keys():
        #     G.addVertex(actor1)
        #     for actor2 in m.keys():
        #         if actor1 == actor2:
        #             pass
        #         elif actor2 in G._V:
        #             pass
        #         elif (actor1, actor2) in G._E:
        #             pass
        #         elif m[actor1].intersection(m[actor2]) != {}:
        #             G.addEdge(actor1, actor2, None)
        # return G

    G = SimpleUGraph(mapAtoM)
    return G

def KBNcompute(G, A):
    KBN = G.findPath(A, 'Kevin Bacon')
    if A == 'Bacon, Kevin':
        return 0
    else:
        if KBN == None:
            return math.inf
        else:
            return len(KBN) - 1                 #Subtract 1 for Keivn Bacon himself
