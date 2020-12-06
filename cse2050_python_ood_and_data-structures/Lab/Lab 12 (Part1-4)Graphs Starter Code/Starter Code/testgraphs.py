import unittest
from graphs import *

class TestGraphs(unittest.TestCase):
	def testSimpleUGraph(self):
		g1 = SimpleUGraph({1,2,3,4}, {(1,2), (1,4), (2,3)})
		self.assertEqual(set(g1.vertices()), {1, 2, 3, 4})
		self.assertEqual(set(g1.edges()), {(1, 2), (3, 2), (1, 4), (2, 1), (2, 3), (4, 1)})
		g1.removeVertex(1)
		self.assertEqual(set(g1.vertices()), {2, 3, 4})
		self.assertEqual(set(g1.edges()), {(3, 2), (2, 3)})

		g1 = SimpleUGraph({'A', 'B', 'C', 'D', 'E', 'F'}, {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('A', 'D'), ('F', 'C')})
		self.assertEqual(set(g1.vertices()), {'A', 'B', 'D', 'E', 'F', 'C'})
		self.assertEqual(set(g1.edges()), {('A', 'B'), ('E', 'D'), ('D', 'C'), ('F', 'C'), ('C', 'F'), ('E', 'F'), ('F', 'E'), ('B', 'C'), ('D', 'A'), ('C', 'D'), ('C', 'B'), ('B', 'A'), ('A', 'D'), ('D', 'E')})
		g1.removeVertex('C')
		self.assertEqual(set(g1.vertices()), {'F', 'E', 'B', 'A', 'D'})
		self.assertEqual(set(g1.edges()), {('A', 'B'), ('E', 'D'), ('E', 'F'), ('F', 'E'), ('D', 'A'), ('B', 'A'), ('A', 'D'), ('D', 'E')})
		g1.removeEdge('A', 'D')
		self.assertEqual(set(g1.edges()), {('F', 'E'), ('A', 'B'), ('E', 'F'), ('B', 'A'), ('E', 'D'), ('D', 'E')})

	def testDfs(self):
		G = SimpleGraph({'A','B','C','D','E'}, {('A','B'), ('A','C'), ('B','E'), ('E','D')})
		self.assertEqual(G.dfs('A'), {'A': None, 'B': 'A', 'C': 'A', 'D': 'E', 'E': 'B'})

		G = SimpleGraph({'A', 'B', 'C', 'D', 'E', 'F'}, {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
		self.assertEqual(G.dfs('A'), {'A': None, 'B': 'A', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E'})

		G = AdjacencyListGraph({'A','B','C','D','E'}, {('A','B'), ('A','C'), ('B','E'), ('E','D')})
		self.assertEqual(G.dfs('A'), {'A': None, 'B': 'A', 'C': 'A', 'D': 'E', 'E': 'B'})

		G = AdjacencyListGraph({'A', 'B', 'C', 'D', 'E', 'F'}, {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
		self.assertEqual(G.dfs('A'), {'A': None, 'B': 'A', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E'})

		G = AdjacencyListUGraph({'A','B','C','D','E'}, {('A','B'), ('A','C'), ('B','E'), ('E','D')})
		self.assertEqual(G.dfs('A'), {'A': None, 'B': 'A', 'C': 'A', 'D': 'E', 'E': 'B'})

		G = AdjacencyMatrixGraph(['A', 'B', 'C', 'D', 'E', 'F'], {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
		self.assertEqual(G.dfs('A'), {'A': None, 'B': 'A', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E'})

		G = AdjacencyMatrixGraph(['A','B','C','D','E'], {('A','B'), ('A','C'), ('B','E'), ('E','D')})
		self.assertEqual(G.dfs('A'), {'A': None, 'B': 'A', 'C': 'A', 'D': 'E', 'E': 'B'})

		G = AdjacencyMatrixUGraph(['A', 'B', 'C', 'D', 'E', 'F'], {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
		self.assertEqual(G.dfs('A'), {'A': None, 'B': 'A', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E'})
		
	def testAdjacencyLists(self):
		g1 = AdjacencyListGraph({'A', 'B', 'C', 'D', 'E', 'F'}, {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('A', 'D'), ('F', 'C')})
		self.assertEqual(set(g1.vertices()), {'A', 'B', 'C', 'F', 'E', 'D'})
		self.assertEqual(set(g1.edges()), {('B', 'C'), ('C', 'D'), ('F', 'C'), ('A', 'B'), ('D', 'E'), ('E', 'F'), ('A', 'D')})
		g1.removeEdge('C', 'D')
		self.assertEqual(set(g1.edges()), {('A', 'B'), ('E', 'F'), ('F', 'C'), ('A', 'D'), ('B', 'C'), ('D', 'E')})

		g1 = AdjacencyListGraph({1,2,3,4}, {(1,2), (1,4), (2,3)})
		self.assertEqual(set(g1.vertices()), {1, 2, 3, 4})
		self.assertEqual(set(g1.edges()), {(1, 2), (1, 4),(2, 3)})
		g1.removeVertex(1)
		self.assertEqual(set(g1.vertices()), {2, 3, 4})
		self.assertEqual(set(g1.edges()), {(2, 3)})

	def testAdjacencyULists(self):
		g1 = AdjacencyListUGraph({'A', 'B', 'C', 'D', 'E', 'F'}, {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('A', 'D'), ('F', 'C')})
		self.assertEqual(set(g1.vertices()), {'A', 'B', 'C', 'F', 'E', 'D'})
		self.assertEqual(set(g1.edges()), {('A', 'B'), ('F', 'C'), ('D', 'E'), ('B', 'C'), ('D', 'C'), ('E', 'D'), ('E', 'F'), ('C', 'B'), ('F', 'E'), ('A', 'D'), ('D', 'A'), ('C', 'F'), ('B', 'A'), ('C', 'D')})
		g1.removeEdge('C', 'D')
		self.assertEqual(set(g1.edges()), {('F', 'E'), ('E', 'D'), ('C', 'F'), ('D', 'E'), ('B', 'A'), ('F', 'C'), ('A', 'D'), ('A', 'B'), ('B', 'C'), ('E', 'F'), ('D', 'A'), ('C', 'B')})

		g1 = AdjacencyListUGraph({1,2,3,4}, {(1,2), (1,4), (2,3)})
		self.assertEqual(set(g1.vertices()), {1, 2, 3, 4})
		self.assertEqual(set(g1.edges()), {(1, 2), (3, 2), (2, 1), (1, 4), (2, 3), (4, 1)})
		g1.removeVertex(1)
		self.assertEqual(set(g1.vertices()), {2, 3, 4})
		self.assertEqual(set(g1.edges()), {(2, 3), (3, 2)})

	def testFindPath(self):
		G = SimpleGraph({'A','B','C','D','E'}, {('A','B'), ('A','C'), ('B','E'), ('E','D')})
		self.assertEqual(G.findPath('A', 'D'), ['A', 'B', 'E', 'D'])

		G = SimpleGraph({'A', 'B', 'C', 'D', 'E', 'F'}, {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
		self.assertEqual(G.findPath('A', 'F'), ['A', 'B', 'C', 'D', 'E', 'F'])

		G = AdjacencyListGraph({'A','B','C','D','E'}, {('A','B'), ('A','C'), ('B','E'), ('E','D')})
		self.assertEqual(G.findPath('C', 'D'), None)

		G = AdjacencyListGraph({'A', 'B', 'C', 'D', 'E', 'F'}, {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
		self.assertEqual(G.findPath('B', 'E'), ['B', 'C', 'D', 'E'])

		G = AdjacencyListUGraph({'A','B','C','D','E'}, {('A','B'), ('A','C'), ('B','E'), ('E','D')})
		self.assertEqual(G.findPath('D', 'A'), ['D', 'E', 'B', 'A'])

		G = AdjacencyMatrixGraph(['A', 'B', 'C', 'D', 'E', 'F'], {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
		self.assertEqual(G.findPath('F', 'A'), None)

		G = AdjacencyMatrixGraph(['A','B','C','D','E'], {('A','B'), ('A','C'), ('B','E'), ('E','D')})
		self.assertEqual(G.findPath('D', 'E'), None)

		G = AdjacencyMatrixUGraph(['A', 'B', 'C', 'D', 'E', 'F'], {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')})
		self.assertEqual(G.findPath('E', 'E'), None)

	def testAdjacencyMatrix(self):
		g1 = AdjacencyMatrixGraph(['A', 'B', 'C', 'D', 'E', 'F'], {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('A', 'D'), ('F', 'C')})
		self.assertEqual(set(g1.vertices()), {'A', 'B', 'C', 'F', 'E', 'D'})
		self.assertEqual(set(g1.edges()), {('B', 'C'), ('C', 'D'), ('F', 'C'), ('A', 'B'), ('D', 'E'), ('E', 'F'), ('A', 'D')})
		g1.removeEdge('C', 'D')
		self.assertEqual(set(g1.edges()), {('A', 'B'), ('E', 'F'), ('F', 'C'), ('A', 'D'), ('B', 'C'), ('D', 'E')})

		g1 = AdjacencyMatrixGraph([1,2,3,4], {(1,2), (1,4), (2,3)})
		self.assertEqual(set(g1.vertices()), {1, 2, 3, 4})
		self.assertEqual(set(g1.edges()), {(1, 2), (1, 4),(2, 3)})
		g1.removeVertex(1)
		self.assertEqual(set(g1.vertices()), {2, 3, 4})
		self.assertEqual(set(g1.edges()), {(2, 3)})

	def testAdjacencyUMatrix(self):
		g1 = AdjacencyMatrixUGraph(['A', 'B', 'C', 'D', 'E', 'F'], {('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('A', 'D'), ('F', 'C')})
		self.assertEqual(set(g1.vertices()), {'A', 'B', 'C', 'F', 'E', 'D'})
		self.assertEqual(set(g1.edges()), {('A', 'B'), ('F', 'C'), ('D', 'E'), ('B', 'C'), ('D', 'C'), ('E', 'D'), ('E', 'F'), ('C', 'B'), ('F', 'E'), ('A', 'D'), ('D', 'A'), ('C', 'F'), ('B', 'A'), ('C', 'D')})
		g1.removeEdge('C', 'D')
		self.assertEqual(set(g1.edges()), {('F', 'E'), ('E', 'D'), ('C', 'F'), ('D', 'E'), ('B', 'A'), ('F', 'C'), ('A', 'D'), ('A', 'B'), ('B', 'C'), ('E', 'F'), ('D', 'A'), ('C', 'B')})

		g1 = AdjacencyMatrixUGraph([1,2,3,4], {(1,2), (1,4), (2,3)})
		self.assertEqual(set(g1.vertices()), {1, 2, 3, 4})
		self.assertEqual(set(g1.edges()), {(1, 2), (3, 2), (2, 1), (1, 4), (2, 3), (4, 1)})
		g1.removeVertex(1)
		self.assertEqual(set(g1.vertices()), {2, 3, 4})
		self.assertEqual(set(g1.edges()), {(2, 3), (3, 2)})


if __name__ == "__main__":
    unittest.main()