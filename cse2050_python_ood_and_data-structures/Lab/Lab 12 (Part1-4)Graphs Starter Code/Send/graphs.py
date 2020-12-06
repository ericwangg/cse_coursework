import random
import time

class Graph:
    def addVertex(self, vert):
        #Add a vertex with key k to the vertex set.
        raise NotImplemented

    def addEdge(self, fromVert, toVert): #fromVert = u  ,etc..
        #Add a directed edge from u to v.
        raise NotImplemented

    def neighbors(self):
        #Return an iterable collection of the keys of all
        #vertices adjacent to the vertex with key v.
        raise NotImplemented

    def removeEdge(self, u, v):
        #Remove the edge from vertex u to v from graph.
        raise NotImplemented

    def removeVertex(self, v):
        #Remove the vertex v from the graph as well as any edges
        #incident to v.
        raise NotImplemented


    def bfs(self, V):
        tree = {}
        tovisit = Queue([(None, v)])
        while tovisit:
            a, b = tovisit.dequeue()
            if b not in tree:
                tree[b] = a
                for n in self.neighbors(b):
                    tovisit.enqueue((b,n))
        return tree

    def dfs(self, v):
        tree = {}
        tovisit = [(None, v)]
        while tovisit:
            a, b = tovisit.pop()
            if b not in tree:
                tree[b] = a
                for n in self.neighbors(b):
                    tovisit.append((b, n))
        return tree

    def findPath(self, u, v):
        paths = self.dfs(u)
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

class SimpleGraph(Graph):
    def __init__(self, V, E):
        self._V = set()
        self._E = set()
        for v in V: self.addVertex(v)
        for u, v in E: self.addEdge(u,v)

    def vertices(self):
        return iter(self._V)

    def edges(self):
        return iter(self._E)

    def addVertex(self, v):
        self._V.add(v)

    def addEdge(self, u, v):
        self._E.add((u, v))

    def neighbors(self, v):
        return (w for u, w in self._E if u == v)

    def removeEdge(self, u, v):
        self._E.remove((u, v))

    def removeVertex(self, v):
        for neighbor in list(self.neighbors(v)):
            self.removeEdge(v, neighbor)
        self._V.remove(v)

## Part 1    Undirected - Think special case of Directed Graph
class SimpleUGraph(SimpleGraph):
    def addEdge(self, u, v):
        self._E.add((u, v))
        self._E.add((v, u))

    def removeEdge(self, u ,v):
        self._E.remove((u, v))
        self._E.remove((v, u))

## Part 3
class AdjacencyListGraph(Graph):
    def __init__(self, V, N):
        self._V = set()
        self._nbrs = dict()
        for v in V: self.addVertex(v)

    def vertices(self):
        return iter(self._V)

    def edges(self):
        for u in self._V:
            for v in self.neighbors(u):
                yield (u, v)

    def addVertex(self, v):
        self._V.add(v)
        self._nbrs[v] = set()

    def neighbors(self, v):
        return iter(self._nbrs[v])

    def addEdge(self, u, v):
        self._nbrs[u].add(v)

    def removeEdge(self, u, v):
        self._nbrs[u].remove(v)

    def removeVertex(self, v):
        for neighbor in list(self.neighbors(v)):
            self.removeEdge(v, neighbor)
        self._V.remove(v)


class AdjacencyListUGraph(AdjacencyListGraph):
    def addEdge(self, u, v):
        self._nbrs[u].add(v)
        self._nbrs[v].add(u)

    def removeEdge(self, u ,v):
        self._nbrs[u].remove(v)
        self._nbrs[v].remove(u)

class AdjacencyMatrixGraph(AdjacencyListGraph):
    def __init__(self, V, E):
        self._V = list()
        self._E = list()
        self._edges = set()

        for v in V: self.addVertex(v)
        for u, v in E: self.addEdge(u, v)


    def vertices(self):
        return self._V

    def edges(self):
        edgeList = []
        ic = 0
        jc = 0
        for i in self._E:
            for j in i:
                if j == 1:
                    edgeList.append( (self._V[ic], self._V[jc]) )
                jc += 1
            ic += 1
            jc = 0
        return iter(edgeList)



    def addVertex(self, v):
        self._V.append(v)
        newRow = [0]
        for row in self._E:
            row.append(0)
            newRow.append(0)
        self._E.append(newRow)

    def removeVertex(self, v):
        idx = self._V.index(v)
        for row in self._E:
            row.pop(idx)
        self._E.pop(idx)
        self._V.remove(v)

    def neighbors(self, v):
        nbrs = []
        idx = self._V.index(v)
        i = 0
        for n in self._E[idx]:
            if n == 1:
                nbrs.append(self._V[i])
            i += 1
        return nbrs

    def addEdge(self, u, v):
        u1 = self._V.index(u)
        v1 = self._V.index(v)
        self._E[u1][v1] = 1

    def removeEdge(self, u, v):
        u1 = self._V.index(u)
        v1 = self._V.index(v)
        self._E[u1][v1] = 0

    def matrix(self):
        return self._E

class AdjacencyMatrixUGraph(AdjacencyMatrixGraph):
    def addEdge(self, u, v):
        u1 = self._V.index(u)
        v1 = self._V.index(v)
        self._E[u1][v1] = 1
        self._E[v1][u1] = 1

    def removeEdge(self, u, v):       
        u1 = self._V.index(u)
        v1 = self._V.index(v)
        self._E[u1][v1] = 0
        self._E[v1][u1] = 0
