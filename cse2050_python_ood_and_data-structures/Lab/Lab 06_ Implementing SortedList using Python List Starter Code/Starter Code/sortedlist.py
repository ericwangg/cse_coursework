class SortedList:
    def __init__(self, L = [], cmpIn = None):
        self._L = L
        self._cmp = cmpIn
        self.ctComparisons = 0
        self.selectionSort()

    # Selection sort provided to you
    def selectionSort(self):
        self.ctComparisons = 0
        for i in range(len(self._L)):
            min_idx = i
            for j in range(i+1, len(self._L)):
                if self._compare(self._L[min_idx], self._L[j]) == 1:
                    min_idx = j
            self._L[i], self._L[min_idx] = self._L[min_idx], self._L[i]
        return self.ctComparisons

    def add(self, item):
        self.ctComparisons = 0
        if len(self._L) == 0:
            self._L.append(item)
            return self._L
        for k in range(len(self._L)):
            if self._compare(self._L[k], item) == 1:
                return self._L.insert(k, item)
            else:
                pass
        return self._L.append(item)
        return self.ctComparisons

    def _compare(self, i, j):
        self.ctComparisons += 1
        if self._cmp != None:
            return self._cmp(i, j)
        else:
            if i > j:
                return 1
            elif i == j:
                return 0
            else:
                return -1

    def setComparison(self, cmpFunction):
        self._cmp = cmpFunction
        self.selectionSort()
		
    def helper(self, L):
        if len(L) <= 1:
            return
        mid = len(L) // 2
        A = L[:mid]
        B = L[mid:]
        self.helper(A)
        self.helper(B)
        return self.merge(A, B, L)

    def mergeSort(self, L):
        self.ctComparisons = 0
        self.helper(L)


    def merge(self, A, B, L):
        i, j = 0, 0
        while i < len(A) and j < len(B):
              if self._compare(A[i], B[j]) == -1:
                  L[i + j] = A[i]
                  i += 1
              else:
                  L[i + j] = B[j]
                  j += 1
        L[i + j:] = A[i:] + B[j:]
        return L

        #     if self._compare(A[i], B[j]) == 0:
        #         self.ctComparisons -= 4
        #         L[i + j], L[(i+j)+1] = A[i], B[j]
        #         i += 1
        #         j += 1
        #     elif self._compare(A[i], B[j]) == 1:
        #         self.ctComparisons -= 2
        #         L[i + j] = A[i]
        #         i += 1
        #     elif self._compare(A[i], B[j]) == -1:
        #         self.ctComparisons -= 2
        #         L[i + j] = B[j]
        #         j += 1
        # return L

    def __contains__(self, item):
        self.ctComparisons = 0
        L = 0
        R = len(self._L)
        while R >= L:
            mid = (L + R) // 2
            if self._compare(self._L[mid], item) == 0:
                return True
            elif self._compare(self._L[mid], item) == 1:
                L = mid + 1
            elif self._compare(self._L[mid], item) == -1:
                R = mid - 1
            return False


    def __str__(self):
        mystring = ""
        for i in self._L:
            mystring += str(i)
            mystring += ","
        return mystring.strip(",")

## DO NOT modify these functions. They are the comparison functions for testing purposes.

def cmpBySum(i, j):
    sum1 = 0
    sum2 = 0
    while i > 0:
        d = i%10
        i = i//10
        sum1 += d
    while j > 0:
        d = j%10
        j = j//10
        sum2 += d
    if sum1 < sum2:
        return -1
    elif sum1 == sum2:
        return 0
    else:
        return 1

def ageCmp(i, j):
    i = i[2]
    j = j[2]
    if i < j:
        return -1
    elif i == j:
        return 0
    else:
        return 1

def nameCmp(x, y):
    x = x[1]
    y = y[1]
    n = min(len(x), len(y))
    for i in range(n):
        if x[i] < y[i]:
            return -1
        elif x[i] > y[i]:
            return 1
        elif i == n-1 and x[i] == y[i]:
            return 0

def stringLenCmp(x, y):
    if len(x) < len(y):
        return -1
    elif len(x) == len(y):
        return 0
    else:
        return 1


sl = SortedList([22, 20, 12, 2, 4, 6, 4, 2, 0, -1, -3])
print(sl)
print(sl.ctComparisons)
