import unittest
from divideandconquer import *

class TestDivideAndConquer(unittest.TestCase):

    def testquickSortLinked(self):
        L = LinkedList()
        L_sort = quickSortLinked(L)
        self.assertEqual(L_sort._head, None)

        l = [2]
        L = LinkedList(l)
        L_sort = quickSortLinked(L)
        self.assertEqual(len(L_sort), 1)
        self.assertEqual(L_sort._head.value, 2)
        self.assertEqual(L_sort._tail.value, 2)

        i = 0
        l = [9, 2]
        l_sort = [2, 9]
        L = LinkedList(l)
        L_sort = quickSortLinked(L)
        currentnode = L_sort._head
        while currentnode is not None:
            self.assertEqual(currentnode.value, l_sort[i])
            currentnode = currentnode.link
            i += 1

        i = 0
        l = [4, 6, 2, 8, 5, 6]
        l_sort = [2, 4, 5, 6, 6, 8]
        L = LinkedList(l)
        L_sort = quickSortLinked(L)
        currentnode = L_sort._head
        while currentnode is not None:
            self.assertEqual(currentnode.value, l_sort[i])
            currentnode = currentnode.link
            i += 1

    def testinplacequicksort(self):
        l = []
        self.assertEqual(quickSortInPlace(l), [])

        l = [2]
        self.assertEqual(quickSortInPlace(l), [2])

        l = [9, 2]
        self.assertEqual(quickSortInPlace(l), [2, 9])

        l = [4, 6, 2, 8, 5, 6]
        self.assertEqual(quickSortInPlace(l), [2, 4, 5, 6, 6, 8])

        l = [1 for i in range(100)]
        self.assertEqual(quickSortInPlace(l), l)

        l = [100-i for i in range(100)]
        l_sort = [i+1 for i in range(100)]
        self.assertEqual(quickSortInPlace(l), l_sort)

    def testquicksort(self):
        l = []
        self.assertEqual(quickSort(l, 0, len(l)), [])

        l = [2]
        self.assertEqual(quickSort(l, 0, len(l)), [2])

        l = [9, 2]
        self.assertEqual(quickSort(l, 0, len(l)), [2, 9])

        l = [4, 6, 2, 8, 5, 6]
        self.assertEqual(quickSort(l, 0, 3), [2, 4, 6, 8, 5, 6])

        l = [1 for i in range(100)]
        self.assertEqual(quickSortInPlace(l, 0, len(l)), l)

        l = [100-i for i in range(100)]
        l_sort = [i+1 for i in range(100)]
        self.assertEqual(quickSortInPlace(l, 0 , len(l)), l_sort)

    def testquicksortwithkey(self):
        l = [76, 34, 91, 47, 33, 89, 10]
        self.assertEqual(quickSort(l, 0, len(l), unitsDigit), [10, 91, 33, 34, 76, 47, 89])
        self.assertEqual(quickSort(l, 0, len(l), decreasing), [91, 89, 76, 47, 34, 33, 10])
        self.assertEqual(quickSort(l, 0, len(l), sumOfDigits), [10, 33, 34, 91, 47, 76, 89])

    def testfindkth(self):
        l = [76, 34, 91, 47, 33, 89, 10]
        self.assertEqual(findKth(l, 1), 10)
        self.assertEqual(findKth(l, 1, decreasing), 91)
        self.assertEqual(findKth(l, 2), 33)
        self.assertEqual(findKth(l, 2, unitsDigit), 91)
        self.assertEqual(findKth(l, 3), 34)
        self.assertEqual(findKth(l, 3, sumOfDigits), 34)
        self.assertEqual(findKth(l, 4), 47)
        self.assertEqual(findKth(l, 4, decreasing), 47)
        self.assertEqual(findKth(l, 5), 76)
        self.assertEqual(findKth(l, 5, unitsDigit), 76)
        self.assertEqual(findKth(l, 6), 89)
        self.assertEqual(findKth(l, 6, sumOfDigits), 76)
        self.assertEqual(findKth(l, 7), 91)
        self.assertEqual(findKth(l, 7, decreasing), 10)

    def testtimeqs(self):
        l = [100-i for i in range(100)]
        starttime = time.time()
        quickSortInPlace(l)
        self.assertTrue(time.time() - starttime < 0.009)

        l = [100-i for i in range(100)]
        starttime = time.time()
        quickSort(l, keyFunc=unitsDigit)
        self.assertTrue(time.time() - starttime < 0.005)

    def testtimefindkth(self):
        l = [100-i for i in range(100)]
        starttime = time.time()
        findKth(l, 65)
        self.assertTrue(time.time() - starttime < 0.0009)

        starttime = time.time()
        findKth(l, 34)
        self.assertTrue(time.time() - starttime < 0.0009)

        starttime = time.time()
        findKth(l, 99)
        self.assertTrue(time.time() - starttime < 0.0009)


if __name__ == "__main__":

    def unitsDigit(item):
        return item%10

    def decreasing(item):
        return -item

    def sumOfDigits(item):
        sum = 0
        while item > 0:
            d = item%10
            item = item//10
            sum += d
        return sum

    unittest.main()
