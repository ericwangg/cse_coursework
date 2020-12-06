import time

class ListNode:
    def __init__(self, value, link = None):
        self.value = value
        self.link = link

class LinkedList:
    def __init__(self, L=[]):
        self._head = None
        self._tail = None
        self._length = 0
        for i in L:
            self.addLast(i)

    def addFirst(self, item):
        self._head = ListNode(item, self._head)
        if self._tail is None:
            self._tail = self._head
        self._length += 1

    def addLast(self, item):
        if self._head is None:
            self.addFirst(item)
        else:
            self._tail.link = ListNode(item)
            self._tail = self._tail.link
            self._length += 1

    def peekLast(self):
        if self._head:
            return self._tail.value
        return None

    def concatenate(self, other):
        if self._head:
            self._tail.link = other._head
            if other:
                self._tail = other._tail
        elif self._head is None:
            return other
        return self

    def __getitem__(self, i):
        cur = self._head
        for j in range(i):
            cur = cur.link
        return cur.value

    def __setitem__(self, i, item):
        cur = self._head
        for j in range(i):
            cur = cur.link
        cur.value = item

    def __str__(self):
        l = []
        cur = self._head
        while cur:
            l.append(cur.value)
            cur = cur.link

        return str(l)

    def __len__(self):
        return self._length

def identity(item):
    return item

def splitTheList(L, mid):
    n = len(L)
    cur1 = L._head
    leftHalf = LinkedList()
    rightHalf = LinkedList()
    for i in range(mid):
        leftHalf.addLast(cur1.value)
        cur1 = cur1.link

    cur2 = L._head
    for i in range(mid):
        cur2 = cur2.link

    if cur2:
        for i in range(mid, n):
            rightHalf.addLast(cur2.value)
            cur2 = cur2.link
    return (leftHalf, rightHalf)

def mergeSort(L):
    # Base Case!
    if len(L) < 2:
        return L

    # Divide!
    mid = len(L) // 2
    leftHalf, rightHalf = splitTheList(L, mid)

    # Conquer!
    leftHalf = mergeSort(leftHalf)
    rightHalf = mergeSort(rightHalf)

    # Combine!
    return merge(leftHalf, rightHalf)


def merge(leftHalf, rightHalf):
  temp = LinkedList()
  A = leftHalf._head
  B = rightHalf._head

  while A and B:
      if A.value < B.value:
          temp.addLast(A.value)
          A = A.link
      else:
          temp.addLast(B.value)
          B = B.link

  if A is None:
      while B:
          temp.addLast(B.value)
          B = B.link
      temp._tail = rightHalf._tail
  elif B is None:
      while A:
          temp.addLast(A.value)
          A = A.link

  return temp

# Part 1
def quickSortLinked(L):
    if len(L) < 2:
        return L
    else:
        pivot = L.peekLast()
        (list1, list2, list3) = splitLinkedList(L, pivot)
        QL1 = quickSortLinked(list1)
        QL2 = quickSortLinked(list2)
        return QL1.concatenate(list3.concatenate(QL2))


def splitLinkedList(L, pivot):
    # (list1, list2, list3) = LinkedList()
    list1 = LinkedList()
    list2 = LinkedList()
    list3 = LinkedList()
    top = L._head
    for x in range(len(L)):
        if top == None:
            break
        elif top.value > pivot:
            list2.addLast(top.value)
        elif top.value < pivot:
            list1.addLast(top.value)
        elif top.value == pivot:
            list3.addLast(top.value)
        top = top.link
    return (list1, list2, list3)


# Part 2
def quickSortInPlace(L, startIdx = 0, endIdx = None):
    if endIdx == None:
        endIdx = len(L)
    if endIdx - startIdx >= 1:
        midIdx = splitList(L, (endIdx - 1), startIdx, endIdx)
        quickSortInPlace(L, startIdx, midIdx)
        quickSortInPlace(L, (midIdx + 1), endIdx)
    return L


def splitList(L, pivot, startIdx, endIdx):
    i = startIdx
    j = pivot - 1
    while i < j:
        while L[i] < L[pivot]:
            i += 1
        while i < j and L[j] >= L[pivot]:
            j -= 1
        if i < j:
            L[i], L[j] = L[j], L[i]
            # newLi = L[j]
            # newLj = L[i]
            # L[i] = newLi
            # L[i] = newLj
    if L[pivot] <= L[i]:
        L[pivot], L[i] = L[i], L[pivot]
        # newerLp = L[i]
        # newerLi = L[pivot]
        # L[pivot] = newerLp
        # L[i] = newerLi
        pivot = i
    return pivot

# def selPivot(L, startIdx = 0, endIdx = -1, keyFunc = identity, pivot = None):
#     first = L[startIdx]
#     middle = L[len(L) // 2]
#     last = L[endIdx - 1]
#     one, two , three = keyFunc(first), keyFunc(middle), keyFunc(last)
#     if one > two and one > three:
#         pivot = first
#     elif two > one and two > three:
#         pivot = middle
#     elif three > one and three > two:
#         pivot = last
#     return pivot

