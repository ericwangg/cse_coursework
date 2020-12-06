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

    ## Part 2
    def dfs(self):       # depth-first search
        # spaths = dict()
        # spaths[v] = None
        # # for i in self.neighbors(v):    # find neightbors of v first
        # #     spaths[i] = v
        # for i in self.edges():         # then find unrelated edges to v
        #     spaths[i[1]] = i[0]        # may also work with just this, since it overwrites neighbors
        # return spaths                  # return desired "dict"
        raise NotImplemented

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

    # def findPath(self, u, v, path = []):          # findPath my way
    #     mypath = list(u)
    #     paths = self.dfs(u)
    #     if u == v:
    #         return mypath
    #     shortest = None
    #     for vertex in paths:
    #         if vertex != mypath:
    #             newpath = findPath(vertex, v)
    #             if newpath:
    #                 if not None or len(newpath) < len(shortest):
    #                     shortest = newpath

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
        return (w for u, w in self._E if u == v)       # what this for loop actually do?!?

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
    def __init__(self, V, N):       # V for Vertex, N for Neightbors
        self._V = set()
        self._nbrs = dict()
        for v in V: self.addVertex(v)       # every "V", "i" in PDF, initialize a new row and column
        for u, v in N: self.addEdge(u, v)

    def vertices(self):                 # same as SimplyGraph
        return iter(self._V)

    def edges(self):                    # corrected edges
        for u in self._V:               # in O(n^2) time for 2 for loops
            for v in self.neighbors(u):
                yield (u, v)
        # return iter(self._nbrs)

    def addVertex(self, v):             # corrected
        self._V.add(v)
        self._nbrs[v] = set()

    def neighbors(self, v):                  # nbrs function for making _nbrs iterable
        return iter(self._nbrs[v])
                                        # using makes _nbrs dict() an iterable object
    def addEdge(self, u, v):            # edge ops w/ _nbrs
        self._nbrs[u].add(v)

    def removeEdge(self, u, v):         # now a dict, pop / del / remove properly
        self._nbrs[u].remove(v)

    def removeVertex(self, v):          # same as SimpleGraph
        for neighbor in list(self.neighbors(v)):
            self.removeEdge(v, neighbor)
        self._V.remove(v)

    # def hasedge(self, u, v):            # from slides, checks edges of vertex "v"
    #     return v in self._nbrs(u)

class AdjacencyListUGraph(AdjacencyListGraph):
    def addEdge(self, u, v):
        self._nbrs[u].add(v)
        self._nbrs[v].add(u)

    def removeEdge(self, u ,v):
        self._nbrs[u].remove(v)
        self._nbrs[v].remove(u)

