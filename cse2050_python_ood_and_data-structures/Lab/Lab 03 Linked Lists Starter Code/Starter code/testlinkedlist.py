import unittest, random
from linkedlist import *

class TestLinkedList(unittest.TestCase):

    def testinit(self):
        LL = LinkedList()
        self.assertEqual(LL.L,[])
        LL = LinkedList([1,2,3])
        self.assertNotEqual(LL.L,[])
        self.assertEqual(LL.L,[1,2,3])

    def testlen(self):
        LL = LinkedList()
        LL.addLast(1)
        LL.addLast(2)
        self.assertEqual(len(LL),2)
        LL.addFirst(2)
        self.assertEqual(len(LL),3)

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
        self.assertEqual(LL.L,[1])
        LL.addFirst(3)
        self.assertEqual(LL.L,[3, 1])
        LL.addFirst(LL.L)
        self.assertEqual(LL.L,[[3, 1], 3, 1])

    def testaddlast(self):
        LL = LinkedList()
        LL.addLast(1)
        self.assertEqual(LL.L,[1])
        LL.addLast(LL.L)
        self.assertEqual(LL.L,[1,[1]])
        LL.addLast(23)
        self.assertEqual(LL.L,[1,[1],23])

    def testiterate(self):
        LL = LinkedList()
        LL.addFirst(23)
        LL.addLast((1,2))
        LL.addLast(12)
        LL.addFirst(86)
        self.assertEqual([i for i in LL],[86,23,(1,2),12])

    def testsetitem(self):
        LL = LinkedList()
        LL.addFirst(8)
        LL.addLast(2)
        self.assertEqual(LL.L,[8,2])
        LL[1] = 8
        LL[0] = 2
        self.assertEqual(LL.L,[2,8])
        LL.addLast(10)
        LL[1] = 10
        self.assertEqual(LL.L,[2,10,10])

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
        self.assertEqual(LL.L,[34])
        LL.addLast(32)
        LL.removeFirst()
        self.assertEqual(LL.L,[32])

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
        self.assertEqual(LL[2],20)

    def testremoveat(self):
        LL = LinkedList()
        LL.addAt(0,130)
        self.assertEqual(LL[0],130)
        LL.addAt(1,210)
        LL.addAt(1,234)
        self.assertEqual(LL[2],210)
        LL.removeAt(0)
        self.assertEqual(LL[1],210)

    def testprintcomplex(self):
        LL = LinkedList()
        LL.addFirst(10)
        LL.addLast(20)
        LL.addAt(0,[])
        LL.addAt(2,[1,2,3])
        self.assertEqual(str(LL),"[[];10;[1, 2, 3];20]")

if __name__ == "__main__":
    unittest.main()
