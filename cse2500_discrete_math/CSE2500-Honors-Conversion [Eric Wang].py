from collections import deque, namedtuple

inf = float('inf')                                  # makes infinity easier to reference with no errors
Edge = namedtuple('Edge', 'start, end, cost')       # makes edges more easily referenceable

def make_edge(start, end, cost=1):
  return Edge(start, end, cost)

class SimpleUGraph:
    def __init__(self, E):      #E for edges
        wrongEdge = [i for i in E if len(i) not in [2, 3]]
        if wrongEdge:
            raise ValueError('Invalid cities: {}'.format(wrongEdge))
        self._E = [make_edge(*edge) for edge in E]

    @property
    def vertices(self):
        return set(sum(([edge.start, edge.end] for edge in self._E), [] ))

    def nodePairs(self, n1, n2, both_ends=True):        #nP = pairs of nodes
        if both_ends:
            nP = [[n1, n2], [n2, n1]]
        else:
            nP = [[n1, n2]]
        return nP

    def removeEdge(self, n1, n2, both_ends=True):
        nP = self.nodePairs(n1, n2, both_ends)
        E = self._E[:]
        for edge in E:
            if [edge.start, edge.end] in nP:
                self._E.remove(edge)

    def addEdge(self, n1, n2, cost=1, both_ends=True):
        nP = self.nodesPairs(n1, n2, both_ends)
        for edge in self._E:
            if [edge.start, edge.end] in nP:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self._E.append(Edge(start = n1, end = n2, cost = cost))
        if both_ends:
            self._E.append(Edge(start = n2, end = n1, cost = cost))

    @property
    def neighbors(self):
        nbrs = {vertex: set() for vertex in self.vertices}
        for edge in self._E:
            nbrs[edge.start].add((edge.end, edge.cost))
        return nbrs

    def Dijkstra(self, a, b):
            # a = start city, b = dest. city, d = distance between two cities
        assert a in self.vertices, "Flight plans for city not considered"
        d = {vertex: inf for vertex in self.vertices}
        lastV = {vertex: None for vertex in self.vertices}
        d[a] = 0
        vertices = self.vertices.copy()
        while vertices:
            thisV = min(vertices, key=lambda vertex: d[vertex])
            vertices.remove(thisV)
            if d[thisV] == inf:
                break
            for nbr, cost in self.neighbors[thisV]:
                altPath = d[thisV] + cost
                if altPath < d[nbr]:
                    d[nbr] = altPath
                    lastV[nbr] = thisV
        path, thisV = deque(), b
        while lastV[thisV] is not None:
            path.appendleft(thisV)
            thisV = lastV[thisV]
        if path:
            path.appendleft(thisV)
        return path

    def flightCost(self, a, b):
        flightmap = {('a','d',100), ('a','b',140), ('a','e',350), ('b','d',85), ('b','c',110), ('c','e',125), ('c','f',200), ('d','e',365), ('e','f',145), ('e','g',220), ('f','g',80)}
        citymap = {'a':'San Francisco', 'b': 'Denver', 'c': 'Chicago', 'd': 'Los Angelos', 'e':'Boston', 'f':'Atlanta', 'g':'Orlando'}
        map = self.Dijkstra(a,b)
        sum = 0
        x = 0
        for i, j in enumerate(map):
            if i < 1:
                track = j
            else:
                for n in flightmap:
                    if track in n and j in n:
                        sum += n[2]
                track = j
        print('Least expensive combination of flights from %s to %s costs $%s' % (citymap.get(a), citymap.get(b), sum))

def main():
    citymap = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    fm1 = {('a','d',100), ('a','b',140), ('a','e',350), ('b','d',85), ('b','c',110), ('c','e',125), ('c','f',200), ('d','e',365), ('e','f',145), ('e','g',220), ('f','g',80)}
    fm2= {('d','a',100), ('b','a',140), ('e','a',350), ('d','b',85), ('c','b',110), ('e','c',125), ('f','c',200), ('e','d',365), ('f','e',145), ('g','e',220), ('g','f',80)}
    #fm1 is the flight mapping with
    flightmap = fm1.union(fm2)
    KAYAK = SimpleUGraph(flightmap)

    print("Ignore extra lines of 'None' ")
    print(KAYAK.Dijkstra('d', 'e'))     # LA to Boston
    print(KAYAK.flightCost('d', 'e'))   # 365
    print(KAYAK.Dijkstra('a', 'g'))     # San Fran to Orlando
    print(KAYAK.flightCost('a', 'g'))   # 140 + 110 + 200 + 80 = 530
    print(KAYAK.Dijkstra('b', 'f'))     # Denver to Atlanta
    print(KAYAK.flightCost('b', 'f'))   # 110 + 200 = 310
    print('Other tests from Eric to show the method works')
    print('\n')
    print(KAYAK.Dijkstra('g', 'd'))     # Orlando to LA
    print(KAYAK.flightCost('g', 'd'))   # 80 + 200 + 110 + 475

if __name__ == "__main__":
    main()

############# 2a - Cities, and flight Costs
# a - San Francisco
# b - Denver
# c - Chicago
# d - Los Angelos
# e - Boston
# f - Atlandta
# g - Orlando

############ 2b - Sarch algorithm outputs - least expensive flights city to city
# d to e    (LA to Boston)          # should return 320
# a to g    (San Fran to Orlando)   # should return 530
# b to f    (Denver to Atlanta)    # should return 310
# Additinal self tests
# g to d    (Orlando to LA)         # should return 475
