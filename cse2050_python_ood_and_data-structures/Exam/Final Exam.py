def insertionSort(L):
    n = len(l)
    for i in range(n):
        print('i = ', i)
        for j in range(n-i-1, n-1):
            print('j = ', j)
            if L[j] > L[j+1]:
                print(j)
                print(j+1)
                L[j], L[j+1] = L[j+1], L[j]
                print('cycle')


l = [3, 4, 2, 7,4,5]
insertionSort(l)
print(l)

a = 255
b = 255
print(a is b)
print(a == b)

c = 256
d = 256
print(c is d)


print('\n')

l = [1, 2, 3]
s = (l, 4)
print(s)
l = [1, 2]
# s = (l, 4)
print(s)

def f():
    a = 2
    def g():
        nonlocal a
        a = 3
        print(a)
    g()
    print(a)
a = 1
f()
print(a)


L = [2, 4, 6, 8]  # sum 20

# def sumIter(L):
#     count = 0
#     i = iter(L)
#     while len(L) > 0:
#         try:
#             count += next(i)
#         except len(L) == 0:
#             raise StopIteration
#     return count
#
# sumIter(L)

def createIndexMap(s):
    map = dict()
    for letter in range(len(s)):
        if s[letter] in map:
            map[letter].append(s[letter])
        else:
            map[s[letter]] = letter
    print(map)

s = 'string'
createIndexMap(s)

print('\n')
# print('createIndexMap2')
#
# def createIndexMap2(s):
#     map = dict()
#     for letter in s:
#         if letter in map:
#             map[letter].append(s.index(letter))
#         else:
#             map[letter] = s.index(letter)
#     print(map)
#
# s = 'stringstring'
# createIndexMap2(s)

print('\n')
print('createIndexMap3')

def CIMap3(s):
    map = dict()
    for i, j in enumerate(s):
        if j in map:
            map[j].append(i)
        else:
            map[j] = [i]
    print(map)

s = 'hippopot'
CIMap3(s)