# # MY WAY OF ADJACENCY MATRIX
# class AdjacencyMatrixGraph(Graph):
#     def __init__(self, V, E):      # every "V", "i" in PDF, initialize a new row and column
#         # CORRECT LIST INITILIZATION
#         self._V = V             # set Vertices, givse size of Matrix
#         self._E = [[0 for y in range(len(self._V))] for x in range(len(self._V))]       # set Edges, builds from empty list
#
#         if 'A' in self._V:         # letters for columns and rows
#             for edge in E:
#                 self._E[ ord(edge[0]) - 65][ ord(edge[1]) - 65 ] = 1
#         else:
#             for edge in E:
#                 self._E[edge[0] - 1][edge[1] - 1] = 1
#
#         key = {'A':0, 'B':1, 'C': 2, 'D':3, 'E':4, 'F':5, 'G':6}
#         key2 = {'A':1, 'B':2, 'C': 3, 'D':4, 'E':5, 'F':6, 'G':7}       # reflects the indices like the numbers given in numerical Vertices
#
#         # # CORRECT DICT INITILIZATION
#         # self._V = dict()
#         # for v in self._V
#         #     dict(v) = None
#         #
#         # self._E = dict()
#         # for u in self._
#
#     def vertices(self):
#         return iter(self._V)
#
#     def matrix(self):
#         return self._E
#
#     def edges(self):
#         key = {'A':0, 'B':1, 'C': 2, 'D':3, 'E':4, 'F':5, 'G':6}
#         keyflip = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G'}
#         # Jbara: Key not scaleable, can use char() for ASCII code,
#         newEdges = set()
#         myEdges = self._E
#         for i in range(len(myEdges)):
#             for j in range(len(myEdges[i])):
#                 if myEdges[i][j] == 1:
#                     if 'A' in self._V:
#                         # newEdges.add( (keyflip.get(i), keyflip.get(j)))
#                         newEdges.add( (chr(i + 65), chr(j + 65) ))
#                     else:
#                         newEdges.add( (i + 1 , j + 1) )
#         return newEdges
#         #
#         # return self._E
#         # [[0, 1, 0, 0, 0, 0],
#         # [0, 0, 1, 0, 0, 0],
#         # [0, 0, 0, 1, 0, 0],
#         # [0, 0, 0, 0, 1, 0],
#         # [0, 0, 0, 0, 0, 1],
#         # [0, 0, 0, 0, 0, 0]]
#
#         ########### Tupler helper ##########
#         # l = self._E
#         # for num in range(len(l)):
#         #     if type(l[num]) == list:
#         #         l[num] = tuple(l[num])
#         #     else:
#         #         l = tuple(l)
#         # l = tuple(l)
#         # return l
#
#     def addVertex(self, u):         #adds a row (new []) and column ', 0'
#         if 'A' in self._V:
#             self._V.add( ord(u) - 65)
#             self._E.add( ord(u) - 65)
#         else:
#             self._V.add(u)
#             self._E.add(u)
#
#     def removeVertex(self, v):      #removes a row (new []) and column ', 0'
#         if 'A' in self._V:
#             self._V.remove(v)
#             self._E.pop( ord(v) - 65)
#             for i in range(len(self._E)):
#                 self._E[i].pop( ord(v) - 65)
#         else:
#             # Old REMOVE method
#             # self._V.remove(v)
#             # self._E.pop(v - 1)
#             # for i in range(len(self._E)):
#             #     self._E[i].pop(v - 1)
#             self._V.remove(v)
#             self._E[v - 1] = [None for i in range(len(self._V) + 1)]
#             for i in range(len(self._E)):
#                 if self._E[i] == None:
#                     pass
#                 else:
#                     self._E[i].pop(v - 1)
#                     self._E[i].insert(v - 1, None)
#
#     def addEdge(self, u, v):       # Finds cell based on tuple (2, 3) ex. and adds 1
#         if u == v:
#             raise("same vertex %s and %s" % (u, v))
#         else:
#             if 'A' in self._V:
#                 self._E[ ord(u) - 65 ][ ord(v) - 65 ] = 1
#             else:
#                 self._E[u][v] = 1
#
#     def removeEdge(self, u, v):     # Removes 1, makes 0
#         if u == v:
#             raise("same vertex %s and %s" % (u, v))
#         else:
#             if 'A' in self._V:
#                 self._E[ ord(u) - 65 ][ ord(v) - 65 ] = 0
#             else:
#                 self._E[u][v] = 0
#
#     def neighbors(self, u):            # Matrix Neightbors
#         return iter(self.edges())
#
#     def nbrs(self, u):               # Matrix nbrs, wtf
#         return iter(self.edges())
#
#     def hasEdge(self, u, v):
#         if self._E[u][v] != 0:
#             return True
#         else:
#             return False
#
#     def dfs(self, v):
#         tree = {}
#         tovisit = [(None, v)]
#         while tovisit:
#             a, b = tovisit.pop()
#             if b not in tree and None:
#                 tree[b[0]] = a[0]
#                 for n in self.neighbors(b):
#                     tovisit.append((b, n))
#         return tree
#
# class AdjacencyMatrixUGraph(AdjacencyMatrixGraph):
#     def __init__(self, V, E):      # every "V", "i" in PDF, initialize a new row and column
#         # CORRECT LIST INITILIZATION
#         self._V = V             # set Vertices, givse size of Matrix
#         self._E = [[0 for y in range(len(self._V))] for x in range(len(self._V))]       # set Edges, builds from empty list
#         if 'A' in self._V:         # letters for columns and rows
#             for edge in E:
#                 self._E[ ord(edge[0]) - 65][ ord(edge[1]) - 65 ] = 1
#                 self._E[ ord(edge[1]) - 65][ ord(edge[0]) - 65 ] = 1
#         else:
#             for edge in E:
#                 self._E[edge[0] - 1][edge[1] - 1] = 1
#                 self._E[edge[1] - 1][edge[0] - 1] = 1
#
#         key = {'A':0, 'B':1, 'C': 2, 'D':3, 'E':4, 'F':5, 'G':6}
#         key2 = {'A':1, 'B':2, 'C': 3, 'D':4, 'E':5, 'F':6, 'G':7}
#
#     def addEdge(self, u, v):                           # when adding (2, 3) also add cell (3,2 )
#         if u == v:
#             raise("same vertex %d and %d" % (u, v))
#         else:
#             self._V[u][v] = 1
#             self._V[v][u] = 1
#
#     def removeEdge(self, u ,v):
#         if u == v:
#             raise("No edges between %d and %d" % (u, v))
#         else:
#             self._V[u][v] = 0
#             self._V[v][u] = 0
#     def addEdge(self, u, v):       # Finds cell based on tuple (2, 3) ex. and adds 1
#         if u == v:
#             raise("same vertex %s and %s" % (u, v))
#         else:
#             if 'A' in self._V:
#                 self._E[ ord(u) - 65 ][ ord(v) - 65 ] = 1
#                 self._E[ ord(v) - 65 ][ ord(u) - 65 ] = 1
#             else:
#                 self._E[u][v] = 1
#                 self._E[v][u] = 1
#
#     def removeEdge(self, u, v):     # Removes 1, makes 0
#         if u == v:
#             raise("same vertex %s and %s" % (u, v))
#         else:
#             if 'A' in self._V:
#                 self._E[ ord(u) - 65 ][ ord(v) - 65 ] = 0
#                 self._E[ ord(v) - 65 ][ ord(u) - 65 ] = 0
#             else:
#                 self._E[u][v] = 0
#                 self._E[v][u] = 0

