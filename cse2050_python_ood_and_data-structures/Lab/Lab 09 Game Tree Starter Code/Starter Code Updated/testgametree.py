import unittest
from gametree import *

class TestGameTree(unittest.TestCase):
    def testDfsBfsCapture(self):
    	bb = Board([(1, 1), (0, 3), (1, 5), (2, 3)])
    	self.assertTrue(dfsCapture(bb))
    	self.assertTrue(bfsCapture(bb))

    	bb = Board([(2, 2), (1, 4), (0, 2), (1, 0), (3, 1)])
    	self.assertTrue(dfsCapture(bb))
    	self.assertTrue(bfsCapture(bb))

    	bb = Board([(1, 1), (0, 3), (1, 5), (2, 3)])
    	self.assertTrue(dfsCapture(bb))
    	self.assertTrue(bfsCapture(bb))

    	bb = Board([(4, 5), (3, 7), (2, 1), (7, 4), (5, 5), (0, 6), (7, 7), (2, 2), (7, 0)])
    	self.assertFalse(dfsCapture(bb))
    	self.assertFalse(bfsCapture(bb))

    def testfindpath(self):
    	bb = Board([(1, 1), (0, 3), (1, 5), (2, 3)])
    	sol = [(2, 3), (1, 5), (0, 3)]
    	self.assertEqual(findPath(bb), sol)

    	bb = Board([(2, 2), (1, 4), (0, 2), (1, 0), (3, 1)])
    	sol = [(1, 4), (0, 2), (1, 0), (3, 1)]
    	self.assertEqual(findPath(bb), sol)

    	bb = Board([(1,1), (3,2), (5,3), (0,3)])
    	sol = []
    	self.assertEqual(findPath(bb), sol)

    	bb = Board([(4, 5), (3, 7), (2, 1), (7, 4), (5, 5), (0, 6), (7, 7), (2, 2), (7, 0)])
    	sol = []
    	self.assertEqual(findPath(bb), sol)

    def testfindallpaths(self):
    	bb = Board([(1, 1), (0, 3), (1, 5), (2, 3)])
    	sol = [[(1, 1), (2, 3), (1, 5), (0, 3)], [(1, 1), (0, 3), (1, 5), (2, 3)]]
    	self.assertEqual(findAllPaths(bb), sol)

    	bb = Board([(1, 1), (0, 3), (1, 5), (2, 3), (2, 7), (3, 5)])
    	sol = [[(1, 1), (2, 3), (3, 5), (2, 7), (1, 5), (0, 3)], [(1, 1), (0, 3), (1, 5), (2, 7), (3, 5), (2, 3)], [(1, 1), (0, 3), (1, 5), (2, 3), (3, 5), (2, 7)]]
    	self.assertEqual(findAllPaths(bb), sol)

    	bb = Board([(1,1), (3,2), (5,3), (0,3)])
    	sol = []
    	self.assertEqual(findAllPaths(bb), sol)

if __name__ == "__main__":
    unittest.main()