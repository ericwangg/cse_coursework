import unittest, random
from adddoublylinkedlists import *

class TestLinkedList(unittest.TestCase):

    def testinit(self):
        s1 = '1234'
        dll1 = DoublyLinkedList(s1)

        s2 = '99'
        dll2 = DoublyLinkedList(s2)

        self.assertEqual(dll1.head.value, 1)
        self.assertEqual(dll1.tail.value, 4)
        self.assertEqual(dll2.head.value, 9)
        self.assertEqual(dll2.tail.value, 9)

    def testaddfirst(self):
        dll = DoublyLinkedList()
        for i in range(30):
            dll.addFirst(i)

        self.assertEqual(dll.head.value, 29)
        self.assertEqual(dll.tail.value, 0)

    def testaddlast(self):
        dll = DoublyLinkedList()
        for i in range(30):
            dll.addLast(i)

        self.assertEqual(dll.head.value, 0)
        self.assertEqual(dll.tail.value, 29)

    def testreverse(self):
        dll = DoublyLinkedList()
        for i in range(30):
            dll.addFirst(i)

        self.assertEqual(dll.head.value, 29)
        self.assertEqual(dll.tail.value, 0)

        dll.reverse()

        self.assertEqual(dll.head.value, 0)
        self.assertEqual(dll.tail.value, 29)

    def testfastreversed(self):
        dll = DoublyLinkedList()
        for i in range(30):
            dll.addFirst(i)

        dll.fastReverse()
        self.assertEqual(dll.isReversed, True)
        self.assertEqual(dll.head.value, 0)
        self.assertEqual(dll.tail.value, 29)

    def testsumlinkednumbers(self):
        s1 = '5930'
        dll1 = DoublyLinkedList(s1)

        s2 = '457'
        dll2 = DoublyLinkedList(s2)

        self.assertEqual(str(sumlinkednumbers(dll1, dll2)), '6387')

        s1 = '457'
        dll1 = DoublyLinkedList(s1)

        s2 = '5930'
        dll2 = DoublyLinkedList(s2)

        self.assertEqual(str(sumlinkednumbers(dll1, dll2)), '6387')

        s1 = '00457'
        dll1 = DoublyLinkedList(s1)

        s2 = '5930'
        dll2 = DoublyLinkedList(s2)

        self.assertEqual(str(sumlinkednumbers(dll1, dll2)), '6387')

        s1 = '00457'
        dll1 = DoublyLinkedList(s1)  

        self.assertEqual(str(dll1), '457')

        s1 = '5930'
        dll1 = DoublyLinkedList(s1)
        dll1.fastReverse()

        s2 = '457'
        dll2 = DoublyLinkedList(s2)

        self.assertEqual(str(sumlinkednumbers(dll1, dll2)), '852')

        dll2.fastReverse()
        self.assertEqual(str(sumlinkednumbers(dll1, dll2)), '1149')


if __name__ == "__main__":
    unittest.main()