class AdjacencyMatrixGraph(AdjacencyListGraph):         # Adj matrix using adj list, can also be done with 'check' Bool - (u, v, Bool)
    def __init__(self, V, E):       # V for Vertex, N for Neightbors
        self._V = list()
        self._E = list()
        self._edges = set()

        for v in V: self.addVertex(v)       # every "V", "i" in PDF, initialize a new row and column
        for u, v in E: self.addEdge(u, v)


    def vertices(self):                 # same as SimplyGraph
        return self._V

    def edges(self):                    # corrected edges
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

        # # Method 2
        # killList = []
        # for i in self._edges:
        #     if i[0] == v or i[1] == v:
        #         killList.append(i)
        # for j in killList:
        #     self._edges.remove(j)

    def addVertex(self, v):
        self._V.append(v)
        newRow = [0]
        for row in self._E:
            row.append(0)
            newRow.append(0)
        self._E.append(newRow)

    def removeVertex(self, v):          # same as SimpleGraph
        idx = self._V.index(v)
        for row in self._E:
            row.pop(idx)
        self._E.pop(idx)
        self._V.remove(v)

    def neighbors(self, v):                  # nbrs function for making _nbrs iterable
        nbrs = []
        idx = self._V.index(v)
        i = 0
        for n in self._E[idx]:
            if n == 1:
                nbrs.append(self._V[i])
            i += 1
        return nbrs
                                        # using makes _nbrs dict() an iterable object
    def addEdge(self, u, v):            # edge ops w/ _nbrs
        u1 = self._V.index(u)
        v1 = self._V.index(v)
        self._E[u1][v1] = 1
        # self._edges.add( (u,v) )

    def removeEdge(self, u, v):         # now a dict, pop / del / remove properly
        u1 = self._V.index(u)
        v1 = self._V.index(v)
        self._E[u1][v1] = 0
        # self._edges.remove( (u,v) )

    def matrix(self):
        return self._E

