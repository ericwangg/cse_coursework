import unittest, random
from sortedlist import *

class TestLinkedList(unittest.TestCase):

    def testsetcomparison(self):
        sl = SortedList([])
        self.assertEqual(sl._cmp, None)
        sl.setComparison(cmpBySum)
        self.assertEqual(sl._cmp, cmpBySum)

    def testaddint(self):
        sl = SortedList([])
        sl.add(123)
        sl.add(34)
        sl.add(26)
        sl.add(9)
        self.assertEqual(sl._L, [9, 26, 34, 123])
        self.assertEqual(sl.ctComparisons, 3)

        sl.setComparison(cmpBySum)
        self.assertEqual(sl._L, [123, 34, 26, 9])

    def testaddtuples(self):
        l_id = [(1, 'Amy', 18), (2, 'Jessica', 19), (3, 'Becky', 20), (4, 'Harry', 17), (5, 'Tom', 16), (6, 'Ben', 21), (7, 'Amy', 10)]
        sl = SortedList([])
        sl.add((2, 'Jessica', 19))
        sl.add((6, 'Ben', 21))
        sl.add((4, 'Harry', 17))
        sl.add((3, 'Becky', 20))
        sl.add((1, 'Amy', 18))
        sl.add((5, 'Tom', 16))
        sl.add((7, 'Amy', 10))
        self.assertEqual(sl._L, l_id)
        self.assertEqual(sl.ctComparisons, 17)

        l_name = [(1, 'Amy', 18), (7, 'Amy', 10), (3, 'Becky', 20), (6, 'Ben', 21), (4, 'Harry', 17), (2, 'Jessica', 19), (5, 'Tom', 16)]
        sl.setComparison(nameCmp)
        self.assertEqual(sl._L, l_name)
        self.assertEqual(sl.ctComparisons, 21)

        l_age = [(7, 'Amy', 10), (5, 'Tom', 16), (4, 'Harry', 17), (1, 'Amy', 18), (2, 'Jessica', 19), (3, 'Becky', 20), (6, 'Ben', 21)]
        sl.setComparison(ageCmp)
        self.assertEqual(sl._L, l_age)
        self.assertEqual(sl.ctComparisons, 21)

    def teststrings(self):
        sl = SortedList(["Banana", "Candy", "Coconut", "Beetroot"], stringLenCmp)
        self.assertEqual(sl._L, ["Candy", "Banana", "Coconut", "Beetroot"])
        self.assertEqual(sl.ctComparisons, 6)

    def testcontains(self):
        sl = SortedList([6, 33, 11, 45, 8, 1, 34])
        test = 11 in sl
        self.assertEqual(sl.ctComparisons, 1)

        sl1 = SortedList(["Banana", "Candy", "Coconut", "Beetroot"], stringLenCmp)
        test = "Beetroot" in sl1
        self.assertEqual(sl1.ctComparisons, 4)

        sl2 = SortedList([(1, 'Amy', 18), (2, 'Jessica', 19), (3, 'Becky', 20), (4, 'Harry', 17), (5, 'Tom', 16), (6, 'Ben', 21), (7, 'Amy', 10)])
        test = (2, 'Jessica', 19) in sl2
        self.assertEqual(sl2.ctComparisons, 6)

    def testmergesort(self):
        sl = SortedList([22, 20, 12, 2, 4, 6, 4, 2, 0, -1, -3])
        self.assertEqual(sl.mergeSort(sl._L), 60)

        sl = SortedList([4, 10, -20, -3, 5, 8, 2, 2])
        self.assertEqual(sl.mergeSort(sl._L), 39)

        sl = SortedList([6, 8, -2, 0, 1, -6])
        self.assertEqual(sl.mergeSort(sl._L), 27)

        sl = SortedList([100, 99, 98, 97, 96, 1, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85, 2])
        self.assertEqual(sl.mergeSort(sl._L), 111)

        sl = SortedList([10])
        self.assertEqual(sl.mergeSort(sl._L), 1)

        sl = SortedList([])
        self.assertEqual(sl.mergeSort(sl._L), 1)

    def testmerge(self):
        A1 = [-3, -1, 0, 4, 12]
        B1 = [2, 5, 6, 7, 8, 20]
        sl = SortedList([-3, 0, -1, 12, 4, 5, 7, 6, 8, 2, 20])
        self.assertEqual(sl.merge(A1, B1, sl._L), 11)

        A2 = [8]
        B2 = [2, 20]
        sl = SortedList([8, 2, 20])
        self.assertEqual(sl.merge(A2, B2, sl._L), 3)

        A3 = []
        B3 = []
        sl = SortedList([])
        self.assertEqual(sl.merge(A3, B3, sl._L), 0)

        A4 = [-20, -3, 4, 10]
        B4 = [2, 2, 5, 8]
        sl = SortedList([4, 10, -20, -3, 5, 8, 2, 2])
        self.assertEqual(sl.merge(A4, B4, sl._L), 8)

if __name__ == "__main__":
    unittest.main()

