class Graph:
    def addVertex(self, vert):
        #Add a vertex with key k to the vertex set.
        raise NotImplemented

    def addEdge(self, fromVert, toVert):
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

    ## Part 2
    def dfs(self, v):
        tree = {}
        tovisit = [(None, v)]
        while tovisit:
            a, b = tovisit.pop()
            if b not in tree:
                tree[b] = a
                for n in self.neighbors(b):
                    tovisit.append((b,n))
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

## Part 1
class SimpleUGraph(SimpleGraph):
    def addEdge(self, u, v):
        self._E.add((u, v))
        self._E.add((v, u))

    def removeEdge(self, u, v):
        self._E.remove((u, v))
        self._E.remove((v, u))

## Part 3
class AdjacencyListGraph(SimpleGraph):
    pass

class AdjacencyListUGraph(SimpleUGraph):
    pass

## Part 4
class AdjacencyMatrixGraph(AdjacencyListGraph):
    pass

class AdjacencyMatrixUGraph(AdjacencyListUGraph):
    pass

#Find Path Test Cases
# G = SimpleGraph({'A','B','C','D','E'}, {('A','B'), ('A','C'), ('B','E'), ('E','D')})
# print(G.findPath('A', 'D') == ['A', 'B', 'E', 'D'])

# G = SimpleGraph({'A', 'B', 'C', 'D', 'E', 'F'}, {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
# print(G.findPath('A', 'F'), ['A', 'B', 'C', 'D', 'E', 'F'])

# G = AdjacencyListGraph({'A','B','C','D','E'}, {('A','B'), ('A','C'), ('B','E'), ('E','D')})
# print(G.findPath('C', 'D'), None)
#
# G = AdjacencyListGraph({'A', 'B', 'C', 'D', 'E', 'F'}, {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
# print(G.findPath('B', 'E'), ['B', 'C', 'D', 'E'])
#
# G = AdjacencyListUGraph({'A','B','C','D','E'}, {('A','B'), ('A','C'), ('B','E'), ('E','D')})
# print(G.findPath('D', 'A'), ['D', 'E', 'B', 'A'])
#
# G = AdjacencyMatrixGraph(['A', 'B', 'C', 'D', 'E', 'F'], {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
# print(G.findPath('F', 'A'), None)
#
# G = AdjacencyMatrixGraph(['A','B','C','D','E'], {('A','B'), ('A','C'), ('B','E'), ('E','D')})
# print(G.findPath('D', 'E') == None)
# #
# G = AdjacencyMatrixUGraph(['A', 'B', 'C', 'D', 'E', 'F'], {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
# print(G.findPath('E', 'E') == None)
# print(G.findPath('E', 'E'))
# print(G.dfs('E'))