class AdjacencyMatrixUGraph(AdjacencyMatrixGraph):
    def addEdge(self, u, v):            # edge ops w/ _nbrs
        u1 = self._V.index(u)
        v1 = self._V.index(v)
        self._E[u1][v1] = 1
        self._E[v1][u1] = 1

    def removeEdge(self, u, v):         # now a dict, pop / del / remove properly
        u1 = self._V.index(u)
        v1 = self._V.index(v)
        self._E[u1][v1] = 0
        self._E[v1][u1] = 0


# ################################ Part 4 Test
# g1 = AdjacencyMatrixGraph(['A', 'B', 'C', 'D', 'E', 'F'], {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('A', 'D'), ('F', 'C')})
# print(set(g1.vertices()) == {'A', 'B', 'C', 'F', 'E', 'D'})
# print(set(g1.edges()) ==  {('B', 'C'), ('C', 'D'), ('F', 'C'), ('A', 'B'), ('D', 'E'), ('E', 'F'), ('A', 'D')})
# g1.removeEdge('C', 'D')
# print(set(g1.edges()) == {('A', 'B'), ('E', 'F'), ('F', 'C'), ('A', 'D'), ('B', 'C'), ('D', 'E')})
########## ^^^ All return True

# ############################### Part 4 Numbers

# print([1,2,3,4], {(1,2), (1,4), (2,3)})
# g1 = AdjacencyMatrixGraph([1,2,3,4], {(1,2), (1,4), (2,3)})
# #
# print(set(g1.vertices()) == {1, 2, 3, 4})
# print(list(g1.vertices()))
# print(len(list(g1.vertices())))
# #
# print(set(g1.edges()) == {(1, 2), (1, 4),(2, 3)})
# print(g1.edges())
# # print(g1.matrix())
# print('\n')
# g1.removeVertex(1)
# print(set(g1.vertices()) == {2, 3, 4})
# print(g1.edges())
#
# print(set(g1.edges()) == {(2, 3)})
# print(set(g1.edges()))
# print(g1.matrix())

############################## Part 4 U Graph #################################
g1 = AdjacencyMatrixUGraph(['A', 'B', 'C', 'D', 'E', 'F'], {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('A', 'D'), ('F', 'C')})
print(set(g1.vertices()) == {'A', 'B', 'C', 'F', 'E', 'D'})
# print(set(g1.edges()) == {('A', 'B'), ('F', 'C'), ('D', 'E'), ('B', 'C'), ('D', 'C'), ('E', 'D'), ('E', 'F'), ('C', 'B'), ('F', 'E'), ('A', 'D'), ('D', 'A'), ('C', 'F'), ('B', 'A'), ('C', 'D')})
# print(g1.matrix())
# g1.removeEdge('C', 'D')
# print(g1.matrix())

# print(set(g1.edges()) =={('F', 'E'), ('E', 'D'), ('C', 'F'), ('D', 'E'), ('B', 'A'), ('F', 'C'), ('A', 'D'), ('A', 'B'), ('B', 'C'), ('E', 'F'), ('D', 'A'), ('C', 'B')})
#
# g1 = AdjacencyMatrixUGraph([1,2,3,4], {(1,2), (1,4), (2,3)})
# print(set(g1.vertices()) == {1, 2, 3, 4})
# print(set(g1.edges()) =={(1, 2), (3, 2), (2, 1), (1, 4), (2, 3), (4, 1)})
# g1.removeVertex(1)
# print(set(g1.vertices()) == {2, 3, 4})
# print(set(g1.edges()) =={(2, 3), (3, 2)})

