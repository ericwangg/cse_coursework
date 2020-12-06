import unittest
from treetraversal import *

class TestTreeTraversal(unittest.TestCase):
    def testbinarytree(self):
        expr = ('*', ('+', 5, 3), ('-', 4, 1))
        exprTree = BinaryTree(expr)
        self.assertEqual(exprTree.data, '*')
        self.assertEqual(exprTree.leftChild.data, '+')
        self.assertEqual(exprTree.rightChild.data, '-')

        expr = ('-', ('*', ('+', 7, 2), 9), 1)
        exprTree = BinaryTree(expr)
        self.assertEqual(exprTree.data, '-')
        self.assertEqual(exprTree.leftChild.data, '*')
        self.assertEqual(exprTree.rightChild.data, 1)

        expr = ('*', (10), ('+', 55, 16))
        exprTree = BinaryTree(expr)
        self.assertEqual(exprTree.data, '*')
        self.assertEqual(exprTree.leftChild.data, 10)
        self.assertEqual(exprTree.rightChild.data, '+')

        expr = ('*')
        exprTree = BinaryTree(expr)
        self.assertEqual(exprTree.data, '*')
        self.assertEqual(exprTree.leftChild, None)
        self.assertEqual(exprTree.rightChild, None)

    def testvalue(self):
        data = ['+', '-', '*', '/', 'sum', 'min', 'max', 'avg']
        val1 = [40, 50]
        val2 = [99, 33]
        val3 = [10000000, 100000]

        res1 = [90, -10, 2000, 0.8, 90, 40, 50, 45]
        res2 = [132, 66, 3267, 3, 132, 33, 99, 66]
        res3 = [10100000, 9900000, 1000000000000, 100, 10100000, 100000, 10000000, 5050000]
        for i in range(len(data)):
            self.assertEqual(value(data[i], val1), res1[i])
            self.assertEqual(value(data[i], val2), res2[i])
            self.assertEqual(value(data[i], val3), res3[i])

    def testcomputevalue(self):
        expr1 = ('+',('sum',5,3,9,4),17) # sum(5,3,9,4) + 17 = 38
        exprTree1 = Tree(expr1)
        x = exprTree1.computeValue()
        self.assertEqual(x, 38)  

        expr2 = ('-', ('avg', 5, 3, 7, 2), 46)
        exprTree2 = Tree(expr2)
        x = exprTree2.computeValue()
        self.assertEqual(x, -41.75)

        expr3 = ('min', ('*', 23, 8789), 998876)
        exprTree3 = Tree(expr3)
        x = exprTree3.computeValue()
        self.assertEqual(x, 202147.0)

    def testcomputespaceusage(self):
        Tfile = [('CSE1010/', None), [('Section 1', None), [('HWs/', None), [('hw1.doc', 5)], [('hw2.doc', 15)]], [('LABs/', None), [('lab1.py', 7)], [('lab2.py', 10)], [('lab3.py', 10)]]], [('Section 2', None), [('HWs/', None), [('hw1.doc', 5)], [('hw2.doc', 18)]], [('LABs/', None), [('lab1.py', 6)], [('lab2.py', 10)], [('lab3.py', 14)]]], [('ToDoList.txt', 20)]]
        treeFile = Tree(Tfile)
        self.assertEqual(treeFile.compute(spaceusage), 120)

        Tfile = [('CSE1010/', None), [('Section 1', None), [('HWs/', None), [('hw2.doc', 15)]], [('LABs/', None), [('lab1.py', 7)], [('lab2.py', 10)], [('lab3.py', 10)]]], [('Section 2', None), [('HWs/', None), [('hw1.doc', 5)], [('hw2.doc', 18)]], [('LABs/', None), [('lab1.py', 6)], [('lab2.py', 10)], [('lab3.py', 14)]]], [('ToDoList.txt', 20)]]
        treeFile = Tree(Tfile)
        self.assertEqual(treeFile.compute(spaceusage), 115)

        Tfile = [('CSE1010/', None), [('Section 1', None), [('HWs/', None), [('hw1.doc', 5)], [('hw2.doc', 15)], [('hw3.doc', 67)]], [('LABs/', None), [('lab1.py', 7)], [('lab2.py', 10)], [('lab3.py', 10)]]], [('Section 2', None), [('HWs/', None), [('hw1.doc', 5)], [('hw2.doc', 18)]], [('LABs/', None), [('lab1.py', 6)], [('lab2.py', 10)], [('lab3.py', 14)]]], [('ToDoList.txt', 20)], [('Exam.pdf', 423)]]
        treeFile = Tree(Tfile)
        self.assertEqual(treeFile.compute(spaceusage), 610)

if __name__ == "__main__":
    unittest.main()



