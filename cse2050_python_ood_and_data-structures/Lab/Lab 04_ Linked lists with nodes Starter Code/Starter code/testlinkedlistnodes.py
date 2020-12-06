import unittest, random
from linkedlist_nodes import *

class TestLinkedList(unittest.TestCase):

    def testinit(self):
        LL = LinkedList()
        self.assertEqual(LL._head, None)
        self.assertEqual(LL._tail, None)
        self.assertEqual(LL._nodeCount, 0)

    def testnode(self):
        LL = LinkedList()
        for i in range(100):
            LL.addFirst(i)
        self.assertEqual(LL._head.link.value, 98)

    def testlen(self):
        LL = LinkedList()
        LL.addLast(1)
        LL.addLast(2)
        self.assertEqual(len(LL),2)
        LL.addLast(3)
        LL.addFirst(2)
        self.assertEqual(len(LL),4)

    def testlenlong(self):
        LL = LinkedList()
        numberOfItems = random.randrange(0,1000)
        i = 0
        while i < numberOfItems:
            LL.addFirst(1)
            i += 1
        self.assertEqual(len(LL),numberOfItems)

    def testlendynamic(self):
        LL = LinkedList()
        LL.addLast(1)
        LL.addLast(2)
        self.assertEqual(len(LL),2)
        LL.addFirst(2)
        self.assertEqual(len(LL),3)
        LL.removeFirst()
        LL.addLast(24)
        self.assertEqual(len(LL),3)
        LL.removeLast()
        self.assertEqual(len(LL),2)

    def testaddfirst(self):
        LL = LinkedList()
        LL.addFirst(1)
        self.assertEqual(LL._head.value, 1)
        self.assertEqual(LL._tail.value, 1)
        LL.addFirst(3)
        self.assertEqual(LL._head.value, 3)
        self.assertEqual(LL._tail.value, 1)
        LL.addFirst(4)
        LL.addFirst(6)
        self.assertEqual(LL._head.value, 6)
        self.assertEqual(LL._tail.value, 1)

    def testaddlast(self):
        LL = LinkedList()
        LL.addLast(1)
        self.assertEqual(LL._head.value, 1)
        self.assertEqual(LL._tail.value, 1)
        LL.addLast(4)
        self.assertEqual(LL._head.value, 1)
        self.assertEqual(LL._tail.value, 4)
        LL.addLast(23)
        self.assertEqual(LL._head.value, 1)
        self.assertEqual(LL._tail.value, 23)

    def testiterate(self):
        LL = LinkedList()
        LL.addFirst(23)
        LL.addLast(55)
        LL.addLast(12)
        LL.addFirst(86)
        self.assertEqual([i for i in LL],[86, 23, 55, 12])

    def testsetitem(self):
        LL = LinkedList()
        LL.addFirst(8)
        LL.addLast(2)
        self.assertEqual(LL._head.value, 8)
        self.assertEqual(LL._tail.value, 2)
        LL[1] = 8
        LL[0] = 2
        self.assertEqual(LL._head.value, 2)
        self.assertEqual(LL._tail.value, 8)
        LL.addLast(10)
        LL[1] = 10
        self.assertEqual(LL._head.value, 2)
        self.assertEqual(LL._head.link.value, 10)

    def teststrcast(self):
        LL = LinkedList()
        self.assertEqual(str(LL),"[]")
        LL.addFirst([])
        self.assertEqual(str(LL),"[[]]")
        LL.addLast(35)
        self.assertEqual(str(LL),"[[];35]")
        LL.addFirst(dict())
        self.assertEqual(str(LL),"[{};[];35]")

    def testcontains(self):
        LL = LinkedList()
        LL.addLast(47)
        self.assertTrue(47 in LL)
        LL.addFirst(98)
        self.assertTrue(98 in LL)

    def testremovefirst(self):
        LL = LinkedList()
        LL.addLast(34)
        LL.addFirst(24)
        LL.removeFirst()
        self.assertEqual(LL._head.value, 34)
        self.assertEqual(LL._tail.value, 34)
        LL.addLast(32)
        LL.removeFirst()
        self.assertEqual(LL._head.value, 32)
        self.assertEqual(LL._tail.value, 32)

    def testindex(self):
        LL = LinkedList()
        LL.addFirst(10)
        LL.addLast(20)
        LL.addFirst(30)
        LL.addFirst(25)
        self.assertEqual(LL[1],30)
        self.assertEqual(LL[3],20)
        LL[0] = 2
        self.assertEqual(LL[0],2)
        LL[1] = (1,2)
        self.assertEqual(LL[1],(1,2))

    def testaddat(self):
        LL = LinkedList()
        LL.addAt(0,10)
        self.assertEqual(LL[0],10)
        LL.addAt(1,20)
        LL.addAt(1,24)
        self.assertEqual(LL._head.value, 10)
        self.assertEqual(LL._tail.value, 20)
        self.assertEqual(LL[1], 24)

    def testremoveat(self):
        LL = LinkedList()
        LL.addAt(0,130)
        self.assertEqual(LL[0],130)
        LL.addAt(1,210)
        LL.addAt(1,234)
        self.assertEqual(LL[2],210)
        LL.removeAt(0)
        self.assertEqual(LL._head.value,234)
        self.assertEqual(LL._tail.value,210)

    def testappend(self):
        LL = LinkedList()
        LL1 = LinkedList()
        for i in range(30):
            LL1.addFirst(1)
        self.assertEqual(LL._nodeCount, 0)
        self.assertEqual(LL1._nodeCount, 30)
        self.assertEqual(LL._head, None)
        self.assertEqual(LL._tail, None)
        self.assertEqual(LL1._head.value, 1)
        self.assertEqual(LL1._tail.value, 1)
        LL.append(LL1)                          # append non empty list to empty list
        self.assertEqual(LL._nodeCount, 30)
        self.assertEqual(LL1._nodeCount, 0)
        self.assertEqual(LL._head.value, 1)
        self.assertEqual(LL._tail.value, 1)
        self.assertEqual(LL1._head, None)
        self.assertEqual(LL1._tail, None)
        LL.append(LL1)                          # append empty list to non empty list
        self.assertEqual(LL._nodeCount, 30)
        self.assertEqual(LL1._nodeCount, 0)
        for i in range(40):
            LL1.addFirst(0)
        self.assertEqual(LL._nodeCount, 30)
        self.assertEqual(LL1._nodeCount, 40)
        LL.append(LL1)                          # append two non empty lists
        self.assertEqual(LL._nodeCount, 70)
        self.assertEqual(LL1._nodeCount, 0)
        self.assertEqual(LL._head.value, 1)
        self.assertEqual(LL._tail.value, 0)

    def testprintcomplex(self):
        LL = LinkedList()
        LL.addFirst(10)
        LL.addLast(20)
        LL.addAt(0,[])
        LL.addAt(2,[1,2,3])
        self.assertEqual(str(LL),"[[];10;[1, 2, 3];20]")

if __name__ == "__main__":
    unittest.main()