# Part 3 and 4
def quickSort(L, startIdx = 0, endIdx = -1, keyFunc = identity):
    if endIdx == None:
        endIdx = len(L)
    elif endIdx == -1:
        endIdx = len(L) - 1
    elif startIdx < endIdx:
        pivot = L.index(selPivot(L, startIdx, endIdx))

        L[pivot], L[endIdx -1] = L[endIdx -1], L[pivot]

        mid = partition(L, startIdx, endIdx, (endIdx - 1), keyFunc)
        quickSort(L, startIdx, mid, keyFunc)
        quickSort(L, (mid + 1), endIdx, keyFunc)
    return L

def selPivot(L, startIdx, endIdx):
    median = (startIdx + endIdx) // 2
    lst = [L[startIdx], L[median], L[endIdx - 1]]
    lst.sort()
    medd = lst[1]
    return medd

def partition(L, startIdx, endIdx, pivot, keyFunc):
    i = startIdx
    j = endIdx - 1
    while i < j:
        while keyFunc(L[i]) < keyFunc(L[pivot]):
            i += 1
        while i < j and keyFunc(L[j]) >= keyFunc(L[pivot]):
            j -= 1
        if i < j:
            L[i], L[j] = L[j], L[i]
    if keyFunc(L[pivot]) <= keyFunc(L[i]):
        L[pivot], L[i] = L[i], L[pivot]
        pivot = i
    return i

# test quickSort
l = []
print('case 1')
print(quickSort(l, 0, len(l)) == [])

l = [2]
print('case 2')
print(quickSort(l, 0, len(l)) == [2])

l = [9, 2]
print('case 3')
print(quickSort(l, 0, len(l)) == [2, 9])

l = [4, 6, 2, 8, 5, 6]
print('case 4')
print(quickSort(l, 0, 3) == [2, 4, 6, 8, 5, 6])


# L = [i for i in range(1000000)]
# starttime = time.time()
# quickSortInPlace(L, 0, 999999) # this is still using old pivot selection
# print(time.time() - starttime)
# starttime = time.time()
# quickSort(L)
# print(time.time() - starttime)


## Part 5
def findKthLinked(L, k, loud = False):
    if len(L) < 2:
        if L:
            return L[0]
        else:
            return None

    pivot = L.peekLast()

    # uses the splitLinkedList function you write in part 1
    LT, ET, GT = splitLinkedList(L, pivot)
    if loud:
        print("Pivot:", pivot)
        print("Split lists:", LT, ET, GT)

    if k <= len(LT):
        return findKthLinked(LT, k, loud)
    elif k <= (len(LT) + len(ET)):
        return ET[0]
    else:
        k = k - (len(LT) + len(ET))
        return findKthLinked(GT, k, loud)

def findKth(L, k, keyFunc = identity):
    if len(L) < 2:
        if L:
            return L[0]
    pivot = (len(L) - 1) // 2
    LT, ET, GT = splitListKth(L, pivot, keyFunc)
    LLT = len(LT)
    if k <= LLT:
        return findKth(LT, k, keyFunc)
    elif k <= (LLT + len(ET)):
        return ET[0]
    else:
        k = k - (LLT + len(ET))
        return findKth(GT, k, keyFunc)


def splitListKth(L, pivot, keyFunc):
    LP = L[pivot]
    LT, ET, GT = [], [], []
    for x in L:
        if keyFunc(x) < keyFunc(LP):
            LT.append(x)
        elif keyFunc(x) == keyFunc(LP):
            ET.append(x)
        else:
            GT.append(x)
    return LT, ET, GT
    # pivot = (right - left) // 2
    # L[pivot], L[right - 1] = L[right - 1], L[pivot]
    # i, j, pivot = left, right - 2, right - 1
    # while i < j:
    #         while L[i] < L[pivot]:
    #             i += 1
    #         while i < j and L[j] >= L[pivot]:
    #             j -= 1
    #         if i < j:
    #             L[i], L[j] = L[j], L[i]
    # L[pivot], L[i] = L[i], L[pivot]
    # return i

# different key Functions
def unitsDigit(item):
    return item % 10

def decreasing(item):
    return - item

def sumOfDigits(item):
    sum = 0
    while item > 0:
        d = item % 10
        item = item // 10
        sum += d
    return sum

# test findKth
# l = [76, 34, 91, 47, 33, 89, 10]
# print(l)
# print(quickSort(l))
# print('\n')
#
# print('10')
# print(findKth(l, 1) == 10)
#
# print('decreasing 91')
# print(findKth(l, 1, decreasing) == 91)
# print(findKth(l, 2) == 33)
# print(findKth(l, 2, unitsDigit) == 91)
# print(findKth(l, 3) == 34)
# print(findKth(l, 3, sumOfDigits) == 34)

# self.assertEqual(findKth(l, 4), 47)
# self.assertEqual(findKth(l, 4, decreasing), 47)
# self.assertEqual(findKth(l, 5), 76)
# self.assertEqual(findKth(l, 5, unitsDigit), 76)
# self.assertEqual(findKth(l, 6), 89)
# self.assertEqual(findKth(l, 6, sumOfDigits), 76)
# self.assertEqual(findKth(l, 7), 91)
# self.assertEqual(findKth(l, 7, decreasing), 10)


# k = 1000000
# p = 50000
# L = [random(0, k) for i range(k)]
#
# starttime = time.time()
# x1 = findKthSlow(L[:], p)
# print(time.time() - starttime)
#
# x2 = findKth(L[:], p)
# print(time.time() - starttime)