# ############################### DFS TESTING ####################################
# G = SimpleGraph({'A','B','C','D','E'}, {('A','B'), ('A','C'), ('B','E'), ('E','D')})
# print(G.dfs('A') == {'A': None, 'B': 'A', 'C': 'A', 'D': 'E', 'E': 'B'})
#
# G = SimpleGraph({'A', 'B', 'C', 'D', 'E', 'F'}, {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
# print(G.dfs('A') == {'A': None, 'B': 'A', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E'})
#
# G = AdjacencyListGraph({'A','B','C','D','E'}, {('A','B'), ('A','C'), ('B','E'), ('E','D')})
# print(G.dfs('A') == {'A': None, 'B': 'A', 'C': 'A', 'D': 'E', 'E': 'B'})
#
# G = AdjacencyListGraph({'A', 'B', 'C', 'D', 'E', 'F'}, {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
# print(G.dfs('A') == {'A': None, 'B': 'A', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E'})
#
# G = AdjacencyListUGraph({'A','B','C','D','E'}, {('A','B'), ('A','C'), ('B','E'), ('E','D')})
# print(G.dfs('A') == {'A': None, 'B': 'A', 'C': 'A', 'D': 'E', 'E': 'B'})
#
# G = AdjacencyMatrixGraph(['A', 'B', 'C', 'D', 'E', 'F'], {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
# print(G.dfs('A') == {'A': None, 'B': 'A', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E'})
# print(G.dfs('A'))

# G = AdjacencyMatrixGraph(['A','B','C','D','E'], {('A','B'), ('A','C'), ('B','E'), ('E','D')})
# print(G.dfs('A')== {'A': None, 'B': 'A', 'C': 'A', 'D': 'E', 'E': 'B'})
#
# G = AdjacencyMatrixUGraph(['A', 'B', 'C', 'D', 'E', 'F'], {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
# print(G.dfs('A') == {'A': None, 'B': 'A', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E'})

############################### Test w Jbara ###################################
# s0 = M1.edges()
# s1 = set(s0)
# for x in s1:
#     print(x)
# print(s1 == {('B', 'C'), ('C', 'D'), ('F', 'C'), ('A', 'B'), ('D', 'E'), ('E', 'F'), ('A', 'D')})
#
# print({('B', 'C'), ('C', 'D'), ('F', 'C'), ('A', 'B'), ('D', 'E'), ('E', 'F'), ('A', 'D')})
# print('\n')
#
# g1.removeEdge('C', 'D')
# print(set(g1.edges()) == {('A', 'B'), ('E', 'F'), ('F', 'C'), ('A', 'D'), ('B', 'C'), ('D', 'E')})
# print(set(g1.edges()))
# print({('A', 'B'), ('E', 'F'), ('F', 'C'), ('A', 'D'), ('B', 'C'), ('D', 'E')})
#
# # Jbara
#
# g = (x for x in range(3))
# set(g)


# g1.removeVertex(1)
# set(g1.vertices()) == {2, 3, 4}
# set(g1.edges()) == {(2, 3
# print(g1)
# print(set(g1.vertices()))

#test from lecture
# V = set()
# E = set()
# for i in range(1000):
#     V.add(i)
# for i i in range(100000):
#     f = random.randint(0, 999)
#     s = random.randint(0, 999)
#     if f != s:
#         E.add((f, s))
#
# G1 = AdjacencyListGraph({1, 2, 3}, {(1, 2), (2, 1), (2, 3)})
# G2 = SimpleGraph({1, 2, 3}, {(1, 2), (2, 1), (1, 3)})
# print(G1)
# print(G2)
